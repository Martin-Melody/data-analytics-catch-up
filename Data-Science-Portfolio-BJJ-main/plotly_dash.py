import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
from dash import dcc, html
# Setup MongoDB connection
uri = ""

# Create a new client and connect to the server
client = MongoClient(uri)  # replace with your MongoDB host and port
db = client['Bjj_data']
collection = db['bjj_data']
# Load the data
data = pd.DataFrame(list(collection.find({})))

# Exclude data where year is 0
# Data cleaning: remove rows with missing 'Year' or 'W/L' values
data_clean = data.dropna(subset=['Year', 'W/L'])

# Convert 'Year' to integer type
data_clean['Year'] = data_clean['Year'].astype(int)

# Remove rows where Year is 0 (these seem to be incomplete records)
data_clean = data_clean[data_clean['Year'] != 0]

# Exclude certain methods
exclude_methods = ['Pts', 'Points', 'Referee Decision', 'N/A']
data_clean = data_clean[~data_clean['Method'].isin(exclude_methods)]

# Get top 10 methods
top_methods = data_clean['Method'].value_counts().index[:10]
data_top_methods = data_clean[data_clean['Method'].isin(top_methods)]

# Get wins by team
wins_by_team = data_clean[data_clean['W/L'] == 'W']['Team'].value_counts()

# Prepare figures
fig_matches_per_year = px.histogram(data_clean, x='Year', nbins=len(data_clean['Year'].unique()), title='Number of Matches per Year', color_discrete_sequence=['#636EFA'])
fig_wins_losses = px.histogram(data_clean, x='W/L', title='Distribution of Wins and Losses', color_discrete_sequence=['#EF553B'])
fig_top_methods = px.histogram(data_top_methods, x='Method', title='Top 10 Most Common Winning Methods', color_discrete_sequence=['#00CC96']).update_xaxes(categoryorder='total descending')
fig_wins_by_team = px.bar(x=wins_by_team.index, y=wins_by_team.values, title='Wins by Team', color_discrete_sequence=['#AB63FA'])
team_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
data_clean.loc[:, 'Year'] = data_clean['Year'].astype(int)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout with the added sliders and dropdowns
app.layout = html.Div(style={'backgroundColor': '#d9d9d9'}, children=[
    dbc.Container([
        dbc.Row(dbc.Col(html.H1('Bjj data analysis'), width=12)),
        dbc.Row([
            dbc.Col(
                dcc.Slider(
                    id='year-slider',
                    min=data_clean['Year'].min(),
                    max=data_clean['Year'].max(),
                    value=data_clean['Year'].min(),
                    marks={
                        str(data_clean['Year'].min()): str(data_clean['Year'].min()),
                        str(data_clean['Year'].max()): str(data_clean['Year'].max())
                    },
                    step=1
                ),
                md=6),
            dbc.Col(
            dcc.Dropdown(
                id='method-dropdown',
                options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in data_clean['Method'].dropna().unique()],
                value='All'
            ),
    md=3),
dbc.Col(
    dcc.Dropdown(
    id='competition-dropdown',
    options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in data_clean['Competition'].dropna().unique()],
    value='All'
),

    md=3),

        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='graph-matches-per-year'), md=6),
            dbc.Col(dcc.Graph(id='graph-wins-losses'), md=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='graph-top-methods'), md=6),
            dbc.Col(dcc.Graph(id='graph-wins-by-team'), md=6),
        ]),

        html.Hr(),
        dbc.Button(
            "Show More Charts",
            id="collapse-button",
            className="mb-3",
            color="primary",
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody(
                [dcc.Graph(figure=px.histogram(data_clean[data_clean['Team'] == team]['Full Name'].value_counts().nlargest(5).reset_index(), x='index', y='Full Name', title=f'Top 5 Competitors for {team}', color_discrete_sequence=[team_colors[i]])) for i, team in enumerate(data_clean['Team'].value_counts().index[:10])]
            )),
            id="collapse",
        ),
    ], fluid=True)
])
@app.callback(
    [Output('graph-matches-per-year', 'figure'),
     Output('graph-wins-losses', 'figure'),
     Output('graph-top-methods', 'figure'),
     Output('graph-wins-by-team', 'figure')],
    [Input('year-slider', 'value'),
     Input('method-dropdown', 'value'),
     Input('competition-dropdown', 'value')]
)
def update_graphs(selected_year, selected_method, selected_competition):
    # Filter the data based on the selected values
    filtered_data = data_clean[data_clean['Year'] >= selected_year]
    
    if selected_method != 'All':
        filtered_data = filtered_data[filtered_data['Method'] == selected_method]
        
    if selected_competition != 'All':
        filtered_data = filtered_data[filtered_data['Competition'] == selected_competition]
    
    # Recreate the figures with the filtered data
    fig_matches_per_year = px.histogram(filtered_data, x='Year', nbins=len(filtered_data['Year'].unique()), title='Number of Matches per Year', color_discrete_sequence=['#636EFA'])
    fig_wins_losses = px.histogram(filtered_data, x='W/L', title='Distribution of Wins and Losses', color_discrete_sequence=['#EF553B'])
    fig_top_methods = px.histogram(filtered_data, x='Method', title='Top 10 Most Common Winning Methods', color_discrete_sequence=['#00CC96']).update_xaxes(categoryorder='total descending')
    fig_wins_by_team = px.bar(x=wins_by_team.index, y=wins_by_team.values, title='Wins by Team', color_discrete_sequence=['#AB63FA'])
    
    return fig_matches_per_year, fig_wins_losses, fig_top_methods, fig_wins_by_team

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [dash.dependencies.State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
