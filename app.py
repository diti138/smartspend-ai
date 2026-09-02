import streamlit as st
import pandas as pd

st.set_page_config(page_title="SmartSpend AI", page_icon="💰")

st.title("💰 SmartSpend AI")
st.subheader("Your Intelligent Personal Finance Controller")

# Create session storage for expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Expense input
st.header("➕ Add an Expense")

amount = st.number_input("Enter Amount (₹)", min_value=0.0)

category = st.selectbox(
    "Select Category",
    ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
)

description = st.text_input("Description")

if st.button("Add Expense"):
    if amount > 0:
        st.session_state.expenses.append({
            "Amount": amount,
            "Category": category,
            "Description": description
        })
        st.success("Expense added successfully!")
    else:
        st.warning("Please enter an amount greater than 0.")

# Show expenses
if st.session_state.expenses:
    st.header("📊 Expense Summary")

    df = pd.DataFrame(st.session_state.expenses)

    st.dataframe(df)

    total = df["Amount"].sum()
    st.metric("Total Expenses", f"₹{total:.2f}")

    st.subheader("Category-wise Spending")
    category_data = df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_data)

    # Simple AI-style insights
    st.header("🤖 SmartSpend Insights")

    highest_category = category_data.idxmax()
    highest_amount = category_data.max()

    st.write(
        f"Your highest spending category is **{highest_category}** "
        f"with ₹{highest_amount:.2f}."
    )

    if highest_amount > total * 0.4:
        st.warning(
            f"You are spending a significant portion of your money on "
            f"{highest_category}. Consider reviewing this category."
        )
    else:
        st.success("Your spending appears reasonably balanced!")

else:
    st.info("Add your first expense to see insights!")