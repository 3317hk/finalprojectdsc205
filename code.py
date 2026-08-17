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
