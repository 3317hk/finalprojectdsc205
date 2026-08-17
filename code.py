import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🏠 House Sales Analysis")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df1 = pd.read_excel("2015_brooklyn.xls")
df2 = pd.read_excel("2025_2026brooklyn.xlsx")

st.success("Datasets loaded successfully!")

# --------------------------------------------------
# 1. HOUSE SALES COMPARISON
# --------------------------------------------------

st.header("1. 🏠 House Sales Comparison")

# Change this to the actual sales column in your files
sales_column = "Sales"

# Sales data
sales1 = df1[sales_column].dropna()
sales2 = df2[sales_column].dropna()

# Summary statistics
comparison = pd.DataFrame({
    "Statistic": [
        "Number of Houses",
        "Total Sales",
        "Average Sales",
        "Median Sales",
        "Minimum Sales",
        "Maximum Sales"
    ],

    "Dataset 1": [
        len(sales1),
        sales1.sum(),
        sales1.mean(),
        sales1.median(),
        sales1.min(),
        sales1.max()
    ],

    "Dataset 2": [
        len(sales2),
        sales2.sum(),
        sales2.mean(),
        sales2.median(),
        sales2.min(),
        sales2.max()
    ]
})

st.dataframe(comparison)

# --------------------------------------------------
# TOTAL AND AVERAGE SALES
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Dataset 1 Total Sales",
        f"${sales1.sum():,.2f}"
    )

with col2:
    st.metric(
        "Dataset 2 Total Sales",
        f"${sales2.sum():,.2f}"
    )

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Dataset 1 Average Sales",
        f"${sales1.mean():,.2f}"
    )

with col2:
    st.metric(
        "Dataset 2 Average Sales",
        f"${sales2.mean():,.2f}"
    )

# --------------------------------------------------
# SALES DISTRIBUTION
# --------------------------------------------------

st.subheader("Sales Distribution")

fig, ax = plt.subplots(figsize=(10, 5))

sns.histplot(
    sales1,
    kde=True,
    label="Dataset 1",
    alpha=0.5,
    ax=ax
)

sns.histplot(
    sales2,
    kde=True,
    label="Dataset 2",
    alpha=0.5,
    ax=ax
)

ax.set_xlabel("Sales")
ax.set_ylabel("Number of Houses")
ax.set_title("Distribution of House Sales")
ax.legend()

st.pyplot(fig)

# --------------------------------------------------
# BOX PLOT
# --------------------------------------------------

st.subheader("House Sales Comparison")

box_data = pd.DataFrame({
    "Dataset 1": sales1,
    "Dataset 2": sales2
})

fig, ax = plt.subplots(figsize=(8, 5))

sns.boxplot(
    data=box_data,
    ax=ax
)

ax.set_ylabel("Sales")
ax.set_title("House Sales by Dataset")

st.pyplot(fig)


# ==================================================
# 2. FACTORS AFFECTING SALES
# ==================================================

st.header("2. 📈 Factors Affecting Sales")

# Select only numeric columns
numeric_data = df1.select_dtypes(include="number")

# Calculate correlations
correlations = numeric_data.corr()[sales_column]

# Remove sales itself
correlations = correlations.drop(sales_column)

# Sort by absolute correlation
correlations_sorted = correlations.reindex(
    correlations.abs().sort_values(
        ascending=False
    ).index
)

# --------------------------------------------------
# CORRELATION TABLE
# --------------------------------------------------

st.subheader("Correlation With House Sales")

correlation_table = pd.DataFrame({
    "Factor": correlations_sorted.index,
    "Correlation": correlations_sorted.values
})

st.dataframe(
    correlation_table.style.format({
        "Correlation": "{:.3f}"
    })
)

# --------------------------------------------------
# TOP FACTORS
# --------------------------------------------------

st.subheader("Strongest Factors Affecting Sales")

top_factors = correlations_sorted.head(10)

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    x=top_factors.values,
    y=top_factors.index,
    ax=ax
)

ax.set_xlabel("Correlation")
ax.set_ylabel("Factor")
ax.set_title("Factors Associated With House Sales")

st.pyplot(fig)

# --------------------------------------------------
# EXPLORE A FACTOR
# --------------------------------------------------

st.subheader("Explore a Factor")

factors = list(correlations_sorted.index)

selected_factor = st.selectbox(
    "Select a factor to compare with sales:",
    factors
)

fig, ax = plt.subplots(figsize=(9, 6))

sns.scatterplot(
    data=df1,
    x=selected_factor,
    y=sales_column,
    ax=ax
)

ax.set_xlabel(selected_factor)
ax.set_ylabel("Sales")
ax.set_title(
    f"{selected_factor} vs House Sales"
)

st.pyplot(fig)

# --------------------------------------------------
# CORRELATION VALUE
# --------------------------------------------------

selected_correlation = correlations[selected_factor]

st.metric(
    "Correlation",
    f"{selected_correlation:.3f}"
)

# --------------------------------------------------
# INTERPRETATION
# --------------------------------------------------

if selected_correlation > 0.7:

    st.success(
        f"Strong positive relationship. Higher "
        f"{selected_factor} values are associated with "
        f"higher house sales."
    )

elif selected_correlation > 0.3:

    st.info(
        f"Moderate positive relationship between "
        f"{selected_factor} and house sales."
    )

elif selected_correlation < -0.7:

    st.warning(
        f"Strong negative relationship. Higher "
        f"{selected_factor} values are associated with "
        f"lower house sales."
    )

elif selected_correlation < -0.3:

    st.info(
        f"Moderate negative relationship between "
        f"{selected_factor} and house sales."
    )

else:

    st.info(
        f"There is a weak linear relationship between "
        f"{selected_factor} and house sales."
    )

# --------------------------------------------------
# MAIN FINDING
# --------------------------------------------------

st.subheader("Main Finding")

strongest_factor = correlations_sorted.index[0]
strongest_value = correlations_sorted.iloc[0]

st.write(
    f"The factor most strongly associated with house sales "
    f"is **{strongest_factor}**, with a correlation of "
    f"**{strongest_value:.3f}**."
)
