import pandas as pd
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
import plotly.graph_objects as go
import json
from PIL import Image


st.set_page_config(page_title="Farmgate Analytics",
                   layout="wide")

# ---- LOAD IMAGE -----
techtalk = Image.open("images/Video.PNG")

# ----- Load CSS


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")


st.title("Welcome to Farmgate Dashboard")

st.write("---")

df_ac = pd.read_csv("data/actual.csv")

# -------------------------Initial------------------------------------

# Convert the data type of column 'Date' from string (YYYY/MM/DD) to datetime64
df_ac["price_date"] = pd.to_datetime(df_ac["price_date"], format="%m/%d/%Y")
df_ac["price_date"] = df_ac["price_date"].dt.date

# extracting dates
start_date = df_ac["price_date"].min()
stop_date = df_ac["price_date"].max()

parish_list = [i for i in df_ac['parish'].unique()]
parish_list.sort(reverse=False)

category_list = [i for i in df_ac['Category'].unique()]
category_list.sort(reverse=False)

commodity_list = [i for i in df_ac['commodity'].unique()]
commodity_list.sort(reverse=False)

supply_list = [i for i in df_ac['supply'].unique()]
supply_list.sort(reverse=False)

grade_list = [i for i in df_ac['grade'].unique()]
grade_list.sort(reverse=False)


# ------ SIDEBAR -------------------
st.sidebar.header("Please Filter Here:")
period = st.sidebar.slider(f"Date Range:", value=(
    start_date, stop_date), format="YYYY/MMM", label_visibility="collapsed")

parish = st.sidebar.multiselect(
    "Parishes", options=parish_list, default=parish_list)

category = st.sidebar.multiselect(
    "Crop Type", options=category_list, default=category_list)

supply = st.sidebar.multiselect(
    "Supply", options=supply_list, default=supply_list)

grade = st.sidebar.multiselect("Grade", options=grade_list, default=grade_list)

if (period == []) | (parish == []) | (category == []) | (supply == []) | (grade == []):
    st.error("Please select at least one value for each drop down menu options")
