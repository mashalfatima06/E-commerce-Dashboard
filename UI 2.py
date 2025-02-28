import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #222831;
            color: white;
        }
        div.stButton > button {
            background-color: #ff6f61;
            color: white;
            border-radius: 8px;
        }
        div.stSelectbox > label {
            color: white;
        }
        /* Change radio button text color to white */
        div[role="radiogroup"] label {
            color: white !important;
        }
        
        /* Set Background Image */
        .stApp {
            background-image: url("https://www.freepik.com/free-photo/hand-painted-watercolor-background-with-sky-clouds-shape_9728603.htm#fromView=keyword&page=1&position=49&uuid=1a43005a-0f4d-459e-b8a2-14f40fe4bcdb&quer");
        }
    </style>
    """,
    unsafe_allow_html=True
)


file_path = "Pakistan Largest Ecommerce Dataset.csv"
df = pd.read_csv(file_path)

drop_columns = ["increment_id", "Working Date", "BI Status", "MV", "M-Y", "FY", "Unnamed: 21", "Unnamed: 22", "Customer ID"]
df.drop(columns=[col for col in drop_columns if col in df.columns], inplace=True)
df["price"].fillna(df["price"].mean(), inplace=True)
df["grand_total"].fillna(df["grand_total"].mean(), inplace=True)
df["discount_amount"].fillna(0, inplace=True)
df.dropna(subset=["qty_ordered", "payment_method", "Year", "Month"], inplace=True)

st.sidebar.title("⚙️ Dashboard Filters")
st.sidebar.image("image1.jpg",width=250)
page = st.sidebar.radio("Select Analysis", ["Home","Category Analysis", "Payment Method Analysis", "Yearly Revenue Analysis"])
if page == "Home":
    #col1, col2 = st.columns([3, 4])
    #with col1:
    st.title("🛒Pakistan's E-Commerce Insights")  
    #with col2:  
    #st.image("image11.png",width=850)
    

    # Yearly Revenue Data
    revenue_data = {
        "Year": [2018, 2019, 2020, 2021, 2022, 2023],
        "Revenue": [1.0, 1.8, 2.7, 3.9, 5.2, 6.3]
    }
    df_revenue = pd.DataFrame(revenue_data)
    
    # Revenue Bar Plot
    st.subheader="Yearly E-Commerce Revenue Growth in Pakistan"
    fig = px.bar(df_revenue, x="Year", y="Revenue", text_auto=True, 
                 labels={"Year": "Year", "Revenue": "Revenue"},
                 color_discrete_sequence=["#E75480"])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Economic Impact Section
    st.markdown(
        """
        ## 📊 Impact on Pakistan's Economy
        
        - **Job Creation:** 500,000+ people employed in e-commerce-related sectors
        - **Economy boost up:** Companies like **Alibaba (Daraz)** investing in Pakistan
        - **Digital Payments Boom:** Growth of **Easypaisa, JazzCash, and RAAST**
        - **Post-COVID Growth:** Online shopping increased **100% during COVID-19**
        - **Future Projection:** Expected to **exceed $10 billion by 2025**
        **Pakistan's e-commerce sector is shaping the digital economy, providing new opportunities for businesses and consumers alike.**
        """
    )


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
