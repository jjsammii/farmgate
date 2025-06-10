import streamlit as st
from streamlit_lottie import st_lottie
import requests
#import plotly.graph_objects as go
from PIL import Image
import os


st.set_page_config(
    page_title="Home", layout="wide"
)


def load_lottieurl(url):
    r = requests.get(url, verify=False)
    if r.status_code != 200:
        return None
    return r.json()


# ----- Assets ----------

lottie_coding = load_lottieurl(
    "https://assets7.lottiefiles.com/private_files/lf30_ijvfbn98.json")

# ---- LOAD Image -----
if os.path.exists("images/Video.PNG"):
    techtalk = Image.open("images/Video.PNG")
else:
    st.warning("Video.PNG not found in images directory.")

# ----- Load CSS


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")


st.title("Welcome to Farmgate Dashboard")

st.write("---")

st.sidebar.success("Select a Report Above.")


left_column, right_column = st.columns(2)
with left_column:
    st.write(
        "This dashboard showcases reports in relation to Farmgate data available on Jamis Website [Web link](https://www.ja-mis.com/companionsite/reportsarchive.aspx)")
    st.write("A prediction report was added to forecast Crop Prices across Jamaica for the next three years (2023 - 2025) as the last data extracted was done December 2022")
    st.write("**👈 Select a Report from the sidebar menu options and choose the appropriate filters below")
    st.markdown("""
                ### Please see details of each dash board listed below?
                - Article: Describes Basic Streamlit deployment, data collection and visualization for JAMIS farmgate data.
                - Dashboard: Interactive dashboard that allows users to manipulate and visualize datasets.
                - Prediction Report: Contains prediction prices for crops for each month with the ability to 
                  filter results based on year and parish.
                """
                )
with right_column:
    st_lottie(lottie_coding, height=400, key="crops")


with st.container():    
    st.write("##")
    st.write("##")
    st.write("##")
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
               In this illustration I'll show you how to build data pipelines and more using azure data factory"""
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
