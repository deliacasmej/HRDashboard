pip install dash

import pandas as pd
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
vdem_df = pd.read_csv("Vdata.csv") 

vdem_df = vdem_df[['country_name', 'year', 'v2x_libdem']]
vdem_df = vdem_df.rename(columns={"country_name": "Country", "year": "Year", "v2x_libdem": "Liberal Democracy Index"})

# Initializes the Dash app
app = dash.Dash(__name__)

# Defines the layout of the app
app.layout = html.Div([
    dcc.RangeSlider(
        id='year-slider',
        min=vdem_df['Year'].min(),
        max=vdem_df['Year'].max(),
        value=[vdem_df['Year'].min(), vdem_df['Year'].max()],
        marks={str(year): str(year) for year in range(vdem_df['Year'].min(), vdem_df['Year'].max() + 1, 5)},
        step=1
    ),
    dcc.Graph(id='democracy-index-map'),
])

# Defines callback to update map based on the selected year range
@app.callback(
    Output('democracy-index-map', 'figure'),
    [Input('year-slider', 'value')]
)
def update_map(year_range):
    # Filters the DataFrame based on the selected year range
    filtered_df = vdem_df[(vdem_df['Year'] >= year_range[0]) & (vdem_df['Year'] <= year_range[1])]
    # Groups by Country and take the average of the selected metric over the period
    avg_df = filtered_df.groupby("Country", as_index=False)['Liberal Democracy Index'].mean()

    # Creates a choropleth map
    fig = px.choropleth(avg_df,
                        locations="Country",
                        locationmode='country names',
                        color="Liberal Democracy Index",
                        color_continuous_scale="Blues",
                        title="Average Liberal Democracy Index by Country (Selected Years)")
    return fig

# Runs the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
