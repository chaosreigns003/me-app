import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retirement Planner", layout="centered")

st.title("🏖️ Retirement Planner Simulator")

# User Inputs
st.sidebar.header("👤 Personal Details")
current_age = st.sidebar.slider("Current Age", 20, 60, 30)
retirement_age = st.sidebar.slider("Retirement Age", current_age+1, 80, 60)
life_expectancy = st.sidebar.slider("Life Expectancy", retirement_age+1, 100, 85)

st.sidebar.header("💸 Financial Details")
current_expenses = st.sidebar.number_input("Current Monthly Expenses (₹)", 1000, 1000000, 50000, step=1000)
inflation_rate = st.sidebar.slider("Expected Inflation Rate (p.a.)", 0.0, 15.0, 6.0, step=0.1) / 100
pre_retirement_return = st.sidebar.slider("Return on Investments (before retirement)", 0.0, 20.0, 10.0, step=0.1) / 100
post_retirement_return = st.sidebar.slider("Return on Investments (after retirement)", 0.0, 20.0, 7.0, step=0.1) / 100

# Computations
years_to_retirement = retirement_age - current_age
years_post_retirement = life_expectancy - retirement_age

# Adjust expenses for inflation
future_monthly_expense = current_expenses * ((1 + inflation_rate) ** years_to_retirement)
future_annual_expense = future_monthly_expense * 12

# Calculate required retirement corpus using Present Value of Annuity Formula
def calculate_retirement_corpus():
    r = post_retirement_return
    n = years_post_retirement
    corpus = future_annual_expense * ((1 - (1 + r) ** -n) / r)
    return corpus

# Estimate corpus accumulation until retirement
def accumulate_corpus_annual(corpus_needed):
    corpus = []
    yearly_investment = corpus_needed / (((1 + pre_retirement_return) ** years_to_retirement - 1) / pre_retirement_return)
    value = 0
    for i in range(1, years_to_retirement + 1):
        value = value * (1 + pre_retirement_return) + yearly_investment
        corpus.append(value)
    return corpus, yearly_investment

required_corpus = calculate_retirement_corpus()
accum_corpus, yearly_investment = accumulate_corpus_annual(required_corpus)

# Display Results
st.subheader("🧾 Summary")
st.write(f"Years to Retirement: **{years_to_retirement} years**")
st.write(f"Monthly Expense at Retirement: **₹{future_monthly_expense:,.0f}**")
st.write(f"Required Retirement Corpus: **₹{required_corpus:,.0f}**")
st.write(f"Suggested Annual Investment: **₹{yearly_investment:,.0f}**")

# Plot Corpus Growth
fig, ax = plt.subplots()
years = np.arange(current_age + 1, retirement_age + 1)
ax.plot(years, accum_corpus, color='green', linewidth=2)
ax.set_title("Corpus Growth Until Retirement")
ax.set_xlabel("Age")
ax.set_ylabel("Corpus (₹)")
ax.grid(True)
st.pyplot(fig)

# Post-retirement corpus drawdown
corpus_left = [required_corpus]
for _ in range(years_post_retirement):
    corpus_left.append(corpus_left[-1] * (1 + post_retirement_return) - future_annual_expense)

fig2, ax2 = plt.subplots()
years_post = np.arange(retirement_age, life_expectancy + 1)
ax2.plot(years_post, corpus_left, color='red', linewidth=2)
ax2.set_title("Post-Retirement Corpus Drawdown")
ax2.set_xlabel("Age")
ax2.set_ylabel("Corpus (₹)")
ax2.grid(True)
st.pyplot(fig2)
