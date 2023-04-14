import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')
import hvplot.pandas

def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")
    return df

def clean_data(df):
    df = df.fillna(0)
    df['gdp_per_capita'] = np.where(df['population']!= 0, df['gdp']/ df['population'], 0)
    idf = df.interactive()
    return idf

def create_year_slider():
    year_slider = pn.widgets.IntSlider(name='Year slider', start=1750, end=2020, step=5, value=1850)
    return year_slider

def create_yaxis_co2():
    yaxis_co2 = pn.widgets.RadioButtonGroup(
        name='Y axis',
        options=['co2', 'co2_per_capita',],
        button_type='success'
    )
    return yaxis_co2

def create_continents():
    continents = ['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica']
    return continents

def create_co2_pipeline(idf, year_slider, continents, yaxis_co2):
    co2_pipeline = (
        idf[
            (idf.year <= year_slider) &
            (idf.country.isin(continents))
        ]
        .groupby(['country', 'year'])[yaxis_co2].mean()
        .to_frame()
        .reset_index()
        .sort_values(by='country')  
        .reset_index(drop=True)
    )
    return co2_pipeline

def create_co2_plot(co2_pipeline, yaxis_co2):
    co2_plot = co2_pipeline.hvplot(x='year', by='country', y=yaxis_co2, line_width=2, title="CO2 emission by continent")
    return co2_plot

def create_co2_table(co2_pipeline):
    co2_table = co2_pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size=10, sizing_mode='stretch_width')
    return co2_table

def create_co2_vs_gdp_scatterplot_pipeline(idf, year_slider, continents):
    co2_vs_gdp_scatterplot_pipeline = (
        idf[
            (idf.year == year_slider) &
            (~ (idf.country.isin(continents)))
        ]
        .groupby(['country', 'year', 'gdp_per_capita'])['co2'].mean()
        .to_frame()
        .reset_index()
        .sort_values(by='year')  
        .reset_index(drop=True)
    )
    return co2_vs_gdp_scatterplot_pipeline

def create_co2_vs_gdp_scatterplot(co2_vs_gdp_scatterplot_pipeline):
    co2_vs_gdp_scatterplot = co2_vs_gdp_scatterplot_pipeline.hvplot(x='gdp_per_capita', y='co2', by='country', size=80, kind="scatter", alpha=0.7, legend=False, height=500, width=500)
    return co2_vs_gdp_scatterplot

def create_yaxis_co2_source():
    yaxis_co2_source = pn.widgets.RadioButtonGroup(
        name='Y axis',
        options=['coal_co2', 'oil_co2', 'gas_co2'],
        button_type='success'
    )
    return yaxis_co2_source

def create_co2_source_bar_pipeline(idf, year_slider, continents_excl_world, yaxis_co2_source):
    co2_source_bar_pipeline = (
        idf[
            (idf.year == year_slider) &
            (idf.country.isin(continents_excl_world))
        ]
        .groupby(['year', 'country'])[yaxis_co2_source].sum()
        .to_frame()
        .reset_index()
        .sort_values(by='year')  
        .reset_index(drop=True)
    )
    return co2_source_bar_pipeline

def create_co2_source_bar_plot(co2_source_bar_pipeline, yaxis_co2_source):
    co2_source_bar_plot = co2_source_bar_pipeline.hvplot(kind='bar', 
                                                         x='country', 
                                                         y=yaxis_co2_source, 
                                                         title='CO2 source by continent')
    return co2_source_bar_plot
year_slider = create_year_slider()
sidebar_components = [
    pn.pane.Markdown("# CO2 Emissions and Climate Change"),
    pn.pane.Markdown("#### Carbon dioxide emissions are the primary driver of global climate change."),
    pn.pane.PNG('https://icons.iconarchive.com/icons/graphicloads/100-flat/256/bank-icon.png'),
    pn.pane.Markdown("## Settings"),
    year_slider
]
main_components = [
    pn.Row(
        pn.Column(yaxis_co2, co2_plot.panel(width=700), margin=(0, 25)),
        co2_table.panel(width=500)
    ),
    pn.Row(
        pn.Column(co2_vs_gdp_scatterplot.panel(width=600), margin=(0, 25)),
        pn.Column(yaxis_co2_source, co2_source_bar_plot.panel(width=600))
    )
]

template = pn.template.FastListTemplate(
    title='World CO2 emission dashboard',
    sidebar=sidebar_components,
    main=main_components,
    accent_base_color="#88d8b0",
    header_background="#88d8b0"
)
template.show()