import streamlit as st
from pandas.tseries.offsets import MonthEnd
import pandas as pd
from PIL import Image
import time
import plotly.express as px


st.set_page_config(page_title="Farmgate Prediction",
                   layout="wide", page_icon="📈")

# ---- LOAD Image -----
techtalk = Image.open("images/Video.PNG")

# ----- Load CSS


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")


st.title("Simple Prediction Tool")

st.write("---")


@st.cache_data
def get_data():
    #AZ_BUCKET_URL = "https://azjcsdls01.blob.core.windows.net/farmgate/"
    #df_pred = pd.read_csv(AZ_BUCKET_URL + "/predictions.csv")
    df_pred = pd.read_csv('data/predictions.zip')
    df_pred["month1"] = pd.to_datetime(df_pred['price_date']).dt.month
    df_pred["month"] = pd.to_datetime(df_pred['price_date']).dt.strftime('%B')
    df_pred["year"] = pd.to_datetime(df_pred['price_date']).dt.strftime('%Y')
    df_pred["date_time"] = pd.to_datetime(
        df_pred['price_date'], format="%Y-%m-%d") + MonthEnd(0)
    df_pred = df_pred.loc[df_pred["year"] != '2022']
    df_pred["price_date"] = pd.to_datetime(
        df_pred['price_date'], format="%Y-%m-%d")
    df_pred = df_pred.sort_values("price_date", ascending=True)
    return df_pred


with st.spinner('Loading'):
    time.sleep(1)
    df_pred = get_data()
    years_list = [i for i in df_pred['year'].unique()]
    parish_list = [i for i in df_pred['parish'].unique()]
    parish_list.sort(reverse=False)

    year = st.multiselect("Select Year", options=years_list, default="2023")
    parish = st.multiselect(
        "Select Parish", options=parish_list, default=parish_list[0:5])

    if (year == []) | (parish == []):
        st.error("Please select at least one value for Parish or Year")
    else:
        dff1 = df_pred.query('(parish ==@parish) & (year ==@year)')

        dff = dff1.groupby(["year", "month", "month1", "parish", "commodity"])[
            'Predicted_Price'].mean().reset_index()
        dff = dff.sort_values(["month1"], ascending=True)

        dff_pivot = dff.pivot_table(
            values='Predicted_Price', index=dff.commodity, columns='month', aggfunc='first')

        dff_pivot = dff_pivot[["January", "February", "March", "April", "May",
                               "June", "July", "August", "September", "October", "November", "December"]]

        dff_pivot = dff_pivot.round(2)

        dff_pivot = dff_pivot.sort_index()

        dff_chart = dff1.groupby(["date_time", "Category"])[
            'Predicted_Price'].mean().reset_index()

        dff_chart = dff_chart.round(2)

        df_chart = dff_chart.sort_values(["date_time"], ascending=True)

        fig = px.area(df_chart, x="date_time",
                      y="Predicted_Price", color="Category")

        fig.update_layout(title_text='Crop Category Predicted Price JMD per KG', title_x=0.5,
                          plot_bgcolor="rgba(0,0,0,0)")

        row1, row2, row3 = st.columns([0.15, 0.7, 0.15])

        with row1:
            st.empty()

        with row2:
            st.markdown("###### Predicted Average Crop Price in JMD per per month")
            st.dataframe(dff_pivot)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        with row3:
            st.empty()

# *************************************************************************************************************

with st.container():
    st.write("---")
    st.header("Youtube Expert Hour")
    st.write("##")
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(techtalk)
    with text_column:
        st.subheader("Tech Expert Hour")
        st.write(
            """This Tech Expert illustration shows how to establish data pipelines within the azure cloud platform. 
               In this illustration I'll show you how to build data pipelines and more uwing azure data factory"""
        )
        st.markdown(
            "[Watch Now...](https://www.youtube.com/watch?v=mWW-OsELCn0&t=1400s)")

# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Contact Form")
    st.write("##")

    # Documentation: https://formsubmit.co/ !!!
    contact_form = """
    <form action="https://formsubmit.co/jc.samuels21@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here" required></textarea>
     <button type="submit">Send</button>
</form>
    """

left_column, right_column = st.columns(2)
with left_column:
    st.markdown(contact_form, unsafe_allow_html=True)
with right_column:
    st.empty()

hide_st_style = """
                <style>
                # MainMenu {visibility: hidden;}
                footer{visibility: hidden;}
                header{visibility:hidden;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)
