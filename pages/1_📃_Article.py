import streamlit as st
import pandas as pd
from PIL import Image


st.set_page_config(page_title="Farmgate Article", layout="wide")

# ---- LOAD IMAGE -----
techtalk = Image.open("images/Video.PNG")

# ----- Load CSS


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

# collect basic data
df_ac = pd.read_csv("data/actual.csv")

df_crop = df_ac[["Category", "commodity"]]

df_crop = df_crop.drop_duplicates()

lst = []
for i in range(len(df_crop["Category"])):
    lst.append(i)
    i = i + 1

df_crop["idx"] = lst

pivot_table = df_crop.pivot_table(index=['idx'],
                                  columns=['Category'],
                                  values=['commodity'],
                                  aggfunc=lambda x: ' '.join(str(v) for v in x))

pivot_table = pivot_table.reset_index()

pivot_table.columns = pivot_table.columns.droplevel(0)

pivot_table = pivot_table[["Vegetable", "Fruit",
                           "Herbs and Spices", "Root Crops", "Legumes"]]

vegetable_list = pivot_table["Vegetable"].unique().tolist()
vegetable_list = [x for x in vegetable_list if str(x) != 'nan']

fruit_list = pivot_table["Fruit"].unique().tolist()
fruit_list = [x for x in fruit_list if str(x) != 'nan']

herbs_list = pivot_table["Herbs and Spices"].unique().tolist()
herbs_list = [x for x in herbs_list if str(x) != 'nan']

roots_list = pivot_table["Root Crops"].unique().tolist()
roots_list = [x for x in roots_list if str(x) != 'nan']

legumes_list = pivot_table["Legumes"].unique().tolist()
legumes_list = [x for x in legumes_list if str(x) != 'nan']


def add_null(lst_of_lists):
    max_list_size = len(vegetable_list)
    for lst in lst_of_lists:
        for i in range(len(lst), max_list_size):
            lst.append("")


category_list = [fruit_list, herbs_list, roots_list, legumes_list]
add_null(category_list)

crop_df = pd.DataFrame({"Vegetables": vegetable_list, "Fruits": fruit_list,
                       "Herbs and Spices": herbs_list, "Root Crops": roots_list, "Legumes": legumes_list})

crop_df = crop_df[crop_df["Vegetables"] != ""]


row1, row2, row3 = st.columns([0.1, 0.8, 0.1])

with row1:
    st.empty()

