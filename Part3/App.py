import streamlit as st
from Marketplace import Marketplace

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="StudentHive",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Shared Marketplace instance
# ---------------------------------------------------------------------------
@st.cache_resource
def get_marketplace():
    return Marketplace()


marketplace = get_marketplace()

# ---------------------------------------------------------------------------
# Session state / navigation
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
# CSS - designed to closely follow the provided StudentHive mock-up
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- Global ---------- */
    :root {
        --navy: #1f2d43;
        --teal: #0f8f83;
        --teal-dark: #08766f;
        --light-blue: #b8d9ec;
        --sidebar: #e8eff3;
        --page: #ffffff;
        --line: #d6d9dc;
        --muted: #657080;
        --card: #ffffff;
        --amber: #f6a000;
    }

    .stApp {
        background: var(--page);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 1.6rem;
        padding-bottom: 2rem;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: var(--sidebar);
        border-right: 1px solid #d5dde2;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.35rem 1.15rem;
    }

    .sidebar-logo {
        color: var(--teal);
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.7px;
        margin: 0.15rem 0 1rem 0.15rem;
    }

    .sidebar-rule {
        height: 3px;
        background: #c8d3da;
        border-radius: 3px;
        margin: 0 0.05rem 1rem 0.05rem;
    }

    section[data-testid="stSidebar"] .stButton {
        margin: 0.18rem 0;
    }

    section[data-testid="stSidebar"] .stButton > button {
        border: none !important;
        background: transparent !important;
        color: var(--navy) !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        border-radius: 12px !important;
        padding: 0.75rem 0.95rem !important;
        min-height: 46px !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #d8e5ed !important;
        color: var(--navy) !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #b4d5e8 !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] hr {
        border: none;
        border-top: 3px solid #c8d3da;
        margin: 1.6rem 0;
    }

    /* ---------- Typography ---------- */
    h1, h2, h3, h4, p, label {
        color: var(--navy);
    }

    /* ---------- Welcome panel ---------- */
    .welcome-box {
        background: #eaf0f4;
        border-radius: 22px;
        min-height: 170px;
        padding: 26px 38px;
        display: flex;
        align-items: center;
        gap: 34px;
        margin-bottom: 1.4rem;
    }

    .avatar-ring {
        width: 116px;
        height: 116px;
        min-width: 116px;
        border: 4px solid #44c9bf;
        border-radius: 50%;
        background: #edf4f6;
    }

    .welcome-title {
        font-size: 2.05rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 0 0 0.65rem 0;
        color: var(--navy);
    }

    .welcome-subtitle {
        font-size: 1.15rem;
        color: #354156;
        margin: 0;
    }

    /* ---------- Dashboard tabs ---------- */
    .tabs-wrap {
        margin: 0.25rem 0 1.4rem;
        border-bottom: 2px solid #d5d5d5;
    }

    div[data-testid="stRadio"] > label {
        display: none;
    }

    div[role="radiogroup"] {
        gap: 0 !important;
        border-bottom: none !important;
    }

    div[role="radiogroup"] > label {
        min-width: 180px;
        padding: 0.65rem 0.5rem 0.85rem 0.5rem !important;
        margin-right: 2rem !important;
        color: #596272 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-bottom: 4px solid transparent;
    }

    div[role="radiogroup"] > label:hover {
        color: var(--teal) !important;
    }

    div[role="radiogroup"] > label[data-checked="true"] {
        color: var(--teal-dark) !important;
        border-bottom-color: var(--teal-dark) !important;
    }

    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* ---------- Cards ---------- */
    .listing-card {
        background: var(--card);
        border-radius: 20px;
        overflow: hidden;
        display: flex;
        min-height: 156px;
        box-shadow: 0 10px 28px rgba(31, 45, 67, 0.08);
        border: 1px solid #f1f3f5;
        margin-bottom: 1rem;
    }

    .listing-image {
        width: 43%;
        min-width: 43%;
        min-height: 156px;
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at 17% 26%, rgba(255,255,255,0.95) 0 9px, transparent 10px),
            radial-gradient(circle at 25% 22%, rgba(255,255,255,0.95) 0 14px, transparent 15px),
            radial-gradient(circle at 34% 24%, rgba(255,255,255,0.95) 0 10px, transparent 11px),
            linear-gradient(to bottom, #cdeefe 0%, #b8e0f5 66%, #d0ea86 66%, #9fca2e 82%, #7fae12 82%, #7fae12 100%);
    }

    .listing-image::before {
        content: "";
        position: absolute;
        left: -8%;
        right: 5%;
        bottom: 21%;
        height: 30px;
        background: #bada63;
        border-radius: 50% 55% 40% 60%;
        transform: rotate(3deg);
    }

    .listing-image::after {
        content: "";
        position: absolute;
        right: -7%;
        bottom: 9%;
        width: 62%;
        height: 38px;
        background: #8bb617;
        border-radius: 50% 0 0 45%;
        transform: rotate(-4deg);
    }

    .listing-emoji {
        position: absolute;
        z-index: 2;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0 !important;
    }

    .listing-body {
        flex: 1;
        padding: 25px 27px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .listing-title {
        color: var(--navy);
        font-size: 1.08rem;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 1rem;
    }

    .listing-meta {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 0.9rem;
        font-weight: 800;
        line-height: 1;
    }

    .price-tag {
        color: var(--navy);
        font-weight: 800;
        font-size: 0.98rem;
    }

    /* Card action button */
    .listing-card + div .stButton > button {
        margin-top: -0.2rem;
        border: 1px solid #d9dfe4 !important;
        background: #ffffff !important;
        color: #334155 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        min-height: 38px !important;
        transition: all 0.15s ease-in-out;
    }

    .listing-card + div .stButton > button:hover {
        background: #0f8f83 !important;
        border-color: #0f8f83 !important;
        color: #ffffff !important;
    }

    .listing-card + div .stButton > button:focus,
    .listing-card + div .stButton > button:focus-visible {
        color: #334155 !important;
        border-color: #0f8f83 !important;
        box-shadow: 0 0 0 2px rgba(15, 143, 131, 0.15) !important;
    }

    /* ---------- Marketplace/detail pages ---------- */
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .page-subtitle {
        color: var(--muted);
        margin-bottom: 1.3rem;
    }

    .detail-hero {
        min-height: 310px;
        border-radius: 20px;
        overflow: hidden;
        position: relative;
        background: linear-gradient(to bottom, #cdeefe 0%, #b9e2f7 62%, #d0eb88 62%, #9ac62d 81%, #78a80e 81%, #78a80e 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .detail-emoji {
        font-size: 5rem;
        position: relative;
        z-index: 2;
    }

    .price-panel {
        background: #fff;
        border: 1px solid #edf0f2;
        border-radius: 18px;
        padding: 1.2rem;
        box-shadow: 0 8px 24px rgba(31, 45, 67, 0.08);
    }

    /* ---------- Mobile ---------- */
    @media (max-width: 900px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .welcome-box {
            padding: 22px;
            gap: 18px;
        }

        .avatar-ring {
            width: 82px;
            height: 82px;
            min-width: 82px;
        }

        .welcome-title {
            font-size: 1.55rem;
        }

        .welcome-subtitle {
            font-size: 0.95rem;
        }

        .listing-card {
            min-height: 135px;
        }

        .listing-image {
            min-height: 135px;
        }

        .listing-body {
            padding: 18px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>StudentHive</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-rule'></div>", unsafe_allow_html=True)

    if st.button(
        "Dashboard",
        use_container_width=True,
        type="primary"
        if st.session_state.page == "dashboard" and st.session_state.dashboard_tab == "My Listings"
        else "secondary",
    ):
        st.session_state.dashboard_tab = "My Listings"
        go_to("dashboard")
        st.rerun()

    if st.button("Marketplace", use_container_width=True, type="primary" if st.session_state.page == "marketplace" else "secondary"):
        go_to("marketplace")
        st.rerun()

    if st.button("Gigs", use_container_width=True, type="primary" if st.session_state.page == "dashboard" and st.session_state.dashboard_tab == "Gigs" else "secondary"):
        st.session_state.dashboard_tab = "Gigs"
        go_to("dashboard")
        st.rerun()

    if st.button("Rentals", use_container_width=True, type="primary" if st.session_state.page == "dashboard" and st.session_state.dashboard_tab == "Rentals" else "secondary"):
        st.session_state.dashboard_tab = "Rentals"
        go_to("dashboard")
        st.rerun()

    st.markdown("---")

    st.button("Messages", use_container_width=True, disabled=True)

    st.markdown("<div style='height: 21rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-rule'></div>", unsafe_allow_html=True)
    st.button("Settings", use_container_width=True, disabled=True)


# ---------------------------------------------------------------------------
# Reusable listing card
# ---------------------------------------------------------------------------
def render_listing_card(listing, key_prefix):
    with st.container():
        st.markdown(
            f"""
            <div class="listing-card">
                <div class="listing-image">
                    <div class="listing-emoji">{listing.image_emoji}</div>
                </div>
                <div class="listing-body">
                    <div class="listing-title">{listing.title}</div>
                    <div class="listing-meta">
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

        # Keep the existing navigation logic from the original prototype.
        if st.button("View listing", key=f"{key_prefix}_{listing.id}", use_container_width=True):
            go_to("listing", listing.id)
            st.rerun()


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
def render_dashboard():
    st.markdown(
        """
        <div class="welcome-box">
            <div class="avatar-ring"></div>
            <div>
                <div class="welcome-title">Welcome, User!</div>
                <p class="welcome-subtitle">Here's what's happening in your hive today.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabs = ["My Listings", "Gigs", "Rentals"]

    default_index = (
        tabs.index(st.session_state.dashboard_tab)
        if st.session_state.dashboard_tab in tabs
        else 0
    )

    chosen = st.radio(
        "Dashboard sections",
        tabs,
        index=default_index,
        horizontal=True,
        label_visibility="collapsed",
    )

    st.session_state.dashboard_tab = chosen

    if chosen == "My Listings":
        listings = marketplace.get_listings_by_owner("User")
    elif chosen == "Gigs":
        listings = marketplace.get_listings_by_type("Gig")
    else:
        listings = marketplace.get_listings_by_type("Rental")

    if not listings:
        st.info("Nothing here yet.")
        return

    cols = st.columns(2, gap="large")

    for i, listing in enumerate(listings):
        with cols[i % 2]:
            render_listing_card(listing, key_prefix="dash")


# ---------------------------------------------------------------------------
# Marketplace
# ---------------------------------------------------------------------------
def render_marketplace():
    st.markdown("<div class='page-title'>Marketplace</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>Browse verified Gigs and Rentals across your campus</div>",
        unsafe_allow_html=True,
    )

    filter_choice = st.radio(
        "Filter",
        ["All", "Gig", "Rental"],
        horizontal=True,
        label_visibility="collapsed",
    )

    listings = marketplace.get_all_listings()

    if filter_choice != "All":
        listings = [l for l in listings if l.type_label() == filter_choice]

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(3, gap="large")

    for i, listing in enumerate(listings):
        with cols[i % 3]:
            render_listing_card(listing, key_prefix="mkt")


# ---------------------------------------------------------------------------
# Listing details
# ---------------------------------------------------------------------------
def render_listing_detail():
    listing = marketplace.get_listing_by_id(st.session_state.selected_listing_id)

    if listing is None:
        st.warning("That listing couldn't be found.")
        if st.button("← Back to Marketplace"):
            go_to("marketplace")
            st.rerun()
        return

    st.markdown(
        f"<div style='color:#687282; margin-bottom:0.5rem;'>Marketplace &nbsp;›&nbsp; {listing.title}</div>",
        unsafe_allow_html=True,
    )

    if st.button("← Back"):
        go_to("marketplace")
        st.rerun()

    main_col, side_col = st.columns([3, 1.05], gap="large")

    with main_col:
        st.markdown(
            f"""
            <div class="detail-hero">
                <div class="detail-emoji">{listing.image_emoji}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"## {listing.title}")

        st.markdown(
            f"""
            <span class='badge' style='background-color:{listing.badge_color()};'>
                {listing.type_label()}
            </span>
            """,
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
        st.markdown(
            f"""
            <div class="price-panel">
                <div style="font-size:1.45rem; font-weight:800; color:#1f2d43;">
                    {listing.price_display}
                </div>
                <div style="font-weight:800; color:#1f2d43; margin-top:1rem;">
                    {listing.owner}
                </div>
                <div style="color:#788291; margin-top:0.2rem;">
                    StudentHive member
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Message Owner", use_container_width=True):
            st.toast(f"Message sent to {listing.owner}! (prototype only)")

        if st.button("Request Booking", use_container_width=True, type="primary"):
            st.toast("Booking requested! (prototype only)")


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if st.session_state.page == "dashboard":
    render_dashboard()
elif st.session_state.page == "marketplace":
    render_marketplace()
elif st.session_state.page == "listing":
    render_listing_detail()