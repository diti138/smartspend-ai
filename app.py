import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(page_title="SmartSpend AI", page_icon="💰")

st.title("💰 SmartSpend AI")
st.subheader("Your AI-Powered Personal Finance Controller")

# Gemini AI setup
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
# Session storage
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Add expense
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


# Expense dashboard
if st.session_state.expenses:

    st.header("📊 Expense Summary")

    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df)

    # Delete expense
    st.subheader("🗑️ Delete an Expense")

    expense_options = [
        f"{i + 1}. ₹{expense['Amount']} - {expense['Category']} - {expense['Description']}"
        for i, expense in enumerate(st.session_state.expenses)
    ]

    selected_expense = st.selectbox(
        "Select an expense to delete",
        range(len(expense_options)),
        format_func=lambda x: expense_options[x]
    )

    if st.button("Delete Selected Expense"):
        st.session_state.expenses.pop(selected_expense)
        st.success("Expense deleted successfully!")
        st.rerun()

    # Analysis
    df = pd.DataFrame(st.session_state.expenses)

    if not df.empty:
                # AI Budget Planner
        st.header("🎯 AI Budget Planner")

        monthly_budget = st.number_input(
            "Enter your monthly budget (₹)",
            min_value=0.0,
            step=500.0
        )

        if st.button("Generate AI Budget Plan"):

            if monthly_budget <= 0:
                st.warning("Please enter a monthly budget greater than ₹0.")

            else:
                expense_summary = df.to_string(index=False)

                planner_prompt = f"""
You are SmartSpend AI, an intelligent personal budget planner.

The user's monthly budget is ₹{monthly_budget}.

Their current expense data is:
{expense_summary}

Create a personalized monthly budget plan.

Include:
1. A suggested category-wise budget.
2. A suggested savings amount.
3. A comparison with the user's current spending pattern.
4. Two practical and realistic money-management suggestions.

Keep the response concise and easy to understand.
Do not provide investment advice or guarantee financial outcomes.
"""
                

                try:
                    with st.spinner("SmartSpend AI is creating your budget plan..."):
                        response = client.models.generate_content(
                            model="gemini-3.7-flash",
                            contents=planner_prompt
                        )

                    st.success("Your AI Budget Plan is ready!")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Unable to generate budget plan: {e}")
                            # AI Savings Challenge
        st.header("🏆 AI Savings Challenge")

        st.write(
            "Get a personalized 7-day savings challenge based on your spending habits."
        )

        if st.button("Generate My Savings Challenge"):

            expense_summary = df.to_string(index=False)
            total_expenses = df["Amount"].sum()

            challenge_prompt = f"""
You are SmartSpend AI, a helpful personal finance habit coach.

Analyze the user's expense data below:

{expense_summary}

Their total recorded expenses are ₹{total_expenses:.2f}.

Create a personalized and realistic 7-Day Savings Challenge.

Include:

Day 1 through Day 7:
Give one simple and practical saving challenge for each day.

Also include:
1. A realistic savings goal for the 7 days.
2. The spending category the user should pay the most attention to.
3. A short motivational message.

Keep the challenge practical, positive, beginner-friendly, and easy to follow.
Do not provide investment advice or make guarantees about savings.
"""

            try:
                max_retries = 3
                response = None

                for attempt in range(max_retries):
                    try:
                        with st.spinner(
                            f"Creating your personalized challenge... "
                            f"(Attempt {attempt + 1}/{max_retries})"
                        ):
                            response = client.models.generate_content(
                                model="gemini-3.7-flash",
                                contents=challenge_prompt
                            )

                        break

                    except Exception as e:
                        error_message = str(e)

                        if (
                            "503" in error_message
                            and attempt < max_retries - 1
                        ):
                            delay = 5 * (2 ** attempt)

                            st.warning(
                                f"AI service is busy. Retrying in "
                                f"{delay} seconds..."
                            )

                            time.sleep(delay)

                        else:
                            raise e

                if response:
                    st.success(
                        "🎉 Your personalized 7-Day Savings Challenge is ready!"
                    )
                    st.write(response.text)

            except Exception as e:
                st.error(
                    f"Unable to generate Savings Challenge: {e}"
                )


        total = df["Amount"].sum()

        st.metric("Total Expenses", f"₹{total:.2f}")

        st.subheader("Category-wise Spending")

        category_data = df.groupby("Category")["Amount"].sum()
        st.bar_chart(category_data)

        # Basic automated insight
        highest_category = category_data.idxmax()
        highest_amount = category_data.max()

        st.header("📈 Spending Insight")

        st.write(
            f"Your highest spending category is **{highest_category}** "
            f"with ₹{highest_amount:.2f}."
        )

        # Actual Gemini AI feature
        st.header("🤖 AI Financial Advisor")

        if st.button("Get AI Financial Advice"):

            if client is None:
                st.error("Gemini API key is not configured correctly.")
            else:
                expense_summary = df.to_string(index=False)

                prompt = f"""
You are SmartSpend AI, a helpful personal finance assistant.

Analyze the following expense data:

{expense_summary}

Give the user:
1. A short summary of their spending.
2. Their highest spending area.
3. Two practical suggestions to improve spending habits.

Keep the response concise, supportive, and easy to understand.
Do not provide professional financial or investment advice.
"""

                try:
                    with st.spinner("SmartSpend AI is analyzing your expenses..."):
                        response = client.models.generate_content(
                            model="gemini-3.7-flash",
                            contents=prompt
                        )

                    st.success("AI Analysis Complete!")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Error: {e}")

else:
    st.info("Add your first expense to see your financial dashboard and AI insights!")