with row2:
    with st.container():
        st.title("Introduction")
        st.markdown("""
                ### Data visualization with Streamlit

                Streamlit is an open source tool that is rapidly growing and was recently acquired by snowflake. This project uses streamlit to build a basic but functional
                dashboard of Jamaica crop data that was scraped from the JAMIS website via a FastAPI. It will showcase the versatility of using Streamlit for reporting, dashboards
                as well as deploying the results of a machine learning model. Currently data visualization remains pivotal in creating business value and
                competitive advantage for organizations as they seek to grow business profits or capilize on data monetization projects. As a result, many businesses utilize
                off the shelf tools to manage, create, deploy and consume reports and dashboards using popular tools such as PowerBI, Tableau and excel just to name a few.
                This project will therefore use streamlit to demonstrate a paginated report, interactive dashboard,  crop price prediction results on a multipage application using streamlit.
        """)
        st.markdown("""
                ### Dataset Background

                Jamaica is known for its diverse agricultural products which are found in many of our exquisite cuisines, natural herbs, spices and remedies.
                These products are typically produced by farmers nationwide and are available on a seasonal basis. Based on historical data provided by the
                Statistical institute dated 2007, approximately 326,000 hectares of land are dedicated to active farmlands, 62% of these lands consists of both
                pastures and crops. The allocation of land solely dedicated to crops is approximately 154,000 hectares which actually represents a decline of
                about some 23,000 hectares based on a prior agricultural census executed in 1996. Despite the reported decline in active farmlands associated
                with crops, agriculture remains a priority for the Jamaican government as it accounts for 8.68% share of gross domestic product in 2020,
                where approximately 18% of the nation’s active population is employed in agriculture and 46% of the total population lives in rural areas where
                agricultural products are cultivated and therefore agriculture plays a pivotal role in Jamaica’s cultural development. As an important commodity
                within the economy it is imperative to review and analyze the cost, distribution, and quality of agricultural products. As crops are cultivated
                mainly on a seasonal or regional basis, there is significant value that can be derived if the proper channels are capitalized, to maximize general
                public consumption and to ultimately improve revenue distribution facilitated by agriculture. Agricultural products are typically available
                nationwide from basic corner stalls, brick and mortar businesses, supermarket etc. and as such many businesses stand to benefit from affordable
                and quality produce from farmers across the nation given that they have access to the necessary information that will aid in strategizing methods
                and timeframes to purchase.

                ### JAMIS
                The Jamaica Agricultural Marketing Information System (JAMIS) provides weekly unbiased reports that relates to various agricultural products across
                Jamaica. The information includes prices, availability and quality which provides useful insights as to how, where and when to purchase various products.
                There are 4 price point reports on the JAMIS website:

                1. Farmgate Prices
                2. Retail Prices
                3. Wholesale Prices
                4. Municipal Prices

                The price point of interest that was extracted for this project was the Farmgate prices, which as the website stipulates are crop prices collected on Wednesdays
                from farmers by the Marketing and Extension officers of the rural agricultural development authority (RADA). The prices are a representation of produce
                cost per Kilogram for the following Saturday of when the data was collected.
                """)
        st.write("---")

    st.title("Data Collection")

    with st.container():
        st.markdown("""
                ### Jamis Farmgate API
                The JAMIS website consisted of 4 report types where only the farmgate data was extracted and analyzed to assess
                farm prices of different agricultural products. FastAPI is an open source high performance web framework that
                facilitated converting the Jamis website publicly available data into an analytics opportunity that can potentially create avenues
                for data monetization across the agricultural industry if augmented with additional but relevant data sources.
                In order to extract data from the JAMIS website an API was built using the FastAPI software framework. The API
                allows downloading of individual pricing reports of produce between 2012 and 2022 as pdf files, after which the
                data was extracted and stored as a database file that was suitable to facilitate data processing.
                """)
        st.write("---")

    st.title("Data Description and Modeling")

    with st.container():
        st.markdown("""
                The information below outlines the data collected, data dictionary, and prediction model utilized.
                ### Description

                - Website: https://www.ja-mis.com/companionsite/home.aspx
                - Price Point Dataset: Farmgate
                - Date when prices were collected: Between Year 2012 and 2022
                - Products: 36 different agricultural products.
                - Product Category: 5 types of products (Fruit, Root Crops, Vegetables, Herbs and Spices, Legumes)
                """)

        st.write("##")

        st.markdown(
            "###### Table Representing all agricultural products within the dataset")

        st.dataframe(crop_df, 700, 700)

        st.markdown("""

                ### Data Dictionary

                - Price Date: The date the price was recorded
                - Parish: The parish in which the commodity (produce) is located
                - Commodity: The name of the agricultural product
                - Type: A description of the agricultural product
                - Category: The category that the agricultural product belongs to
                - Supply: An indication of the abundance of the product
                - Grade: An indication of the quality of the product
                - Price: An indication of the price of goods
                - Most frequent: An indication of the most frequent price of commodity (produce)
                """)

        st.markdown("""

                ### Data Modelling

                To predict the price of different products over time the variable to consider and to build a prediction model
                against is the most frequent price variable, therefore the low and high price attributes were ommitted from data modelling. 
                The most frequent price attribute contains contiguous values and therefore a regression
                model is the most suitable approach to determine the relationship between all attribute columns from the dataset
                against the most frequent price column which is the target variable.
                The modeling process was measured against 5 different regression models where the model with least mean square error
                or mean percentage error and the highest r squared score was selected. The r squared score is a measure of how well the proportion
                of variance of the product prices is explained by all the other columns / attributes within the dataset. The model
                selected was built from Random Forest Regressor which subsequently can be used to predict future product prices, and can be
                modified or rebuilt to incorporate data from other JAMIS agricultural product prices for future initiatives.

                ### Random Regressor Performance:

                - Mean Absolute Percentage Error (MAPE) value given in percentage: 13.43%
                - Mean absolute error: 24.68
                - Mean squared error: 45.85
                - r-squared score: 89.23 %
                - Model performance: 89.23% accuracy

                Note (Larger r2 scores implies greater dependency of product prices on the independent variables such as date, parish,
                commodity, supply, type, supply, grade, etc) *

                """)
        st.markdown("""

                ### Dashboard and Visuals
                Now that we have described the data and the prediction models performance, its time to review how we can display reports and visuals
                in the form of a dashboard. The typical formart will include some snapshots that showcases the average crop price by category followed by bar charts, a 
                Jamaica chloropleth graph and sunburst charts to represent hierarchical data. These visuals will show how averae crop prices are distributed by parish and the
                respectives months where crop prices are the highest. Finally we can complete our visuals with A tabulated report where the first tab consists of line plots 
                and stacked bar graphs to assess a more detailed description of prices and trends by supply and grade, as well as scatter charts and pie charts 
                on tab two for assesing price distribution over time. Since streamlit is a python oriented tool, we have access to a plethora of data visualization libraries. 
                These libraries include altair charts, plotly, bokeh etc. For this project mainly the plotly library was used to build the visuals for the dashboard and 
                the prediction results visuals. This dashboard will feature a limited amount of slicers and drop down options within the sidebar menu to allow users to interact with 
                datasets as they see fit. 

                    
                ### Forecasting
                The modeling procedure used for this project only accounts for data available on the JAMIS website and was not augmented by any additional sources. Therefore
                this model is soley for illustraiton purposes and how streamlit is a great tool to facilitate deployment.  Users may use the drop down menu options which includes
                the year and parish filters to review crop predicted prices by month or to the general trend of crop category prices over time.                    

                """)

        st.write("##")
        st.write("##")
        st.write("##")
        st.markdown("""
                ### 
                    Use to contact form below to reach out to me via email if have you have any questions about streamlit, data modeling or data visualization. You can 
                    also check out my youtube post where I show how to deploy an azure pipeline using azure cloud services.
                    """)


with row3:
    st.empty()


with st.container():
    st.write("##")
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
