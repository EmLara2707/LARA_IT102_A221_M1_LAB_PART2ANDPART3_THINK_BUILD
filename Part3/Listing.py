from dataclasses import dataclass, field
from typing import List, Optional, Callable
 
import streamlit as st
 
 
@dataclass
class Listing:
    """A single Gig or Rental posted on StudentHive."""
 
    id: int
    title: str
    category: str          # "Gig" or "Rental"
    price: float
    unit: str               # "hr" or "day"
    owner: str
    course: str
    description: List[str] = field(default_factory=list)
    subjects: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
 
    @property
    def price_label(self) -> str:
        """Formatted price, e.g. '₱300/hr'."""
        return f"\u20b1{self.price:.0f}/{self.unit}"
 
    def render_placeholder_image(self, height: int = 160) -> None:
        """A simple stand-in for a real listing photo (no custom colors)."""
        with st.container(border=True):
            st.markdown(
                f"<div style='height:{height}px; display:flex; "
                f"align-items:center; justify-content:center; font-size:2.5rem;'>"
                f"\U0001F3DE\uFE0F</div>",
                unsafe_allow_html=True,
            )
 
    def render_card(self, on_view: Optional[Callable[[int], None]] = None,
                     key_prefix: str = "listing") -> None:
        """Full card used in the Marketplace grid, with a 'View' action."""
        with st.container(border=True):
            st.caption(self.category)
            self.render_placeholder_image()
            st.markdown(f"**{self.title}**")
            st.caption(self.price_label)
            st.write(f"{self.owner} \u00b7 {self.course}")
            if on_view is not None:
                clicked = st.button(
                    "View",
                    key=f"{key_prefix}_view_{self.id}",
                    use_container_width=True,
                )
                if clicked:
                    on_view(self.id)
 
    def render_mini_card(self) -> None:
        """Compact card used in the Dashboard's 'My Listings' tab."""
        with st.container(border=True):
            self.render_placeholder_image(height=120)
            st.write(f"**{self.title}**")
            st.caption(f"{self.category} \u00b7 {self.price_label}")
 
    def render_detail(self) -> None:
        """Full detail body used on the Listing Detail page (main column)."""
        self.render_placeholder_image(height=280)
        st.title(self.title)
        st.divider()
        st.subheader(f"About this {self.category}")
        for paragraph in self.description:
            st.write(paragraph)
 
        subjects_col, requirements_col = st.columns(2)
        with subjects_col:
            with st.container(border=True):
                st.markdown("**Subjects Covered**")
                for subject in self.subjects:
                    st.write(f"- {subject}")
        with requirements_col:
            with st.container(border=True):
                st.markdown("**Requirements**")
                for requirement in self.requirements:
                    st.write(f"- {requirement}")
 
    def render_side_panel(self) -> None:
        """Price / owner / actions panel used on the Listing Detail page."""
        with st.container(border=True):
            st.subheader(self.price_label)
            st.write(f"**{self.owner}**")
            st.caption(f"Course, {self.course}")
            st.button("Message Owner", use_container_width=True, disabled=True,
                       key=f"message_owner_{self.id}")
            st.button("Request Booking", use_container_width=True, disabled=True,
                       key=f"request_booking_{self.id}")
 
 
@dataclass
class Booking:
    """A booking record shown on the Dashboard's Gigs/Rentals tabs."""
 
    listing_title: str
    date: str
    slots: List[str] = field(default_factory=list)
 
    def render(self, key_suffix: str = "") -> None:
        """Render this booking as a row card."""
        with st.container(border=True):
            image_col, info_col, date_col = st.columns([1, 3, 1])
            with image_col:
                st.markdown("\U0001F3DE\uFE0F")
            with info_col:
                st.write(f"**{self.listing_title}**")
                for slot in self.slots:
                    st.caption(slot)
            with date_col:
                st.button(
                    self.date,
                    key=f"booking_{key_suffix}",
                    disabled=True,
                    use_container_width=True,
                )