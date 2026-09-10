"""
######### Learning Signature ######### 
Programmed by: Elizabeth Maude M. Lara
Date Submitted: September 10, 2026
 
Program Description: The class for Vendo Kiosk where the processing happens.
Reflection: I practiced using OOP and class and objects in creating this class and functions.
[/] No AI Assistance - Completed independently without AI.
[ ] AI as Support Tool - Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner - Used AI to design, structure, or co-create significant code.
"""

from ClassItems import Item
from ClassTransactions import Transactions

class VendoKiosk:
    def __init__(self, name: str = "Vendo Kiosk"):
        self.name = name
        self.inventory = {
            "Water": Item("Water", 20.0),
            "Soda": Item("Soda", 25.0),
            "Chips": Item("Chips", 30.0)
        }

    def get_item_names(self):
        return list(self.inventory.keys())

    def get_item(self, name: str) -> Item:
        return self.inventory[name]

    def process_transaction(self, item_name: str, payment: float) -> Transactions:
        item = self.get_item(item_name)
        return Transactions(item, payment)