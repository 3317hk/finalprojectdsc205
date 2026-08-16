import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="House Sales Analysis",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 House Sales Analysis")
st.write(
    "This application compares two house-sales datasets "
    "and examines the factors associated with house sales."
)

# --------------------------------------------------
# LOAD DATA FROM GITHUB
# --------------------------------------------------

file1_url = "https://raw.githubusercontent.com/3317hk/finalprojectdsc205/main/2015_brooklyn.xlsx"
file2_url = "https://raw.githubusercontent.com/3317hk/finalprojectdsc205/main/2025_2026brooklyn.xlsx"

df1 = pd.read_excel(file1_url)
df2 = pd.read_excel(file2_url)

# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------

st.header("1. Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dataset 1")
    st.write(f"Number of houses: {len(df1)}")
    st.dataframe(df1.head())

with col2:
    st.subheader("Dataset 2")
    st.write(f"Number of houses: {len(df2)}")
    st.dataframe(df2.head())

# --------------------------------------------------
# FIND COMMON NUMERIC VARIABLES
# --------------------------------------------------

common_columns = list(
    set(df1.columns).intersection(df2.columns)
)

numeric_columns = []

for column in common_columns:
    if (
        pd.api.types.is_numeric_dtype(df1[column])
        and pd.api.types.is_numeric_dtype(df2[column])
    ):
        numeric_columns.append(column)

st.header("2. Variables Available for Analysis")

st.write(numeric_columns)

# --------------------------------------------------
# SELECT SALES COLUMN
# --------------------------------------------------

sales_column = st.selectbox(
    "Select the sales variable:",
    numeric_columns
)

# --------------------------------------------------
# SALES SUMMARY
# --------------------------------------------------

st.header("3. House Sales Comparison")

sales1 = df1[sales_column].dropna()
sales2 = df2[sales_column].dropna()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Dataset 1 Total Sales",
        f"{sales1.sum():,.2f}"
    )

with col2:
    st.metric(
        "Dataset 2 Total Sales",
        f"{sales2.sum():,.2f}"
    )

with col3:
    st.metric(
        "Dataset 1 Average",
        f"{sales1.mean():,.2f}"
    )

with col4:
    st.metric(
        "Dataset 2 Average",
        f"{sales2.mean():,.2f}"
    )

# --------------------------------------------------
# ADDITIONAL STATISTICS
# --------------------------------------------------

summary = pd.DataFrame({
    "Statistic": [
        "Number of Houses",
        "Total Sales",
        "Average Sales",
        "Median Sales",
        "Minimum Sales",
        "Maximum Sales",
        "Standard Deviation"
    ],

    "Dataset 1": [
        len(sales1),
        sales1.sum(),
        sales1.mean(),
        sales1.median(),
        sales1.min(),
        sales1.max(),
        sales1.std()
    ],

    "Dataset 2": [
        len(sales2),
        sales2.sum(),
        sales2.mean(),
        sales2.median(),
        sales2.min(),
        sales2.max(),
        sales2.std()
    ]
})

st.subheader("Sales Statistics")

st.dataframe(
    summary.style.format({
        "Dataset 1": "{:,.2f}",
        "Dataset 2": "{:,.2f}"
    })
)

# --------------------------------------------------
# SALES DISTRIBUTION
# --------------------------------------------------

st.header("4. Sales Distribution")

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

ax.set_xlabel(sales_column)
ax.set_ylabel("Number of Houses")
ax.set_title("Distribution of House Sales")
ax.legend()

st.pyplot(fig)

# --------------------------------------------------
# BOX PLOT
# --------------------------------------------------

st.header("5. Compare House Sales")

sales_comparison = pd.DataFrame({
    "Dataset 1": sales1,
    "Dataset 2": sales2
})

fig, ax = plt.subplots(figsize=(8, 5))

sns.boxplot(
    data=sales_comparison,
    ax=ax
)

ax.set_ylabel(sales_column)
ax.set_title("House Sales Comparison")

