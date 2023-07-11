import dash

dash.register_page(__name__, path="/")

#from dash.dependencies import Input, Output
#import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import requests
from zipfile import ZipFile
import pandas as pd
import os
import wget
from datetime import datetime
from geopy.geocoders import Nominatim
import json

source_df = pd.read_csv('emissionsources.csv')

date_format = '%d/%m/%Y'
years =[]
months = []

for date in source_df['date']:
    # Convert the date string to a datetime object
    date = datetime.strptime(date, date_format)
    years.append(date.year)
    months.append(date.month)

source_df['Year'] = years
source_df['Month'] = months

source_year = source_df['Year'].unique()
def create_figure1(df, value):
    fig = px.scatter_mapbox(df, lat='lat', lon='lon',
                             size='emission',
                            color='emission',
                            animation_frame="Month",
                             title='Emissions in Year '+str(value), zoom=3, center={'lat': 0, 'lon': 0})

    # Update the map layout
    fig.update_layout(mapbox_style='carto-positron', hovermode='closest')
    return fig
#instantiate the App and incorporate BOOTSTRA theme stylesheet
#'https://codepen.io/chriddyp/pen/bWLwgP.css'
#__name__, external_stylesheets = [dbc.themes.LUX]
#__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
graphtitle = dcc.Markdown(children='')
#mygraph1 =
mygraph2 = dcc.Graph(figure={})
mygraph3 = dcc.Graph(figure={})

years = set()
#times = df['YEAR'].unique()
# incorporate data into App
def get_country_name(latitude, longitude):
    geolocator = Nominatim(user_agent='geoapiExercises')  # Create a geolocator instance
    location = geolocator.reverse((latitude, longitude), exactly_one=True)  # Reverse geocode coordinates
    if location is not None:
        address = location.raw['address']
        country = address.get('country', '')
        state = address.get('state', '')
        city = address.get('city', '')
        return country, state, city
    else:
        return None
def find_country_state_city(dff):
    country = []
    state = []
    city = []
    for point1, point2 in zip(dff['lat'], dff['lon']):
        country_name = get_country_name(point1, point2)
        country.append(country_name[0])
        state.append(country_name[1])
        city.append(country_name[2])

    sub_df = pd.DataFrame(
        {'Year': dff.Year, 'Month': dff.Month, 'emission': dff.emission, 'lat': dff.lat, 'lon': dff.lon,
         'country': country, 'state': state, 'city': city})
    return sub_df

def create_time_series(df, title):

    fig = px.scatter(df, x='Year', y='emission')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

def process_data_cusworth(df):
    return df
def process_data_copernicus(df):
    return df
def process_data_carbon_mapper(value):
    date_format = '%Y-%m-%dT%H:%M:%S'
    years = []
    months = []
    days = []
    if value is not None:
        for date in value['datetime']:
            # Convert the date string to a datetime object
            date = datetime.strptime(date, date_format)
            years.append(date.year)
            months.append(date.month)
            days.append(date.day)
        # value['Year'] = years
        # value['Month'] = months
        # value['Day'] = days
        emission = value['emission']
        lat = value['plume_lat']
        lon = value['plume_lon']
        sub_points_df = pd.DataFrame(
            {'Year': years, 'Month': months, 'Day': days, 'emission': emission, 'lat': lat, 'lon': lon})
        # print(sub_points_df.shape)
        cleaned_sub_df = sub_points_df.dropna()
        df_sorted = cleaned_sub_df.sort_values(['Year', 'Month'])

    return df_sorted

def combine_methane_data(value1, value2, value3):
    return value1

def create_figure2(dff):
    return dff

def create_figure3(dff):
    return dff

