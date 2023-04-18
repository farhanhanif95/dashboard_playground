import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import time

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
    for seconds in range(2000):
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

            # create two columns for charts
            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                st.markdown("### First Chart")
                fig1, fig2 = create_charts(df)
                st.write(fig1)

            with fig_col2:
                st.markdown("### Second Chart")
                st.write(fig2)

            st.markdown("### Detailed Data View")
            st.dataframe(df)
            time.sleep(1)

def main():
    df = load_data()
    df = preprocess_data(df)
    display_dashboard(df)

if __name__ == "__main__":
    main()