st.pyplot(fig)

# --------------------------------------------------
# CORRELATION ANALYSIS
# --------------------------------------------------

st.header("6. What Factors Impact House Sales?")

numeric_df = df1.select_dtypes(include="number")

correlation = numeric_df.corr()[sales_column].sort_values(
    ascending=False
)

correlation = correlation.drop(sales_column)

correlation_table = pd.DataFrame({
    "Variable": correlation.index,
    "Correlation": correlation.values
})

st.subheader("Correlation With House Sales")

st.dataframe(
    correlation_table.style.format({
        "Correlation": "{:.3f}"
    })
)

# --------------------------------------------------
# CORRELATION VISUALIZATION
# --------------------------------------------------

st.subheader("Strongest Factors Associated With Sales")

top_factors = (
    correlation
    .abs()
    .sort_values(ascending=False)
    .head(10)
)

top_factors_names = top_factors.index

plot_data = correlation.loc[top_factors_names].sort_values()

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    x=plot_data.values,
    y=plot_data.index,
    ax=ax
)

ax.set_xlabel("Correlation")
ax.set_ylabel("Variable")
ax.set_title("Variables Associated With House Sales")

st.pyplot(fig)

# --------------------------------------------------
# SELECT A FACTOR
# --------------------------------------------------

st.header("7. Explore Individual Factors")

factors = [
    column for column in numeric_columns
    if column != sales_column
]

selected_factor = st.selectbox(
    "Select a factor:",
    factors
)

fig, ax = plt.subplots(figsize=(9, 6))

sns.scatterplot(
    data=df1,
    x=selected_factor,
    y=sales_column,
    ax=ax
)

ax.set_title(
    f"{selected_factor} vs. {sales_column}"
)

ax.set_xlabel(selected_factor)
ax.set_ylabel(sales_column)

st.pyplot(fig)

# --------------------------------------------------
# CORRELATION FOR SELECTED FACTOR
# --------------------------------------------------

selected_correlation = df1[
    [selected_factor, sales_column]
].corr().iloc[0, 1]

st.metric(
    f"Correlation: {selected_factor} vs {sales_column}",
    f"{selected_correlation:.3f}"
)

# --------------------------------------------------
# AUTOMATIC INTERPRETATION
# --------------------------------------------------

st.subheader("Interpretation")

if selected_correlation >= 0.7:

    st.success(
        f"{selected_factor} has a strong positive relationship "
        f"with {sales_column}. Houses with higher values of "
        f"{selected_factor} tend to have higher sales."
    )

elif selected_correlation >= 0.3:

    st.info(
        f"{selected_factor} has a moderate positive relationship "
        f"with {sales_column}."
    )

elif selected_correlation <= -0.7:

    st.warning(
        f"{selected_factor} has a strong negative relationship "
        f"with {sales_column}. Higher values of {selected_factor} "
        f"tend to be associated with lower sales."
    )

elif selected_correlation <= -0.3:

    st.info(
        f"{selected_factor} has a moderate negative relationship "
        f"with {sales_column}."
    )

else:

    st.info(
        f"{selected_factor} has a weak linear relationship "
        f"with {sales_column}."
    )

# --------------------------------------------------
# STRONGEST FACTOR
# --------------------------------------------------

st.header("8. Main Finding")

strongest_factor = correlation.abs().idxmax()
strongest_correlation = correlation[strongest_factor]

st.write(
    f"The variable with the strongest relationship with "
    f"house sales is **{strongest_factor}**, with a correlation "
    f"of **{strongest_correlation:.3f}**."
)

if strongest_correlation > 0:

    st.write(
        f"This is a positive relationship, meaning higher values "
        f"of {strongest_factor} are generally associated with "
        f"higher house sales."
    )

else:

    st.write(
        f"This is a negative relationship, meaning higher values "
        f"of {strongest_factor} are generally associated with "
        f"lower house sales."
    )