#app = dash.Dash(__name__, )
layout = html.Div([

    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo.png'),
                     id='Tech_Logo',
                     style={
                         "height": "100px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     ),
            html.Div([
                html.H1("Digital Methane Tracking"),
                html.H5("Tracking Impact of Emission on Health", style={"margin-top": "0px", 'color': '#1f2c56'}),

            ]),
        ], className = "six column", id = "title")

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.H6(children='Total Emission',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            html.P('Something goes here',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 20}
                   ),
            html.P('Something goes here',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15}
                   ),

        ], className="card_container three columns",
        ),
        html.Div([
            html.H6(children='Another Indicator',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            html.P('Something goes here',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 20}
                   ),
            html.P('Something goes here',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15}
                   ),
        ], className="card_container three columns",
        ),
        html.Div([
            html.H6(children='Total Deaths',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            html.P('Something goes here',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 20}
                   ),
            html.P('Something goes here',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15}
                   ),
        ], className="card_container three columns",
        ),
        html.Div([
            html.H6(children='Total Rate',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            html.P('Something goes here',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 20}
                   ),
            html.P('Something goes here',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15}
                   ),
        ], className="card_container three columns",
        ),
    ]),
    html.Div([
        html.Div([
            html.P('Data Platforms:', className='fix_label', style={'color': 'white'}),
            # html.Label('Data Platforms'),
            dcc.Dropdown(
                id='dropdown-1',
                options=[
                    {'label': 'Carbon Mapper Platform', 'value': 'Carbon Mapper Platform'},
                    {'label': 'Copernicus', 'value': 'Copernicus'},
                    {'label': 'Cusworth', 'value': 'Cusworth'},
                    {'label': 'CDC Wonder', 'value': 'CDC Wonder'}
                ],
                value=[],
                multi=True
            ),

            html.P('Carbon Mapper Data - Select Relevant Years:', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='dropdown-2', multi=True),
            html.Hr(),
            html.P('Copernicus Data - Select Relevant Methane Mix: ', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='dropdown-3'
                         ),
            # html.Label('Algorithm'),
            html.P('Algorithm: ', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id='dropdown-31',
                         ),

            html.P('Select Level:', className='fix_label', style={'color': 'white', 'margin-left': '1%'}),
            dcc.Dropdown(id='dropdown-311',
                         multi=True),
            html.P('Select Version:', className='fix_label', style={'color': 'white', 'margin-left': '1%'}),
            dcc.Dropdown(id='dropdown-312'
                         ),
            html.P('Select Year:', className='fix_label', style={'color': 'white', 'margin-left': '1%'}),
            dcc.Dropdown(id='dropdown-313',
                         multi=True
                         ),

        ], className="create_container three columns"),

        html.Div([
            dcc.Dropdown(id='select-years',
                         ),
                        dcc.Graph(figure={}, className="create_container 8 columns",
                            id='map-scatter',
                            #hoverData={'points': [{'customdata': ''}]},
                      )

        ], className="row flex-display"),
    ],className = "row flex-display"),

    html.Div([

        html.Div([
            dcc.Graph(id='time-series_line_1',
                      config={'displayModeBar': 'hover'}),
        ], className="create_container six columns"),
        html.Div([
            dcc.Dropdown(id='dropdown-bar',
                options=[{"label": x, "value": x} for x in source_year],
                         ),
            dcc.Graph(id='bar-chart1',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),
    ], className = "row flex-display"),

    html.Div(id='hover-data'),

    dcc.Store(id='methane-data', data=[], storage_type='memory'),
    dcc.Store(id='filtered-methane-data', data=[], storage_type='memory'),
    dcc.Store(id='cusworth-data'),
    dcc.Store(id='processed-methane-data'),
    dcc.Store(id='processed-cusworth-data'),
    dcc.Store(id='processed-copernicus-data'),
    dcc.Store(id='copernicus-data'),
    dcc.Store(id='health-data'),
    dcc.Store(id='processed-health-data'),
    dcc.Store(id='combined-methane-data'),
    dcc.Store(id='merged-data')

], id = "mainContainer", style = {"display": "flex", "flex-direction": "column"}
)
@callback(
    Output('dropdown-2', 'options'),
    Output('dropdown-3', 'options'),
    Input('dropdown-1', 'value'))