else:
    df = df_ac.query(
        # '(price_date >= @period[0] & price_date <= @period[1]) | price_date >= @period[0] & parish == @parish & Category ==@category & supply ==@supply & grade ==@grade'
        '(price_date >= @period[0] & price_date <= @period[1]) & (parish == @parish) & (Category ==@category) & (supply ==@supply) & (grade ==@grade)')

    commodity = st.sidebar.multiselect(
        "Crop Name", options=commodity_list, default=commodity_list)

    df = df.query('commodity ==@commodity')

    df = df.round({"Actual_Price": 2})

    cards1, cards2, cards3, cards4, cards5 = st.columns(5)

    cards_metric_df = df.groupby(["Category"])[
        'Actual_Price'].mean().reset_index()

    def get_val(dframe, lst):
        if len(lst) == 0:
            val = 0
        else:
            val = dframe.Actual_Price.values[0]
            val = round(val, 2)
        return val

    fruits = cards_metric_df.loc[cards_metric_df["Category"] == "Fruit"]
    fruits_list = fruits.Actual_Price.values
    fruits_val = get_val(fruits, fruits_list)

    herbs = cards_metric_df.loc[cards_metric_df["Category"]
                                == "Herbs and Spices"]
    herbs_list = herbs.Actual_Price.values
    herbs_val = get_val(herbs, herbs_list)

    legumes = cards_metric_df.loc[cards_metric_df["Category"] == "Legumes"]
    legumes_list = legumes.Actual_Price.values
    legumes_val = get_val(legumes, legumes_list)

    roots = cards_metric_df.loc[cards_metric_df["Category"] == "Root Crops"]
    roots_list = roots.Actual_Price.values
    roots_val = get_val(roots, roots_list)

    vegetables = cards_metric_df.loc[cards_metric_df["Category"]
                                     == "Vegetable"]
    vegetables_list = vegetables.Actual_Price.values
    vegetables_val = get_val(vegetables, vegetables_list)

    with cards1:
        st.metric(label="Avg Fruits Price JMD / KG :apple:",
                  value="$ " + str(fruits_val))

    with cards2:
        st.metric(label="Avg Herbs Price JMD / KG :herb:",
                  value="$ " + str(herbs_val))

    with cards3:
        st.metric(label="Avg Legumes Price JMD / KG :corn:",
                  value="$ " + str(legumes_val))

    with cards4:
        st.metric(label="Avg Roots Price JMD / KG :seedling:",
                  value="$ " + str(roots_val))

    with cards5:
        st.metric(label="Avg Vegetables Price JMD / KG :tomato:",
                  value="$ " + str(vegetables_val))

    border_left_color: str = "#1F77B4",
    box_shadow: bool = True,

    style_metric_cards(border_left_color)

    st.write("---")

    # Row 2
    # Chloropleth plot
    with open('data/geojson.json') as f:
        geojson = json.load(f)

    df_parish = df.groupby(["parish"])['Actual_Price'].mean().reset_index()
    df_parish = df_parish.round()

    fig_chloro = px.choropleth(df_parish, geojson=geojson, color="Actual_Price",
                               locations="parish", featureidkey="properties.woe_name",
                               color_continuous_scale="Jet",
                               range_color=(110, 300),
                               labels={"parish": "Parish",
                                       "Actual_Price": "Actual Price"}, width=600, height=450
                               )
    fig_chloro.update_geos(fitbounds="locations", visible=False)

    fig_chloro.add_scattergeo(
        geojson=geojson,
        locations=df_parish['parish'],
        text=df_parish['Actual_Price'],
        featureidkey="properties.woe_name",
        mode='text',
    )
    fig_chloro.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        title_text="Total Price Average Price Distribution", title_x=0.5,
        dragmode=False
    )

    # Plotting Highlight Bar Chart
    df["month1"] = pd.to_datetime(df['price_date']).dt.month
    df["month"] = pd.to_datetime(df['price_date']).dt.strftime('%b')
    df["year"] = pd.to_datetime(df['price_date']).dt.year
    df["month_year"] = pd.to_datetime(df['price_date']).dt.strftime('%b-%Y')

    df_hp = df.groupby(["month", "month1"])[
        'Actual_Price'].mean().reset_index()
    df_hp["Actual_Price"] = [round(i) for i in df_hp["Actual_Price"]]
    df_hp = df_hp.sort_values(["month1"], ascending=True)

    df_hp = df_hp.reset_index(drop=True)

    df_hp1 = df_hp.copy()

    idx_list = []
    num = 0
    for i in range(5):
        idx_list.append(df_hp1["Actual_Price"].idxmax())
        df_hp1 = df_hp1.drop(idx_list[num])
        num = num+1

    colors = ['#1F77B4',] * len(df_hp)
    colors[idx_list[0]] = '#BF1A2F'
    colors[idx_list[1]] = '#ED6A5A'
    colors[idx_list[2]] = '#ED6A5A'
    colors[idx_list[3]] = '#E7BA52'
    colors[idx_list[4]] = '#E7BA52'
    # colors[idx_list[4:5]] = 'orange'

    fig_hp = go.Figure(data=[go.Bar(
        x=df_hp['month'],
        y=df_hp['Actual_Price'],
        marker_color=colors,
        text=df_hp['Actual_Price'],
        textposition='outside'  # marker color can be a single color value or an iterable
    )])

    fig_hp.update_layout(title_text='Avg price per KG / Month', title_x=0.5,
                         plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(
                             title='Average Price $JMD'), width=300,
                         height=300, margin=dict(l=5, r=5, t=68, b=0))
    fig_hp.update_xaxes(showgrid=False, visible=True, fixedrange=True)
    fig_hp.update_yaxes(showgrid=False, visible=True, fixedrange=True)

    # Plottin Sunburst
    df_seg = df.groupby(["supply", "grade", "commodity"])[
        'Actual_Price'].mean().reset_index()

    fig_sun = px.sunburst(df_seg, path=['supply', 'grade', 'commodity'],
                          values='Actual_Price', color='supply',
                          color_discrete_map={'Scarce': '#BF1A2F', 'Moderate': '#E7BA52', 'Fair': '#1F77B4',
                                              'Average': '#8EB8E5', 'Good': '#6457A6', 'Abundant': '#4E937A'}, width=300, height=400)

    fig_sun.update_layout(
        title_text="Heirarchal Report by Abundance, Grade and Commodity", title_x=0.5)
    fig_sun.update_traces(textinfo="label+percent parent"
                          )

    # Plotting by Column
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.plotly_chart(fig_chloro, use_container_width=True,
                        theme="streamlit")

    with row2_col2:
        st.plotly_chart(fig_hp, use_container_width=True, theme="streamlit")

    with row2_col3:
        st.plotly_chart(fig_sun, use_container_width=True, theme="streamlit")

    # ROW 3

    # Scatter and bar plot
    df_avail = df.groupby(["price_date", "grade", "supply"])[
        'Actual_Price'].mean().reset_index()

    df_avail["grade1"] = [1 if i == "Average" else 2 if i ==
                          "Good" else 3 for i in df_avail["grade"]]

    df_avail = df_avail.round()

    # df_avail0 = df.groupby(["month", "month1", "supply"])[ 'Actual_Price'].mean().reset_index()

    df_avail0 = df.groupby(["year", "supply"])[
        "Actual_Price"].mean().reset_index()

    df_avail0 = df_avail0.sort_values(["year"], ascending=True)

    df_avail0 = df_avail0.round()

    df_avail1 = df.groupby(["year", "grade"])[
        'Actual_Price'].mean().reset_index()

    df_avail1 = df_avail1.sort_values(["year"], ascending=True)

    df_avail1 = df_avail1.round()

    df_supply = df.groupby(["month", "month1", "supply"])[
        'Actual_Price'].mean().reset_index()

    df_supply = df_supply.sort_values(["month1"], ascending=True)

    df_supply = df_supply.round()

    df_grade = df.groupby(["month", "month1", "grade"])[
        'Actual_Price'].mean().reset_index()

    df_grade = df_grade.sort_values(["month1"], ascending=True)

    df_grade = df_grade.round()

    # Line Plots
    fig_line_sup = px.line(df_avail0, x="year",
                           y="Actual_Price", color="supply")

    fig_line_sup.update_layout(title_text='Average Price by Supply over Time', title_x=0.5,
                               plot_bgcolor="rgba(0,0,0,0)", width=550,
                               height=350)

    fig_line_grade = px.line(df_avail1, x="year",
                             y="Actual_Price", color="grade")

    fig_line_grade.update_layout(title_text='Average Price by Grade over Time', title_x=0.5,
                                 plot_bgcolor="rgba(0,0,0,0)", width=550,
                                 height=350)

    # stack bar plots

    fig_stack_sup = px.bar(df_supply, x="month",
                           y="Actual_Price", text_auto=True, color="supply")

    fig_stack_sup.update_layout(title_text='Crop Price and Availability by Month', title_x=0.5,
                                plot_bgcolor="rgba(0,0,0,0)", width=550,
                                height=350)

    fig_stack_grade = px.bar(
        df_grade, x="month", y="Actual_Price", text_auto=True, color="grade")

    fig_stack_grade.update_layout(title_text='Crop Price and Quality by Month', title_x=0.5,
                                  plot_bgcolor="rgba(0,0,0,0)", width=550,
                                  height=350)

    # Pie Charts
    fig_pie_sup = go.Figure(data=[go.Pie(
        labels=df_avail["supply"].unique(), values=df_avail["Actual_Price"], hole=.6)])

    fig_pie_sup.update_layout(title_text='Average Price by Supply', title_x=0.5,
                              plot_bgcolor="rgba(0,0,0,0)", width=550,
                              height=350)

    fig_pie_grade = go.Figure(data=[go.Pie(
        labels=df_avail["grade"].unique(), values=df_avail["Actual_Price"], hole=.6)])

    fig_pie_grade.update_layout(title_text='Average Price by Quality', title_x=0.5,
                                plot_bgcolor="rgba(0,0,0,0)", width=550,
                                height=350)

    # Scatter Plots for supply and grade reports

    fig_supply = px.scatter(df_avail, x="price_date", y="Actual_Price", color="supply",
                            size='Actual_Price')

    fig_supply.update_layout(title_text='Average Price by Supply / Month', title_x=0.5,
                             plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(
                                 title='Average Price $JMD'), width=550,
                             height=350)
    fig_supply.update_xaxes(showgrid=False, visible=True)
    fig_supply.update_yaxes(showgrid=False, visible=True)

    # quality plots
    fig_quality = px.scatter(df_avail, x="price_date", y="Actual_Price", color="grade",
                             size='Actual_Price')

    fig_quality.update_layout(title_text='Average Price by Quality / Month', title_x=0.5,
                              plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(
                                  title='Average Price $JMD'), width=550,
                              height=350)
    fig_quality.update_xaxes(showgrid=False, visible=True)
    fig_quality.update_yaxes(showgrid=False, visible=True)

    # Plotting Line Charts, Stack Bar Graphs and scatter plots Row3

    tab1, tab2 = st.tabs(["Trends", "Price Distribution"])

    with tab1:
        row3_col1, row3_col2 = st.columns(2)

        with row3_col1:
            st.plotly_chart(fig_line_sup, theme="streamlit",
                            use_container_width=True)

        with row3_col2:
            st.plotly_chart(fig_stack_sup, theme="streamlit",
                            use_container_width=True)

        with row3_col1:
            st.plotly_chart(fig_line_grade, theme="streamlit",
                            use_container_width=True)

        with row3_col2:
            st.plotly_chart(fig_stack_grade, theme="streamlit",
                            use_container_width=True)

    with tab2:
        row3_col1, row3_col2 = st.columns(2)

        with row3_col1:
            st.plotly_chart(fig_supply, theme="streamlit",
                            use_container_width=True)

        with row3_col2:
            st.plotly_chart(fig_pie_sup, theme="streamlit",
                            use_container_width=True)

        with row3_col1:
            st.plotly_chart(fig_quality, theme="streamlit",
                            use_container_width=True)

        with row3_col2:
            st.plotly_chart(fig_pie_grade, theme="streamlit",
                            use_container_width=True)

with st.container():
    st.write("##")
    st.write("##")
    st.write("##")
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
