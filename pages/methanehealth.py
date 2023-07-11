import dash

dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd



filename = r'C:\Users\akinola\PycharmProjects\DigitalMethaneTracking\Respiratory.csv'

df = pd.read_csv(filename)

dff = pd.DataFrame(df)

def create_time_series(data):

    fig = px.scatter(data, x='Year', y='Number_of_Death')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text='Death Caused by Respiratory Diseases')

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig
def refine_respiratory_data(data):
    Months = []
    Years = []
    for i in dff['Date']:
        text = i.replace(".", "")
        Years = text[5:9]
        month = text[0:3]
        # print(month)
        if month == 'Jan':
            Months.append(1)
        if month == 'Feb':
            Months.append(2)
        if month == 'Mar':
            Months.append(3)
        if month == 'Apr':
            Months.append(4)
        if month == 'May':
            Months.append(5)
        if month == 'Jun':
            Months.append(6)
        if month == 'Jul':
            Months.append(7)
        if month == 'Aug':
            Months.append(8)
        if month == 'Sep':
            Months.append(9)
        if month == 'Oct':
            Months.append(10)
        if month == 'Nov':
            Months.append(11)
        if month == 'Dec':
            Months.append(12)

    dff['Month'] = Months
    dff['Year'] = Years

    res_df = pd.DataFrame(
        {'State': dff.State, 'Year': dff.Year, 'Month': dff.Month, 'Cause_of Death': dff.Cause_of_death,
         'Num_Death': dff.Number_of_Death})
    return res_df

#df = px.data.tips()
new_df = refine_respiratory_data(dff)

uni_year = new_df['Year'].unique()


layout = html.Div(
    [
        html.Div([
            dcc.Dropdown(
            id="dropdown_series",
            options=[{"label": x, "value": x} for x in uni_year],
            value=uni_year[0],
            clearable=False,
        ),
            dcc.Graph(id="time-chart"),
        ]),

        html.Div([
            dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in uni_year],
            value=uni_year[0],
            clearable=False,
        ),
        dcc.Graph(id="bar-chart"),
        ])

    ]
)
@callback(Output("bar-chart", "figure"), Input("dropdown", "value"))
def update_bar_chart(day):
    mask = df["day"] == day
    fig = px.bar(df[mask], x="sex", y="total_bill", color="smoker", barmode="group")
    return fig

@callback(Output("time-chart", "figure"), Input("dropdown_series", "value"))
def update_bar_chart(year):
    mask = new_df[new_df["Year"] == year]

    fig = create_time_series(mask)
    return fig