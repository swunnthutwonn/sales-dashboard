import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time

st.set_page_config (
    page_title = "Sale Dashboard",
    page_icon = '📊',
    layout = "wide",
    initial_sidebar_state = "auto",
    # initial_sidebar_state = "collapsed"
    # initial_sidebar_state = "expanded"
    menu_items={
        "Get Help": "https://support.example.com",
        "Report a bug": "https://bugtracker.example.com",
        "About": "This is a demo dashboard."
    }
)


# Load CSS from external file
def load_css(file_name):
    with open(file_name, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)



# Load Data Function
@st.cache_data
def load_data():
    df = pd.read_csv('sale_data.csv', parse_dates=["Date"])
    return df

st.sidebar.header("🔄 Auto Refresh")
refresh_rate = st.sidebar.slider("Set refresh rate (seconds)", 5, 60, 10)

df = load_data()

# Add Manual Refresh Button
if st.sidebar.button("🔄 Refresh Now"):
    st.rerun()



# Calculate key metric
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

# Display KPI
col1, col2 = st.columns(2)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")

tab1, tab2, tab3 = st.tabs(["📈 Sales Trends", "📍 Sales by Region", "📊 Category Analysis"])


# Sidebar filter
st.sidebar.header("🔍 Filter Options")

# Date filter
start_date, end_date = st.sidebar.date_input(
    "Select Date Range", [df["Date"].min(), df["Date"].max()]
)

# Categories filte
categories = df["Category"].unique()
selected_category = st.sidebar.multiselect("Select Category", categories, default=categories)


# Apply filter
filtered_df = df [
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date)) &
    (df["Category"].isin(selected_category))
]

with tab1:
    st.subheader("📈 Animated Sales Trends Over Time")

    # Aggregate sales by date
    sale_trend = filtered_df.groupby("Date")["Sales"].sum().reset_index()

    # st.dataframe(sale_trend)

    # Plot line chart
    fig = px.line(
        sale_trend,
        x="Date", y="Sales",
        title="Sale Over Time",
        markers=True,
        animation_frame="Date"
    )
    st.plotly_chart(fig)

with tab2:
    st.subheader("📍 Sales by Region")
    
    sales_by_region = filtered_df.groupby("Region")["Sales"].sum().reset_index()

    # Bar chart
    fig = px.bar(sales_by_region, x="Region", y="Sales", title="Sale by Region", color="Sales")
    st.plotly_chart(fig)

with tab3:
    st.subheader("📊 Sales by Categories")

    sales_by_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()

    fig = px.pie(sales_by_category, names="Category", values="Sales", title="Sale Distribution by Category")
    st.plotly_chart(fig)