def update_dropdown_options(selected_values):
    #print('seen')
    options = []
    options2 = []
    if 'Carbon Mapper Platform' in selected_values:
        options.extend([
            {'label': 'Carbon Mapper-2016', 'value': '2016'},
            {'label': 'Carbon Mapper-2017', 'value': '2017'},
            {'label': 'Carbon Mapper-2019', 'value': '2019'},
            {'label': 'Carbon Mapper-2020', 'value': '2020'},
            {'label': 'Carbon Mapper-2021', 'value': '2021'},
            {'label': 'Carbon Mapper-2022', 'value': '2022'}
        ])

    if 'Copernicus' in selected_values:
        options2.extend([
            {'label': 'Column-averaged dry-air ', 'value': 'Column-averaged dry-air'},
            {'label': 'Mid-tropospheric column-averaged ', 'value': 'Mid-tropospheric column-averaged '}
        ])
    #if 'CDC Wonder' in selected_values:
    return options, options2

@callback(
    Output('methane-data', 'data'),
    Input('dropdown-2', 'value'))
def upload_dataset(selected_values):
    selected_years = [selected_values]
    raw_datasets = []
    each_year = selected_years[0]
    combined_df = []
    df = {}
    #print(each_year)
    cleaned_df = pd.DataFrame()
    #print(type(cleaned_df))
    #print(selected_years)
    if each_year is not None:
        #years.update(each_year)
        # print[selected_values]
        for yr in each_year:

            url = 'https://s3.us-west-1.amazonaws.com/msf.data/exports/plumes_' + str(yr) + '-01-01_' + str(
                yr) + '-12-31.zip'
            #print(url)
            req = requests.get(url)
            filename = url.split('/')[-1]
            #if os.path.exists(filename):
            with open(filename, 'wb') as file:
                file.write(req.content)
            #wget(url)
            print('ZIP file downloaded successfully.')

            with ZipFile(filename, 'r') as zip_object:
                file_names = zip_object.namelist()

                for file_name in file_names:
                    if file_name.endswith('.csv'):
                        zip_object.extract(file_name)
                        raw_data = pd.read_csv(file_name)
                        # Append the dataframe to the list
                        raw_datasets.append(raw_data)

                # Concatenate the dataframes into a single dataframe
        combined_df = pd.concat(raw_datasets, ignore_index=True)
        cleaned_df = process_data_carbon_mapper(combined_df)
        print(type(cleaned_df))
        #datasets = cleaned_df.to_json(orient='split', date_format='iso'),
        #df = pd.DataFrame(cleaned_df)
        #json_data = json.dumps(combined_df)
    return cleaned_df.to_dict('records')

@callback(
    Output('dropdown-31', 'options'),
    Input('dropdown-3', 'value'))
def update_subset(value):
    options = []
    if value is not None:
        if 'Column-averaged dry-air' == value:
            options = [
                {'label': 'SCIAMACHY and IMAP', 'value': 'sciamachy_imap'},
                {'label': 'SCIAMACHY and WFMD', 'value': 'sciamachy_wfmd'},
                {'label': 'TANSO2-FTS2 and SRPR', 'value': 'tanso2_fts2_srpr'},
                {'label': 'TANSO2-FTS2 and SRFP', 'value': 'tanso2_fts2_srfp'},
                {'label': 'TANSO-FTS and SRFP', 'value': 'tanso_fts_srfp'},
                {'label': 'TANSO-FTS and SRPR', 'value': 'tanso_fts_srpr'},
                {'label': 'MERGED and EMMA', 'value': 'merged_emma'},
                {'label': 'MERGED and OBS4MIPS', 'value': 'merged_obs4mips'},
                {'label': 'TANSO-FTS and OCFP', 'value': 'tanso_fts_ocfp'},
                {'label': 'TANSO-FTS and OCPR', 'value': 'tanso_fts_ocpr'}
            ]

        if 'Mid-tropospheric column-averaged' == value:
            options = [
                {'label': 'IASI (Metop-A) and NLIS', 'value': 'iasi_metop_a_nlis'},
                {'label': 'IASI (Metop-B) and NLIS', 'value': 'iasi_metop_b_nlis'},
                {'label': 'TANSO2-FTS2 and SRPR', 'value': 'tanso2_fts2_srpr'},
                {'label': 'TANSO2-FTS2 and SRFP', 'value': 'tanso2_fts2_srfp'}
            ]
    return options

@callback(
    Output('dropdown-311', 'options'),
    Output('dropdown-312', 'options'),
    Output('dropdown-313', 'options'),
    Input('dropdown-31', 'value'))
