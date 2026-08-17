import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏠 House Sales Analysis")

# Load the two Excel files
df1 = pd.read_excel("2015_brooklyn.xls",engine = "xlrd")
df2 = pd.read_excel("2025_2026brooklyn.xlsx",engine = "openpyxl")

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


    st.bar_chart(neighborhood_sales)

    st.write(
        "This chart shows the average house sale price "
        "for the 15 neighborhoods with the highest average sales."
    )

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏠 Brooklyn House Sales Analysis")

# -----------------------------
# LOAD DATA
# -----------------------------

df1 = pd.read_excel("2015_brooklyn.xls", engine="xlrd")
df2 = pd.read_excel("2016_brooklyn.xlsx", engine="openpyxl")

# Clean column names
df1.columns = df1.columns.astype(str).str.strip().str.upper()
df2.columns = df2.columns.astype(str).str.strip().str.upper()

# -----------------------------
# HOUSE SALES COMPARISON
# -----------------------------

st.header("1. 🏠 House Sales Comparison")

col1, col2 = st.columns(2)

with col1:
    st.metric("2015 Houses", len(df1))

with col2:
    st.metric("2016 Houses", len(df2))

st.subheader("Sales Price Comparison")

# Make SALE PRICE numeric
df1["SALE PRICE"] = pd.to_numeric(
    df1["SALE PRICE"],
    errors="coerce"
)

df2["SALE PRICE"] = pd.to_numeric(
    df2["SALE PRICE"],
    errors="coerce"
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "2015 Average Sale Price",
        f"${df1['SALE PRICE'].mean():,.0f}"
    )

with col2:
    st.metric(
        "2016 Average Sale Price",
        f"${df2['SALE PRICE'].mean():,.0f}"
    )

# -----------------------------
# FACTORS AFFECTING SALES
# -----------------------------

st.header("2. 📈 Factors Affecting Sales")

factor = st.radio(
    "Select a factor:",
    [
        "Neighborhood",
        "Year Built",
        "Gross Square Feet"
    ],
    horizontal=True
)

# -----------------------------
# NEIGHBORHOOD
# -----------------------------

if factor == "Neighborhood":

    st.subheader("🏘️ Neighborhood and Sales")

    neighborhood = (
        df1.groupby("NEIGHBORHOOD")["SALE PRICE"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(neighborhood)

    st.write(
        "This chart shows the average sale price "
        "for the top 10 neighborhoods."
    )

# -----------------------------
# YEAR BUILT
# -----------------------------

elif factor == "Year Built":

    st.subheader("🏠 Year Built and Sales")

    data = df1[
        ["YEAR BUILT", "SALE PRICE"]
    ].dropna()

    data = data[
        (data["YEAR BUILT"] > 0) &
        (data["SALE PRICE"] > 0)
    ]

    fig, ax = plt.subplots()

    ax.scatter(
        data["YEAR BUILT"],
        data["SALE PRICE"]
    )

    ax.set_xlabel("Year Built")
    ax.set_ylabel("Sale Price")
    ax.set_title("Year Built vs Sale Price")

    st.pyplot(fig)

    correlation = data["YEAR BUILT"].corr(
        data["SALE PRICE"]
    )

    st.write(
        f"Correlation: **{correlation:.3f}**"
    )

# -----------------------------
# GROSS SQUARE FEET
# -----------------------------

elif factor == "Gross Square Feet":

    st.subheader("📐 Gross Square Feet and Sales")

    data = df1[
        ["GROSS SQUARE FEET", "SALE PRICE"]
    ].dropna()

    data = data[
        (data["GROSS SQUARE FEET"] > 0) &
        (data["SALE PRICE"] > 0)
    ]

    fig, ax = plt.subplots()

    ax.scatter(
        data["GROSS SQUARE FEET"],
        data["SALE PRICE"]
    )

    ax.set_xlabel("Gross Square Feet")
    ax.set_ylabel("Sale Price")
    ax.set_title("Gross Square Feet vs Sale Price")

    st.pyplot(fig)

    correlation = data["GROSS SQUARE FEET"].corr(
        data["SALE PRICE"]
    )

    st.write(
        f"Correlation: **{correlation:.3f}**"
    )


