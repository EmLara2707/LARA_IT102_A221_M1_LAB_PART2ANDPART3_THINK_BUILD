"""
marketplace.py
--------------
Business logic layer. The Marketplace class owns the collection of Listing
objects and exposes methods to query them. The UI (app.py) never touches
listing storage directly -- it always goes through this class.
 
OOP concepts used:
- Encapsulation: the listing collection (_listings) is private; callers use
  methods like get_all_listings() / get_listing_by_id() instead of reaching
  into the list themselves.
- Composition: Marketplace "has a" collection of Listing objects (Gig/Rental).
"""
 
from Listing import Gig, Rental
 
 
class Marketplace:
    def __init__(self):
        self._listings = []
        self._seed_demo_data()
 
    # ---------------- internal setup ----------------
    def _seed_demo_data(self):
        self.add_listing(Gig(
            title="Advanced Calculus Tutoring",
            description=(
                "One-on-one and small group tutoring for Advanced Calculus, covering everything "
                "from limits to multivariable functions. Sessions are tailored to your course "
                "syllabus and can be held on campus or online.\n\n"
                "I've tutored over 30 students in the past two semesters, with most reporting "
                "improved grades and confidence going into exams. Practice sets and past exam "
                "walkthroughs included in every session.\n\n"
                "Flexible scheduling on weekdays and weekends. Message me to check availability "
                "before booking."
            ),
            price=300,
            owner="User",
            subjects=[
                "Differential Calculus",
                "Integral Calculus",
                "Multivariable Calculus",
                "Series & Sequences",
            ],
            requirements=[
                "Own laptop or tablet",
                "Basic algebra knowledge",
                "Stable internet connection",
                "1-hour minimum booking",
            ],
            image_emoji="📐",
        ))
 
        self.add_listing(Rental(
            title="Scientific Calculator (Casio fx-991)",
            description=(
                "Casio fx-991ES Plus scientific calculator, lightly used and in great condition. "
                "Great for engineering, math, and physics courses. Comes with a hard case and "
                "spare battery.\n\nAvailable for daily rental, perfect for exam week or a quick "
                "borrow between classes."
            ),
            price=150,
            owner="User",
            item_details=[
                "Casio fx-991ES Plus",
                "Includes hard case",
                "Spare battery included",
                "Pickup on campus",
            ],
            requirements=[
                "Valid student ID for pickup",
                "Return within agreed rental period",
                "Replace if lost or damaged",
            ],
            image_emoji="🧮",
        ))
 
        self.add_listing(Gig(
            title="Poster & Slide Deck Design",
            description=(
                "Need a research poster, thesis defense slides, or a clean pitch deck? I design "
                "clear, well-organized visuals using Canva and Figma. Fast turnaround, unlimited "
                "minor revisions within 48 hours of delivery."
            ),
            price=250,
            owner="User",
            subjects=["Poster Design", "Slide Decks", "Infographics", "Branding Basics"],
            requirements=["Content/outline provided by client", "48-hour minimum lead time"],
            image_emoji="🎨",
        ))
 
        self.add_listing(Rental(
            title="Single Room near North Gate",
            description=(
                "Furnished single room in a shared apartment 5 minutes from the North Gate. "
                "Includes bed, study desk, closet, and shared kitchen/bathroom access. Wi-Fi and "
                "utilities included in the daily rate -- great for short stays during exam season "
                "or practicum."
            ),
            price=150,
            owner="User",
            item_details=[
                "Furnished single room",
                "Wi-Fi & utilities included",
                "5 minutes from North Gate",
                "Shared kitchen and bathroom",
            ],
            requirements=[
                "Valid school ID",
                "Minimum 2-night stay",
                "No pets, no smoking",
            ],
            image_emoji="🏠",
        ))
 
    # ---------------- public API ----------------
    def add_listing(self, listing):
        self._listings.append(listing)
 
    def get_all_listings(self):
        return list(self._listings)
 
    def get_listings_by_type(self, type_label):
        return [l for l in self._listings if l.type_label() == type_label]
 
    def get_listings_by_owner(self, owner):
        return [l for l in self._listings if l.owner == owner]
 
    def get_listing_by_id(self, listing_id):
        for l in self._listings:
            if l.id == listing_id:
                return l
        return None