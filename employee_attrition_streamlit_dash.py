import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import time
import plotly.express as px


def load_data():
    df = pd.read_csv('employee_attrition_train.csv')
    return df

def preprocess_data(df):
    df = df.fillna('0')
    df['DistanceFromHome'] = pd.to_numeric(df['DistanceFromHome'], errors='coerce')
    mapping = {'Yes': 1, 'No': 0}
    df['Attrition'] = df['Attrition'].replace(mapping)
    df['Attrition'] = df['Attrition'].astype(int)
    df['Age'] = df['Age'].astype(int)
    df['DailyRate'] = df['DailyRate'].astype(int)
    return df

def create_kpi_metrics(df):
    avg_age = round(df['Age'].sum()/len(df['Age']),2)
    attrition_yes = int(
        df[(df["Attrition"] == 1)]["Attrition"].count()
        + np.random.choice(range(1, 30))
    )
    avg_daily_rate = np.mean(df["DailyRate_new"])
    return avg_age, attrition_yes, avg_daily_rate

def create_charts(df):
    fig1 = px.density_heatmap(
        data_frame=df, y="age_new", x="Attrition"
    )
    fig2 = px.histogram(data_frame=df, x="age_new")
    return fig1, fig2

import plotly.express as px

def create_map(df):
    city_data = df.groupby('City', as_index=False).mean()
    city_coords = pd.read_csv('uk_cities.csv')
    city_data = pd.merge(city_data, city_coords, on='City')
    city_data['Attrition'] = city_data['Attrition'].round(2)
    city_data['MonthlyIncome'] = city_data['MonthlyIncome'].round(2)
    city_data['JobSatisfaction'] = city_data['JobSatisfaction'].round(2)
    fig = px.scatter_mapbox(city_data, lat='Latitude', lon='Longitude', color='Attrition',
                            size='MonthlyIncome', hover_name='City',
                            hover_data=['Attrition', 'MonthlyIncome','JobSatisfaction'],
                            zoom=5, height=375, width=500)
    fig.update_layout(
        mapbox_style='open-street-map',
        margin={'l': 0, 'r': 0, 't': 10, 'b': 0}
    )
    return fig



# Modify the display_dashboard function to include the map widget
def display_dashboard(df):
    st.set_page_config(
        page_title="Employee Attrition Dashboard",
        layout="wide",
    )

    st.title("Employee Attrition Interactive Dashboard")

    dep_filter = st.selectbox("Select the department",pd.unique(df['Department']))

    df = df[df['Department']==dep_filter]

    # Creating a single element container
    placeholder = st.empty()
    df["age_new"] = df["Age"] * np.random.choice(range(1, 5))
    df["DailyRate_new"] = df["DailyRate"] * np.random.choice(range(1, 5))   

    avg_age, attrition_yes, avg_daily_rate = create_kpi_metrics(df)

    with placeholder.container():


        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Age",
            value=round(avg_age),
            delta=round(avg_age) - 10,
        )

        kpi2.metric(
            label="Attrition = Yes Count",
            value=attrition_yes,
            delta=-10 + attrition_yes,
        )

        kpi3.metric(
            label="Daily Rate",
            value=f"$ {round(avg_daily_rate,2)} ",
            delta=-round(avg_daily_rate / attrition_yes) * 100,
        )

        # create two columns for charts and map
        fig_col1, fig_col2, fig_col3 = st.columns(3)
        with fig_col1:
            st.markdown("### First Chart")
            fig1, fig2 = create_charts(df)
            st.write(fig1)

        with fig_col2:
            st.markdown("### Second Chart")
            st.write(fig2)

        with fig_col3:
            st.markdown("### Attrition by City Map")
            fig3 = create_map(df)
            st.plotly_chart(fig3)

        st.markdown("### Detailed Data View")
        st.dataframe(df)



def main():
    df = load_data()
    df = preprocess_data(df)
    display_dashboard(df)

if __name__ == "__main__":
    main()