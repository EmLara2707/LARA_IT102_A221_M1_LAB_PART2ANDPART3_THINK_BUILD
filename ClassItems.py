"""
######### Learning Signature ######### 
Programmed by: Elizabeth Maude M. Lara
Date Submitted: September 10, 2026
 
Program Description: The class items of Vendo Kiosk where items will be stored.
Reflection: I practiced using OOP and class and objects in creating this class and functions.
[/] No AI Assistance - Completed independently without AI.
[ ] AI as Support Tool - Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner - Used AI to design, structure, or co-create significant code.
"""

class Item:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def items(self):
        return f"{self.name} (₱{self.price:.2f})"