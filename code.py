import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏠 Brooklyn House Sales Analysis")

# Load data
df2015 = pd.read_excel("2015_brooklyn.xls", engine="xlrd")
df2025 = pd.read_excel("2025_2026brooklyn.xlsx", engine="openpyxl")

# Clean column names
df2015.columns = df2015.columns.str.strip().str.upper()
df2025.columns = df2025.columns.str.strip().str.upper()

# --------------------------------
# HOUSE SALES COMPARISON
# --------------------------------

st.header("1. 🏠 House Sales Comparison")

st.write("Number of houses in each year:")

col1, col2 = st.columns(2)

col1.metric("2015", len(df2015))
col2.metric("2025", len(df2025))

# --------------------------------
# GROSS SQUARE FEET VS SALE PRICE
# --------------------------------

st.header("2. 📈 Factors Affecting Sales")

st.subheader("Gross Square Feet vs Sale Price")



fig, ax = plt.subplots()

ax.scatter(
    df2015["GROSS SQUARE FEET"],
    df2015["SALE PRICE"]
)

ax.set_xlabel("Gross Square Feet")
ax.set_ylabel("Sale Price ($)")
ax.set_title("Gross Square Feet vs Sale Price")

st.pyplot(fig)

# --------------------------------
# YEAR BUILT VS SALE PRICE
# --------------------------------

st.subheader("Year Built vs Sale Price")


fig, ax = plt.subplots()

ax.scatter(
    df["YEAR BUILT"],
    df["SALE PRICE"]
)

ax.set_xlabel("Year Built")
ax.set_ylabel("Sale Price ($)")
ax.set_title("Year Built vs Sale Price")

st.pyplot(fig)
