"""
######### Learning Signature ######### 
Programmed by: Elizabeth Maude M. Lara
Date Submitted: September 10, 2026
 
Program Description: The Streamlit UI of Vendo Kiosk.
Reflection: I practiced using OOP in creating this program and also using classes and objects while also practicing how to use streamlit for the GUI.
[/] No AI Assistance - Completed independently without AI.
[ ] AI as Support Tool - Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner - Used AI to design, structure, or co-create significant code.
"""

import streamlit as st
from ClassItems import Item
from ClassTransactions import Transactions
from ClassVendoKiosk import VendoKiosk

st.set_page_config(page_title="Vendo Kiosk", page_icon="🥤", layout="centered")

if "kiosk" not in st.session_state:
    st.session_state.kiosk = VendoKiosk()

kiosk = st.session_state.kiosk

st.title(f"🥤 {kiosk.name}")
st.write("Select an item, enter your payment, and get your change.")

st.divider()

st.subheader("Available Items")
cols = st.columns(len(kiosk.get_item_names()))
for col, name in zip(cols, kiosk.get_item_names()):
    item = kiosk.get_item(name)
    with col:
        st.metric(label=item.name, value=f"₱{item.price:.2f}")

st.divider()

st.subheader("Make a Purchase")
selected_name = st.selectbox("Select an item:", kiosk.get_item_names())
selected_item = kiosk.get_item(selected_name)
 
st.write(f"Price: **₱{selected_item.price:.2f}**")
 
payment = st.number_input(
    "Enter payment amount (₱):",
    min_value=0.0,
    step=1.0,
    format="%.2f",
)
 
if st.button("Buy", type="primary"):
    transaction = kiosk.process_transaction(selected_name, payment)
 
    st.write("---")
    st.write(f"**Selected Item:** {selected_item.name}")
    st.write(f"**Price:** ₱{selected_item.price:.2f}")
    st.write(f"**Payment:** ₱{payment:.2f}")
 
    if transaction.is_sufficient():
        change = transaction.get_change()
        st.success(f"✅ Dispensing {selected_item.name}. Your change is ₱{change:.2f}")
    else:
        st.error("❌ Insufficient payment.")