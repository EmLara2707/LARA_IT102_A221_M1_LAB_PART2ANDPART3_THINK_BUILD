from typing import List, Optional
 
from Listing import Listing, Booking
 
 
class Marketplace:
    """Central data holder for listings and bookings."""
 
    def __init__(self) -> None:
        self._listings: List[Listing] = self._build_listings()
        self._gig_bookings: List[Booking] = self._build_bookings()
        self._rental_bookings: List[Booking] = self._build_bookings2()
 
    # ------------------------------------------------------------------
    # Sample data builders
    # ------------------------------------------------------------------
    def _build_listings(self) -> List[Listing]:
        description = [
            "Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum.",
            "Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem "
            "ipsum. Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum "
            "Lorem ipsum. Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum.",
            "Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem "
            "ipsum. Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum.",
        ]
        subjects = ["Subject One", "Subject Two", "Subject Three", "Subject Four"]
        requirements = ["Requirement One", "Requirement Two", "Requirement Three", "Requirement Four"]
 
        return [
            Listing(1, "Advanced Calculus Tutoring", "Gig", 300, "hr",
                    "User", "MMCM", description, subjects, requirements),
            Listing(2, "Dorm Room Mini Fridge Rental", "Rental", 150, "day",
                    "User", "MMCM", description, subjects, requirements),
            Listing(3, "Programming Fundamentals Tutoring", "Gig", 300, "hr",
                    "User", "MMCM", description, subjects, requirements),
            Listing(4, "Graphing Calculator Rental", "Rental", 150, "day",
                    "User", "MMCM", description, subjects, requirements),
            Listing(5, "Essay Editing & Proofreading", "Gig", 300, "hr",
                    "User", "MMCM", description, subjects, requirements),
            Listing(6, "Study Room Speaker Rental", "Rental", 150, "day",
                    "User", "MMCM", description, subjects, requirements),
        ]
 
    def _build_bookings(self) -> List[Booking]:
        slots = [
            "10:00 AM - 12:00 PM, First Last Name",
            "3:00 PM - 5:00 PM, First Last Name",
        ]
        return [Booking("Booked Listing", "Aug 19", slots) for _ in range(3)]

    def _build_bookings2(self) -> List[Booking]:
            slots = [
                "12:00 PM - 3:00 PM, First Last Name",
                "5:00 PM - 8:00 PM, First Last Name",
            ]
            return [Booking("Booked Listing", "Sept 16", slots) for _ in range(3)]
 
    # ------------------------------------------------------------------
    # Listings API
    # ------------------------------------------------------------------
    def get_all_listings(self) -> List[Listing]:
        """All listings shown in the Marketplace tab."""
        return self._listings
 
    def get_my_listings(self) -> List[Listing]:
        """Listings owned by the current user, shown on the Dashboard."""
        return self._listings[:4]
 
    def get_listing_by_id(self, listing_id: int) -> Optional[Listing]:
        for listing in self._listings:
            if listing.id == listing_id:
                return listing
        return None
 
    # ------------------------------------------------------------------
    # Bookings API (separate from "My Listings")
    # ------------------------------------------------------------------
    def get_gig_bookings(self) -> List[Booking]:
        return self._gig_bookings
 
    def get_rental_bookings(self) -> List[Booking]:
        return self._rental_bookings