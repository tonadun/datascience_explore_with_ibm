# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create the dictionary
all_sites_option = {'label': 'All Sites', 'value': 'ALL'}
# Append the dictionary to your options array
all_options = [all_sites_option] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites

                                dcc.Dropdown(id='site-dropdown',
                                    options=all_options,
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Launch Site wise Success Rate')
        return fig
    else:
        # filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # outcomes = np.where(filtered_df['class'] == 1, 'success', 'fail')
        # filtered_df['outcome'] = outcomes
        # fig = px.pie(filtered_df, values='outcome', 
        # names='outcome', 
        # title='Success Rate on ')
        # return fig

        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    
        # Calculate the counts of success and failed outcomes
        success_count = filtered_df[filtered_df['class'] == 1].shape[0]
        fail_count = filtered_df[filtered_df['class'] == 0].shape[0]
        
        # Create labels and sizes for the pie chart
        labels = ['Success', 'Failed']
        sizes = [success_count, fail_count]
        
        # Plot the pie chart
        # Create a DataFrame for the pie chart
        pie_data = {'Outcome': ['Success', 'Failed'], 'Count': [success_count, fail_count]}
        pie_df = pd.DataFrame(pie_data)
        
        # Plot the pie chart
        fig = px.pie(pie_df, values='Count', names='Outcome', title='Success vs Failed Launches for {}'.format(entered_site))
    
        return fig
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