def update_subset1(value):
    levels = []
    versions = []
    a_years = []
    if value is not None:
        if 'sciamachy_imap' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '7.2', 'value': '7.2'},
            ]
            a_years = [
                {'label': '2003', 'value': '2003'},
                {'label': '2004', 'value': '2004'},
                {'label': '2005', 'value': '2005'},
                {'label': '2006', 'value': '2006'},
                {'label': '2007', 'value': '2007'},
                {'label': '2008', 'value': '2008'},
                {'label': '2009', 'value': '2009'},
                {'label': '2010', 'value': '2010'},
                {'label': '2011', 'value': '2011'},
                {'label': '2012', 'value': '2012'}
            ]
        if 'tanso2_fts2_srpr' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '2.0.0', 'value': '2.0.0'},
            ]
            a_years = [
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ]
        #  if 'sciamachy_wfmd' == value:
        #  levels = [
        #      {'label': 'Level 2', 'value': 'level_2'},
        #  ]
        #   versions = [
        #     ]
        #    a_years = [
        #       {'label': '2003', 'value': '2003'},
        #      {'label': '2004', 'value': '2004'},
        #     {'label': '2005', 'value': '2005'},
        #     {'label': '2006', 'value': '2006'},
        #     {'label': '2007', 'value': '2007'},
        #    {'label': '2008', 'value': '2008'},
        #     {'label': '2009', 'value': '2009'},
        #     {'label': '2010', 'value': '2010'},
        #     {'label': '2011', 'value': '2011'}
        #  ]
        if 'tanso_fts_ocfp' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '7.2', 'value': '7.2'},
                {'label': '7.3', 'value': '7.3'}
            ]
            a_years = [
                {'label': '2009', 'value': '2009'},
                {'label': '2010', 'value': '2010'},
                {'label': '2011', 'value': '2011'},
                {'label': '2012', 'value': '2012'},
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ]
        if 'tanso_fts_ocpr' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '7.2', 'value': '7.2'},
                {'label': '9.0', 'value': '9.0'}
            ]
            a_years = [
                {'label': '2009', 'value': '2009'},
                {'label': '2010', 'value': '2010'},
                {'label': '2011', 'value': '2011'},
                {'label': '2012', 'value': '2012'},
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ]
        if 'tanso_fts_srfp' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '2.3.8', 'value': '2.3.8'}
            ]
            a_years = [
                {'label': '2009', 'value': '2009'},
                {'label': '2010', 'value': '2010'},
                {'label': '2011', 'value': '2011'},
                {'label': '2012', 'value': '2012'},
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2019', 'value': '2019'}
            ]

        if 'tanso_fts_srpr' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '2.3.8', 'value': '2.3.8'},
                {'label': '2.3.9', 'value': '2.3.9'}
            ]
            a_years = [
                {'label': '2009', 'value': '2009'},
                {'label': '2010', 'value': '2010'},
                {'label': '2011', 'value': '2011'},
                {'label': '2012', 'value': '2012'},
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'}
            ]

        if 'merged_emma' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '4.3', 'value': '4.3'},
                {'label': '4.4', 'value': '4.4'}
            ]
            a_years = [
                {'label': '2003', 'value': '2003'},
                {'label': '2004', 'value': '2004'},
                {'label': '2005', 'value': '2005'},
                {'label': '2006', 'value': '2006'},
                {'label': '2007', 'value': '2007'},
                {'label': '2008', 'value': '2008'},
                {'label': '2009', 'value': '2009'},
                {'label': '2010', 'value': '2010'},
                {'label': '2011', 'value': '2011'},
                {'label': '2012', 'value': '2012'},
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ]

        if 'tanso2_fts2_srfp' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '2.0.0', 'value': '2.0.0'}
            ]
            a_years = [
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ]
        if 'merged_obs4mips' == value:
            levels = [
                {'label': 'Level 3', 'value': 'level_3'}
            ]
            versions = [
                {'label': '4.3', 'value': '4.3'},
                {'label': '4.4', 'value': '4.4'}
            ]
            a_years = [
            ]

        if 'iasi_metop_a_nlis' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '9.1', 'value': '9.1'}
            ]
            a_years = [
                {'label': '2007', 'value': '2007'},
                {'label': '2008', 'value': '2008'},
                {'label': '2009', 'value': '2009'},
                {'label': '2010', 'value': '2010'},
                {'label': '2011', 'value': '2011'},
                {'label': '2012', 'value': '2012'},
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ]

        if 'iasi_metop_b_nlis' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '9.1', 'value': '9.1'}
            ]
            a_years = [
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ]

        if 'iasi_metop_b_nlis' == value:
            levels = [
                {'label': 'Level 2', 'value': 'level_2'}
            ]
            versions = [
                {'label': '9.1', 'value': '9.1'}
            ]
            a_years = [
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ]

    return levels, versions, a_years

