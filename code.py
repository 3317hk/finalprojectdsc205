import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏠 House Sales Analysis")

# Load the two Excel files
df1 = pd.read_excel("2015_brooklyn.xls")
df2 = pd.read_excel("2025_2026brooklyn.xlsx")

# -----------------------------------
# HOUSE SALES COMPARISON
# -----------------------------------

st.header("1. 🏠 House Sales Comparison")

st.write("2015 Data")
st.dataframe(df1.head())

st.write("2025-2026 Data")
st.dataframe(df2.head())

# Show number of sales
st.subheader("Number of Houses Sold")

col1, col2 = st.columns(2)

with col1:
    st.metric("2015", len(df1))

with col2:
    st.metric("2025-2026", len(df2))

# --------------------------------
# FACTORS AFFECTING SALES
# --------------------------------

st.header("2. 📈 Factors Affecting Sales")

factor = st.radio(
    "Choose a factor:",
    ["Neighborhood", "Year Built", "Gross Square Feet"],
    horizontal=True
)

# --------------------------------
# NEIGHBORHOOD
# --------------------------------

if factor == "Neighborhood":

    st.subheader("🏘️ Neighborhood vs House Sales")

    neighborhood_sales = (
        df1.groupby("NEIGHBORHOOD")("SALE PRICE").mean().sort_values(ascending=False).head(15)
    )

    st.bar_chart(neighborhood_sales)

    st.write(
        "This chart shows the average house sale price "
        "for the 15 neighborhoods with the highest average sales."
    )


# --------------------------------
# YEAR BUILT
# --------------------------------

elif factor == "Year Built":

    st.subheader("🏠 Year Built vs House Sales")

    year_data = df1[
        ["YEAR BUILT", "SALE PRICE"]
    ].dropna()

    year_data = year_data[
        year_data["YEAR BUILT"] > 0
    ]

    st.scatter_chart(
        year_data,
        x="YEAR BUILT",
        y="SALE PRICE"
    )

    correlation = year_data[
        "YEAR BUILT"
    ].corr(
        year_data["SALE PRICE"]
    )

    st.metric(
        "Correlation",
        f"{correlation:.3f}"
    )


# --------------------------------
# GROSS SQUARE FEET
# --------------------------------

elif factor == "Gross Square Feet":

    st.subheader("📐 Gross Square Feet vs House Sales")

    sqft_data = df1[
        ["GROSS SQUARE FEET", "SALE PRICE"]
    ].dropna()

    sqft_data = sqft_data[
        (sqft_data["GROSS SQUARE FEET"] > 0) &
        (sqft_data["SALE PRICE"] > 0)
    ]

    st.scatter_chart(
        sqft_data,
        x="GROSS SQUARE FEET",
        y="SALE PRICE"
    )

    correlation = sqft_data[
        "GROSS SQUARE FEET"
    ].corr(
        sqft_data["SALE PRICE"]
    )

    st.metric(
        "Correlation",
        f"{correlation:.3f}"
    )
