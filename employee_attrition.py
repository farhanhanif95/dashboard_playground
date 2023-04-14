import pandas as pd
import hvplot.pandas as hv
import panel as pn

# Read the data
df_train = pd.read_csv(r"C:\Users\mfarh\OneDrive\Personal and Private\Documents\GitHub\dashboard_playground\employee_attrition_train.csv")
df_train['Attrition'] = df_train['Attrition'].replace({"No": 0, "Yes": 1})

# Define widgets
age_min = int(df_train['Age'].min())
age_max = int(df_train['Age'].max())
age_slider = pn.widgets.IntRangeSlider(name='Age Range', start=age_min, end=age_max, value=(age_min, age_max))
x_dropdown = pn.widgets.Select(name='X Axis', options=list(df_train.columns), value='Age')
y_dropdown = pn.widgets.Select(name='Y Axis', options=list(df_train.columns), value='Attrition')

# Define plot functions
def create_histogram(attrition_df):
    return attrition_df.hvplot.hist(y='Attrition', bins=2, title='Attrition Histogram', xlabel='Attrition', ylabel='Count')

def create_scatter(attrition_df, x_axis, y_axis):
    return attrition_df.hvplot.scatter(x=x_axis, y=y_axis, color='Attrition', marker='o', cmap='viridis', title='Attrition Scatter Plot', xlabel=x_axis, ylabel=y_axis)

# Define layout
sidebar = pn.Column(pn.pane.Markdown("# Employee Attrition Dash"),
                    pn.pane.Markdown("#### Employee Attrition data visualization."),
                    pn.pane.PNG('https://icons.iconarchive.com/icons/graphicloads/100-flat/256/bank-icon.png'),
                    pn.pane.Markdown("## Settings"),
                    age_slider)

main = pn.Row(create_histogram(df_train), create_scatter(df_train, x_dropdown.value, y_dropdown.value))
layout = pn.template.FastListTemplate(title='Employee Attrition Visualization Dashboard', sidebar=sidebar, main=main)

# Define update function
@pn.depends(age_slider.param.value, x_dropdown.param.value, y_dropdown.param.value)
def update_plots(age_range, x_axis, y_axis):
    filtered_df = df_train[(df_train['Age'] >= age_range[0]) & (df_train['Age'] <= age_range[1])]
    main[0] = create_histogram(filtered_df)
    main[1] = create_scatter(filtered_df, x_axis, y_axis)

# Link update function to age_slider widget
age_slider.param.watch(update_plots, ['value'])

# Update layout and show
layout.show()
