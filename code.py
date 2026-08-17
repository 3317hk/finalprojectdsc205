import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏠 House Sales Analysis")

# Load the two Excel files
df1 = pd.read_excel("2015_brooklyn.xls")


# -----------------------------------
# HOUSE SALES COMPARISON
# -----------------------------------

st.header("1. 🏠 House Sales Comparison")

st.write("2015 Data")
st.dataframe(df1.head())

st.write("2016 Data")
st.dataframe(df2.head())

# Show number of sales
st.subheader("Number of Houses Sold")

col1, col2 = st.columns(2)

with col1:
    st.metric("2015", len(df1))

with col2:
    st.metric("2016", len(df2))


# -----------------------------------
# FIND SALES COLUMN
# -----------------------------------

st.header("2. 📈 Factors Affecting Sales")

st.write("Columns in the dataset:")

st.write(df1.columns.tolist())

# Select the sales column
sales_column = st.selectbox(
    "Select the sales column:",
    df1.select_dtypes(include="number").columns
)

# -----------------------------------
# CORRELATION
# -----------------------------------

correlation = df1.select_dtypes(
    include="number"
).corr()[sales_column]

correlation = correlation.drop(sales_column)

st.subheader("Factors Related to Sales")

st.dataframe(
    correlation.sort_values(
        ascending=False
    )
)

# -----------------------------------
# BAR CHART
# -----------------------------------

st.subheader("Factors Affecting Sales")

fig, ax = plt.subplots()

correlation.sort_values().plot.barh(ax=ax)

ax.set_xlabel("Correlation")
ax.set_ylabel("Factor")
ax.set_title("Factors Affecting House Sales")

st.pyplot(fig)
