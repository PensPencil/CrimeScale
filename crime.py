import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import json
import numpy as np

app = Dash(__name__)
server = app.server
india = json.load(open(r"C:\Users\siddh\Projects\CrimeScale\states_india.geojson"))
state_id_map = {}
for feature in india['features']:
    feature['id'] = feature['properties']['state_code']
    state_id_map[feature['properties']['st_nm']] = feature['id']

df = pd.read_csv(r"C:\Users\siddh\Projects\CrimeScale\project_base.csv")
df['id'] = df['STATE/UT'].apply(lambda x:state_id_map[x])


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Statewise Crime Scale", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_crime",
                 options=[
                     {"label": "Murder", "value": "MURDER"},
                     {"label": "Homicide", "value": "HOMICIDE"},
                     {"label": "Hit & Run", "value": "HIT AND RUN"},
                     {"label": "Assault on Women", "value": "ASSAULT ON WOMEN"},
                     {"label": "Kidnapping", "value": "KIDNAPPING AND ABDUCTION"},
                     {"label": "Human Trafficking", "value": "HUMAN TRAFFICKING"},
                     {"label": "Rape", "value": "RAPE"}],
                 multi=False,
                 value="MURDER",
                 style={'width': "35%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_map', component_property='figure')],
    [Input(component_id='slct_crime', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Analysis for {} counts in India for the year 2021-2022.".format(option_slctd)

    dff = df.copy()
    dff['CrimeScale'] = np.log10(dff[option_slctd])
    # Plotly Express
    fig = px.choropleth_mapbox(
        data_frame=dff,
        locations='id',
        geojson = india,
        color='CrimeScale',
        color_continuous_scale="Aggrnyl",#Aggrnyl Sunsetdark
        hover_name = 'STATE/UT',
        # hover_data = [option_slctd]
        hover_data = {option_slctd:True,
                      'id':False,
                      'CrimeScale':':.3f'},
        mapbox_style="carto-positron",#carto-positron stamen-watercolor
        center={'lat':24,'lon':78},
        zoom=2.5,
        opacity=0.5
    )
    return container, fig
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)