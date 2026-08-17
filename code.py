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


st.subheader("Factors Affecting Sales")

fig, ax = plt.subplots()



ax.set_xlabel("Correlation")
ax.set_ylabel("Factor")
ax.set_title("Factors Affecting House Sales")

st.pyplot(fig)

# --------------------------------
# FACTORS AFFECTING SALES
# --------------------------------

st.header("2. 📈 Factors Affecting Sales")

factor = st.radio(
    "Choose a factor:",
    ["Location", "Neighborhood", "Age of House"],
    horizontal=True
)

# --------------------------------
# LOCATION
# --------------------------------

if factor == "Location":

    st.subheader("📍 Location and House Sales")

    location_sales = (
        df1.groupby("Location")["Sales"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(location_sales)

    st.write(
        "This graph compares the average house sales "
        "for different locations."
    )


# --------------------------------
# NEIGHBORHOOD
# --------------------------------

elif factor == "Neighborhood":

    st.subheader("🏘️ Neighborhood and House Sales")

    neighborhood_sales = (
        df1.groupby("Neighborhood")["Sales"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(neighborhood_sales)

    st.write(
        "This graph compares the average house sales "
        "across different neighborhoods."
    )


# --------------------------------
# AGE OF HOUSE
# --------------------------------

elif factor == "Age of House":

    st.subheader("🏠 Age of House and Sales")

    st.scatter_chart(
        df1,
        x="Age",
        y="Sales"
    )

    correlation = df1["Age"].corr(df1["Sales"])

    st.metric(
        "Correlation between Age and Sales",
        f"{correlation:.3f}"
    )

    if correlation > 0:
        st.write(
            "There is a positive relationship between "
            "house age and sales."
        )
    else:
        st.write(
            "There is a negative relationship between "
            "house age and sales."
        )
