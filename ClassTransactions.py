"""
######### Learning Signature ######### 
Programmed by: Elizabeth Maude M. Lara
Date Submitted: September 10, 2026
 
Program Description: The class transaction of Vendo Kiosk where transactions are processed.
Reflection: I practiced using OOP and class and objects in creating this class and functions.
[/] No AI Assistance - Completed independently without AI.
[ ] AI as Support Tool - Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner - Used AI to design, structure, or co-create significant code.
"""

from ClassItems import Item

class Transactions:
    def __init__ (self, item: Item, payment: float):
        self.item = item
        self.payment = payment

    def is_sufficient(self) -> bool:
        return self.payment >= self.item.price

    def get_change(self) -> float:
        return self.payment - self.item.price