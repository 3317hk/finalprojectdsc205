import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("🏠 Brooklyn House Sales Analysis")

# Load data
df2015 = pd.read_excel("2015_brooklyn.xls", engine="xlrd", header=4)
df2025 = pd.read_excel("2025_2026brooklyn.xlsx", engine="openpyxl")


# Clean column names
# Strip spaces, replace newlines, and uppercase column names
df2015.columns = df2015.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip().str.upper()
df2025.columns = df2025.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip().str.upper()

# Ensure numeric data types for plotting (handles commas, spaces, or non-numeric strings)
numeric_cols = ["GROSS SQUARE FEET", "SALE PRICE", "YEAR BUILT"]
for col in numeric_cols:
    if col in df2015.columns:
        df2015[col] = pd.to_numeric(df2015[col], errors="coerce")
    if col in df2025.columns:
        df2025[col] = pd.to_numeric(df2025[col], errors="coerce")

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

ax.scatter(df2015["GROSS SQUARE FEET"], df2015["SALE PRICE"], alpha=0.5)

ax.set_xlabel("Gross Square Feet")
ax.set_ylabel("Sale Price ($)")
ax.set_title("Gross Square Feet vs Sale Price (2015)")

st.pyplot(fig)

# --------------------------------
# YEAR BUILT VS SALE PRICE
# --------------------------------

st.subheader("Year Built vs Sale Price")

fig, ax = plt.subplots()

# Filter out invalid Year Built values (e.g., 0)
df2015_filtered = df2015[df2015["YEAR BUILT"] > 0]

ax.scatter(df2015_filtered["YEAR BUILT"], df2015_filtered["SALE PRICE"], alpha=0.5)

ax.set_xlabel("Year Built")
ax.set_ylabel("Sale Price ($)")
ax.set_title("Year Built vs Sale Price (2015)")

st.pyplot(fig)  # Removed trailing period
choice = st.radio(
    "Choose a factor:",
    ["Neighborhood", "Year Built", "Gross Square Feet"]
)

# --------------------------------
# NEIGHBORHOOD
# --------------------------------

if choice == "Neighborhood":

    st.subheader("Neighborhood vs Sale Price")

    data = df2015.groupby(
        "NEIGHBORHOOD"
    )["SALE PRICE"].mean()

    data = data.sort_values(
        ascending=False
    ).head(10)

    st.bar_chart(data)
if choice == "Year Built":

    st.subheader("Year Built vs Sale Price")

    data = df2015.groupby(
        "YEAR BUILT"), ["SALE PRICE"]
    .mean()
    data = data.sort_values(
        ascending=False
    ).head(10)

    st.bar_chart(data)

if choice == "Gross Square Feet":

    st.subheader("Gross Square Feet vs Sale Price")

    data = df2015[
        ["GROSS SQUARE FEET", "SALE PRICE"]
    ].dropna()
    data = data.sort_values(
        ascending=False
    ).head(10)

    st.bar_chart(data)
