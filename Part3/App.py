import streamlit as st
 
from Marketplace import Marketplace
 
st.set_page_config(page_title="StudentHive", layout="wide")
 
 
# ----------------------------------------------------------------------
# App state & data
# ----------------------------------------------------------------------
def init_state() -> None:
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "selected_listing_id" not in st.session_state:
        st.session_state.selected_listing_id = None
 
 
@st.cache_resource
def get_marketplace() -> Marketplace:
    """Cached so sample data is built once per app session, not every rerun."""
    return Marketplace()
 
 
def go_to(page: str, listing_id: int = None) -> None:
    """Update navigation state and immediately rerun so the new page shows."""
    st.session_state.page = page
    if listing_id is not None:
        st.session_state.selected_listing_id = listing_id
    st.rerun()
 
 
# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## StudentHive")
        st.divider()
 
        current_page = st.session_state.page
 
        if st.button("Dashboard", use_container_width=True,
                      type="primary" if current_page == "dashboard" else "secondary"):
            go_to("dashboard")
 
        if st.button("Marketplace", use_container_width=True,
                      type="primary" if current_page == "marketplace" else "secondary"):
            go_to("marketplace")
 
        # Placeholder-only entries: present for layout, not wired up.
        st.button("Gigs", use_container_width=True, disabled=True, key="sidebar_gigs")
        st.button("Rentals", use_container_width=True, disabled=True, key="sidebar_rentals")
        st.button("Messages", use_container_width=True, disabled=True, key="sidebar_messages")
 
        st.divider()
        st.button("Settings", use_container_width=True, disabled=True, key="sidebar_settings")
 
 
# ----------------------------------------------------------------------
# Dashboard page
# ----------------------------------------------------------------------
def render_dashboard(marketplace: Marketplace) -> None:
    with st.container(border=True):
        avatar_col, text_col = st.columns([1, 8])
        with avatar_col:
            with st.container(border=True):
                st.markdown(
                    "<div style='text-align:center; font-size:1.6rem;'>\U0001F642</div>",
                    unsafe_allow_html=True,
                )
        with text_col:
            st.subheader("Welcome, User!")
            st.write("Here's what's happening in your hive today.")
 
    tab_listings, tab_gigs, tab_rentals = st.tabs(["My Listings", "Gigs", "Rentals"])
 
    with tab_listings:
        render_my_listings_tab(marketplace)
 
    with tab_gigs:
        render_bookings_tab(marketplace.get_gig_bookings(), suffix="gigs")
 
    with tab_rentals:
        render_bookings_tab(marketplace.get_rental_bookings(), suffix="rentals")
 
 
def render_my_listings_tab(marketplace: Marketplace) -> None:
    """'My Listings' tab: the user's own posted listings (separate from bookings)."""
    listings = marketplace.get_my_listings()
    columns = st.columns(2)
    for index, listing in enumerate(listings):
        with columns[index % 2]:
            listing.render_mini_card()
 
 
def render_bookings_tab(bookings, suffix: str) -> None:
    """Shared layout for the Gigs and Rentals tabs (booking cards, not listings)."""
    upcoming_col, all_col = st.columns(2)
    with upcoming_col:
        st.subheader("Upcoming Bookings")
        for index, booking in enumerate(bookings):
            booking.render(key_suffix=f"{suffix}_upcoming_{index}")
    with all_col:
        st.subheader("Bookings")
        for index, booking in enumerate(bookings):
            booking.render(key_suffix=f"{suffix}_all_{index}")
 
 
# ----------------------------------------------------------------------
# Marketplace page
# ----------------------------------------------------------------------
def render_marketplace(marketplace: Marketplace) -> None:
    st.title("Marketplace")
    st.caption("Browse verified Gigs and Rentals across your campus")
 
    listings = marketplace.get_all_listings()
    columns = st.columns(3)
    for index, listing in enumerate(listings):
        with columns[index % 3]:
            listing.render_card(on_view=lambda listing_id: go_to("listing_detail", listing_id))
 
 
# ----------------------------------------------------------------------
# Listing detail page
# ----------------------------------------------------------------------
def render_listing_detail(marketplace: Marketplace) -> None:
    listing = marketplace.get_listing_by_id(st.session_state.selected_listing_id)
 
    if st.button("\u2190 Back to Marketplace"):
        go_to("marketplace")
 
    if listing is None:
        st.warning("This listing could not be found.")
        return
 
    st.caption(f"Marketplace  >  {listing.title}")
 
    main_col, side_col = st.columns([3, 1])
    with main_col:
        listing.render_detail()
    with side_col:
        listing.render_side_panel()
 
 
# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main() -> None:
    init_state()
    marketplace = get_marketplace()
 
    render_sidebar()
 
    page = st.session_state.page
    if page == "marketplace":
        render_marketplace(marketplace)
    elif page == "listing_detail":
        render_listing_detail(marketplace)
    else:
        render_dashboard(marketplace)
 
 
if __name__ == "__main__":
    main()