
"""
listing.py
----------
Domain model for StudentHive.
 
OOP concepts used:
- Abstraction: Listing is an abstract base class that can't be instantiated directly.
- Inheritance: Gig and Rental extend Listing and reuse its shared behavior.
- Encapsulation: internal state (like the id counter) is kept "private" (prefixed
  with an underscore) and exposed through properties/methods instead of raw access.
- Polymorphism: each subclass implements type_label() and badge_color() differently,
  so the UI can call the same method on any Listing and get the right result.
"""
 
from abc import ABC, abstractmethod
 
 
class Listing(ABC):
    """Abstract base class for anything that can be posted on StudentHive."""
 
    _id_counter = 1  # shared across all listings, "protected" by convention
 
    def __init__(self, title, description, price, price_unit, owner, image_emoji="🏞️", details=None):
        self._id = Listing._id_counter
        Listing._id_counter += 1
 
        self.title = title
        self.description = description
        self.price = price
        self.price_unit = price_unit
        self.owner = owner
        self.image_emoji = image_emoji
        self.details = details or {}
 
    # ---- Encapsulated read-only access to the id ----
    @property
    def id(self):
        return self._id
 
    # ---- Shared helper available to every subclass ----
    @property
    def price_display(self):
        return f"₱{self.price:,}/{self.price_unit}"
 
    # ---- Must be implemented by every subclass (polymorphism) ----
    @abstractmethod
    def type_label(self):
        """Short label shown on badges, e.g. 'Gig' or 'Rental'."""
        raise NotImplementedError
 
    @abstractmethod
    def badge_color(self):
        """Hex color used for this listing type's badge."""
        raise NotImplementedError
 
    def short_summary(self):
        return f"{self.title} · {self.price_display}"
 
    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} title={self.title!r}>"
 
 
class Gig(Listing):
    """A service a student offers, billed hourly (tutoring, design work, etc.)."""
 
    def __init__(self, title, description, price, owner, subjects=None, requirements=None, image_emoji="📚"):
        details = {
            "Subjects Covered": subjects or [],
            "Requirements": requirements or [],
        }
        super().__init__(title, description, price, "hr", owner, image_emoji, details)
 
    def type_label(self):
        return "Gig"
 
    def badge_color(self):
        return "#0f766e"  # teal
 
 
class Rental(Listing):
    """A physical item or space a student rents out, billed daily."""
 
    def __init__(self, title, description, price, owner, item_details=None, requirements=None, image_emoji="🏠"):
        details = {
            "Item Details": item_details or [],
            "Requirements": requirements or [],
        }
        super().__init__(title, description, price, "day", owner, image_emoji, details)
 
    def type_label(self):
        return "Rental"
 
    def badge_color(self):
        return "#f59e0b"  # amber