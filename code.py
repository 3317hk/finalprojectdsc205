
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏠 Brooklyn House Sales")

# Load the files
df2015 = pd.read_excel("2015_brooklyn.xls", engine="xlrd")
df202526 = pd.read_excel("2025_2026brooklyn.xlsx", engine="openpyxl")

# Clean column names
df2015.columns = df2015.columns.str.strip()
df202526.columns = df202526.columns.str.strip()

# --------------------------------
# HOUSE SALES COMPARISON
# --------------------------------

st.header("1. 🏠 House Sales Comparison")

st.write("Number of houses sold:")

col1, col2 = st.columns(2)

col1.metric("2015", len(df2015))
col2.metric("202526", len(df202526))

# Make sale price numeric
df2015["SALE PRICE"] = pd.to_numeric(
    df2015["SALE PRICE"],
    errors="coerce"
)

df202526["SALE PRICE"] = pd.to_numeric(
    df2016["SALE PRICE"],
    errors="coerce"
)

# Remove zero prices
sales2015 = df2015[df2015["SALE PRICE"] > 0]
sales202526 = df202526[df202526["SALE PRICE"] > 0]

# Average sale price
col1, col2 = st.columns(2)

col1.metric(
    "2015 Average Sale Price",
    f"${sales2015['SALE PRICE'].mean():,.0f}"
)

col2.metric(
    "2025-26 Average Sale Price",
    f"${sales202526['SALE PRICE'].mean():,.0f}"
)

# --------------------------------
# FACTORS AFFECTING SALES
# --------------------------------

st.header("2. 📈 Factors Affecting Sales")

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

# --------------------------------
# YEAR BUILT
# --------------------------------

if choice == "Year Built":

    st.subheader("Year Built vs Sale Price")

    data = df2015[
        ["YEAR BUILT", "SALE PRICE"]
    ].dropna()

    data = data[data["SALE PRICE"] > 0]
    data = data[data["YEAR BUILT"] > 0]

    fig, ax = plt.subplots()

    ax.scatter(
        data["YEAR BUILT"],
        data["SALE PRICE"]
    )

    ax.set_xlabel("Year Built")
    ax.set_ylabel("Sale Price")
    ax.set_title("Year Built vs Sale Price")

    st.pyplot(fig)

# --------------------------------
# GROSS SQUARE FEET
# --------------------------------

if choice == "Gross Square Feet":

    st.subheader("Gross Square Feet vs Sale Price")

    data = df2015[
        ["GROSS SQUARE FEET", "SALE PRICE"]
    ].dropna()

    data = data[data["SALE PRICE"] > 0]
    data = data[data["GROSS SQUARE FEET"] > 0]

    fig, ax = plt.subplots()

    ax.scatter(
        data["GROSS SQUARE FEET"],
        data["SALE PRICE"]
    )

    ax.set_xlabel("Gross Square Feet")
    ax.set_ylabel("Sale Price")
    ax.set_title("Gross Square Feet vs Sale Price")

    st.pyplot(fig)