#@callback(
 #   Output('processed-methane-data', 'data'),
  #  Input('methane-data', 'data'))
#def clean_data_carbon_mapper(value_methane):
 #   datasets = {}

  #  if value_methane is not None:
   #     print(type(value_methane))
    #    dff = pd.DataFrame(value_methane)
     #   #df = pd.read_json(dff, orient='split')
    #    #print(value_methane.shape)
       # cleaned_df = process_data_carbon_mapper(df)
     #   datasets = df.to_json(orient='split', date_format='iso')
      #  print('progress4')
    #return datasets

@callback(
    Output('select-years', 'options'),
    #Output('filtered-methane-data', 'data'),
    Input('methane-data', 'data'))
def update_years(data):
    options = []
    if len(data) != 0:
        dff = pd.DataFrame(data)
        print(dff.columns.tolist())
       # print(type(dff))
       # print(dff.head())
        #df = pd.read_json(year_value, orient='split')
        yr = dff['Year'].unique()
        #print(yr)
        options = [int(num) for num in yr]

    return options

@callback(
    Output('map-scatter', 'figure'),
    Input('methane-data', 'data'),
    Input('select-years', 'value'))
def update_graph(data_value, value):
    fig = {}
    if len(data_value) != 0 and value is not None:
        #data = pd.read_json(data_value, orient='split')
        dff = pd.DataFrame(data_value)
        df = dff[dff['Year'] == value]
        fig = create_figure1(df, value)
        #print('progress')
    return fig
@callback(
    Output('time-series_line_1', 'figure'),
    Input('map-scatter', 'hoverData'),
    Input('methane-data', 'data'))
def update_y_timeseries(hoverData, value):

    if len(value) != 0 and hoverData is not None:
        lon = hoverData['points'][0]['lon']
        lat = hoverData['points'][0]['lat']
        print(lon)
        print(lat)
        country_details = get_country_name(lat, lon)
        print(country_details[0])
        print(country_details[1])
        print(country_details[2])

        df = value[value['lon'] == lon]
        dff = df[df['lat'] == lat]
        print(dff)
        print(get_country_name(lat, lon))
        fig = create_time_series(df, '')
        #fig = px.scatter(value, x='Year', y='emission')
    return fig
@callback(
    Output('bar-chart1', 'figure'),
    Input('dropdown-bar', 'value'))
def update_y_timeseries(val):
    mask = source_df[source_df["Year"] == val]
    fig = px.bar(mask, x="Month", y="emission", animation_frame="Month", color="ipcc", barmode="group")
    return fig

#@callback(Output('processed-cusworth-data', 'data'), Input('cusworth-data', 'value'))
#def clean_data_carbon_mapper(value):
 #   cleaned_df = process_data_carbon_mapper(value)
  #  return cleaned_df

#@callback(Output('processed-copernicus-data', 'data'), Input('copernicus-data', 'value'))
#def clean_data_carbon_mapper(value):
 #       # some expensive data processing step
  #  cleaned_df = process_data_carbon_mapper(value)
   # return cleaned_df.to_json(date_format='iso', orient='split')

#@callback(Output('combined-methane-data', 'data'), Input('processed-methane-data', 'value1'),Input('processed-cusworth-data', 'value2'),Input('processed-copernicus-data', 'value2'))
#def clean_data_copernicus(value1, value2, value3):
 #   dff = process_data_copernicus(value1)
  #  return dff.to_json(date_format='iso', orient='split')

