import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import base64

def set_bg_image(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            .metric-box {{
                text-align: center;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            }}
            .metric-box h1 {{
                color: #d1001c;
                margin: 0;
            }}
            .metric-box p {{
                margin: 0;
                font-size: 18px;
                color: #333;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_bg_image("bbb.jpg")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #A5DEF2;
            color: black;
        }
        div.stButton > button {
            background-color: #ff6f61;
            color: white;
            border-radius: 8px;
        }
        div.stSelectbox > label {
            color: black;
        }
        div[role="radiogroup"] label {
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

file_path = "cleaned_file.csv"
df = pd.read_csv(file_path)

drop_columns = ["increment_id", "Working Date", "BI Status", "MV", "M-Y", "FY", "Unnamed: 21", "Unnamed: 22", "Customer ID"]
df.drop(columns=[col for col in drop_columns if col in df.columns], inplace=True)
df["price"].fillna(df["price"].mean(), inplace=True)
df["grand_total"].fillna(df["grand_total"].mean(), inplace=True)
df["discount_amount"].fillna(0, inplace=True)
df.dropna(subset=["qty_ordered", "payment_method", "Year", "Month"], inplace=True)

st.sidebar.title("⚙️ Dashboard Filters")
st.sidebar.image("download1.png", width=250)
page = st.sidebar.radio("Select Analysis", ["Home", "Category Analysis", "Payment Method Analysis", "Yearly Revenue Analysis"])

if page == "Home":
    st.title("🛒 Pakistan's E-Commerce Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-box"> <h1>500,000+</h1> <p>Jobs Created</p> </div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"> <h1>100%</h1> <p>Online Shopping Growth in Covid-19</p> </div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"> <h1>$10B</h1> <p>Projected Revenue by 2025</p> </div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"> <h1>FDI+</h1> <p>Alibaba & Others Investing</p> </div>', unsafe_allow_html=True)
    

    revenue_data = {
        "Year": [2018, 2019, 2020, 2021, 2022, 2023],
        "Revenue": [1.0, 1.8, 2.7, 3.9, 5.2, 6.3]
    }
    df_revenue = pd.DataFrame(revenue_data)
    st.header("Yearly E-Commerce Revenue Growth in Pakistan")
    fig = px.bar(df_revenue, x="Year", y="Revenue", text_auto=True, 
                 labels={"Year": "Year", "Revenue": "Revenue (Billion USD)"},
                 color_discrete_sequence=["#E75480"])
    st.plotly_chart(fig, use_container_width=True)


elif page == "Category Analysis":
    st.title("📦 Category Analysis")
    selected_categories = st.multiselect("Select Categories", df["category_name_1"].unique())
    df_selected = df[df["category_name_1"].isin(selected_categories)]
    
    if not df_selected.empty:
        fig = px.bar(df_selected, x="Month", y="grand_total", color="category_name_1", title="Sales by Category")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one category to display the data.")

elif page == "Payment Method Analysis":
    st.title("💳 Payment Method Analysis")
    selected_methods = st.multiselect("Select Payment Methods", df["payment_method"].unique())
    df_selected = df[df["payment_method"].isin(selected_methods)]
    
    if not df_selected.empty:
        fig = px.pie(df_selected, names="payment_method", values="grand_total", title="Revenue by Payment Method")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one payment method to display the data.")

elif page == "Yearly Revenue Analysis":
    st.title("📅 Yearly Revenue Analysis")
    selected_years = st.multiselect("Select Years", df["Year"].unique())
    df_selected = df[df["Year"].isin(selected_years)]
    
    if not df_selected.empty:
        fig = px.bar(df_selected, x="Month", y="grand_total", color="Year", title="Yearly Revenue Trends")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one year to display the data.")







