"""
app.py
------
StudentHive Streamlit prototype - UI layer only.
 
This file is only responsible for rendering screens and handling navigation.
All data / business logic lives in Marketplace (marketplace.py) and the
Listing/Gig/Rental classes (listing.py). The UI talks to the Marketplace
object through its public methods and never manipulates listings directly.
"""
 
import streamlit as st
from Marketplace import Marketplace
 
st.set_page_config(page_title="StudentHive", page_icon="🐝", layout="wide")
 
# ---------------------------------------------------------------------------
# One shared Marketplace instance per session (cached so it survives reruns
# but is rebuilt fresh for every new user/session).
# ---------------------------------------------------------------------------
@st.cache_resource
def get_marketplace():
    return Marketplace()
 
 
marketplace = get_marketplace()
 
# ---------------------------------------------------------------------------
# Session state / simple navigation
# ---------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "selected_listing_id" not in st.session_state:
    st.session_state.selected_listing_id = None
if "dashboard_tab" not in st.session_state:
    st.session_state.dashboard_tab = "My Listings"
 
 
def go_to(page, listing_id=None):
    st.session_state.page = page
    if listing_id is not None:
        st.session_state.selected_listing_id = listing_id
 
 
# ---------------------------------------------------------------------------
# Styling to loosely match the mock-ups
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #000000; }
    .shive-title { color: #0f766e; font-weight: 800; }
    .listing-card {
        border: 1px solid #eef0f2;
        border-radius: 14px;
        padding: 0;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 18px;
    }
    .listing-image {
        background: linear-gradient(to bottom, #cdeafe 60%, #86b93c 60%, #6a9c2b 100%);
        height: 110px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 42px;
    }
    .listing-body { padding: 14px 16px; }
    .badge {
        display: inline-block;
        color: black;
        padding: 3px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }
    .price-tag { font-weight: 700; color: #1f2937; float: right; }
    .welcome-box {
        background: #eef1f4;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
 
# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 class='shive-title'>🐝 StudentHive</h2>", unsafe_allow_html=True)
    st.markdown("---")
 
    if st.button("🏠 Dashboard", use_container_width=True):
        go_to("dashboard")
    if st.button("🛒 Marketplace", use_container_width=True):
        go_to("marketplace")
    if st.button("💼 Gigs", use_container_width=True):
        st.session_state.dashboard_tab = "Gigs"
        go_to("dashboard")
    if st.button("🔑 Rentals", use_container_width=True):
        st.session_state.dashboard_tab = "Rentals"
        go_to("dashboard")
    st.button("💬 Messages", use_container_width=True, disabled=True)
 
    st.markdown("---")
    st.button("⚙️ Settings", use_container_width=True, disabled=True)
 
 
# ---------------------------------------------------------------------------
# Reusable card renderer
# ---------------------------------------------------------------------------
def render_listing_card(listing, key_prefix):
    with st.container():
        st.markdown(
            f"""
            <div class="listing-card">
                <div class="listing-image">{listing.image_emoji}</div>
                <div class="listing-body">
                    <div><b>{listing.title}</b></div>
                    <div style="margin-top:8px;">
                        <span class="badge" style="background-color:{listing.badge_color()};">
                            {listing.type_label()}
                        </span>
                        <span class="price-tag">{listing.price_display}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View listing", key=f"{key_prefix}_{listing.id}", use_container_width=True):
            go_to("listing", listing.id)
            st.rerun()
 
 
# ---------------------------------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------------------------------
def render_dashboard():
    st.markdown(
        """
        <div class="welcome-box">
            <h2 style="margin-bottom:4px;">Welcome, User! 👋</h2>
            <div style="color:#4b5563;">Here's what's happening in your hive today.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
    tabs = ["My Listings", "Gigs", "Rentals"]
    default_index = tabs.index(st.session_state.dashboard_tab) if st.session_state.dashboard_tab in tabs else 0
    chosen = st.radio("Dashboard sections", tabs, index=default_index, horizontal=True, label_visibility="collapsed")
    st.session_state.dashboard_tab = chosen
    st.markdown("---")
 
    if chosen == "My Listings":
        listings = marketplace.get_listings_by_owner("User")
    elif chosen == "Gigs":
        listings = marketplace.get_listings_by_type("Gig")
    else:
        listings = marketplace.get_listings_by_type("Rental")
 
    if not listings:
        st.info("Nothing here yet.")
        return
 
    cols = st.columns(2)
    for i, listing in enumerate(listings):
        with cols[i % 2]:
            render_listing_card(listing, key_prefix="dash")
 
 
# ---------------------------------------------------------------------------
# MARKETPLACE PAGE
# ---------------------------------------------------------------------------
def render_marketplace():
    st.title("Marketplace")
    st.caption("Browse verified Gigs and Rentals across your campus")
 
    filter_choice = st.radio(
        "Filter", ["All", "Gig", "Rental"], horizontal=True, label_visibility="collapsed"
    )
 
    listings = marketplace.get_all_listings()
    if filter_choice != "All":
        listings = [l for l in listings if l.type_label() == filter_choice]
 
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, listing in enumerate(listings):
        with cols[i % 3]:
            render_listing_card(listing, key_prefix="mkt")
 
 
# ---------------------------------------------------------------------------
# LISTING DETAIL PAGE
# ---------------------------------------------------------------------------
def render_listing_detail():
    listing = marketplace.get_listing_by_id(st.session_state.selected_listing_id)
 
    if listing is None:
        st.warning("That listing couldn't be found.")
        if st.button("← Back to Marketplace"):
            go_to("marketplace")
            st.rerun()
        return
 
    st.markdown(f"**Marketplace** > **{listing.title}**")
    if st.button("← Back"):
        go_to("marketplace")
        st.rerun()
 
    main_col, side_col = st.columns([3, 1])
 
    with main_col:
        st.markdown(
            f"""
            <div style="background:linear-gradient(to bottom, #cdeafe 55%, #86b93c 55%, #6a9c2b 100%);
                        border-radius:14px; height:260px; display:flex; align-items:center;
                        justify-content:center; font-size:90px;">
                {listing.image_emoji}
            </div>
            """,
            unsafe_allow_html=True,
        )
 
        st.markdown(f"## {listing.title}")
        st.markdown(
            f"<span class='badge' style='background-color:{listing.badge_color()};'>{listing.type_label()}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
 
        st.subheader("About this " + listing.type_label())
        for paragraph in listing.description.split("\n\n"):
            st.write(paragraph)
 
        detail_cols = st.columns(2)
        for i, (heading, items) in enumerate(listing.details.items()):
            with detail_cols[i % 2]:
                st.markdown(f"**{heading}**")
                for item in items:
                    st.markdown(f"- {item}")
 
    with side_col:
        with st.container(border=True):
            st.markdown(f"### {listing.price_display}")
            st.markdown(f"**{listing.owner}**")
            st.caption("StudentHive member")
            st.markdown("")
            if st.button("Message Owner", use_container_width=True):
                st.toast(f"Message sent to {listing.owner}! (prototype only)")
            if st.button("Request Booking", use_container_width=True, type="primary"):
                st.toast("Booking requested! (prototype only)")
 
 
# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
page = st.session_state.page
if page == "dashboard":
    render_dashboard()
elif page == "marketplace":
    render_marketplace()
elif page == "listing":
    render_listing_detail()