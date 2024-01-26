import threading
import random
import logging
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import wordle
from informed_player import InformedPlayer
from utils import create_colorful_letters_row, create_current_words_table, str_to_float_list

game = wordle.Game()
player = InformedPlayer(game)

# Dash App for displaying stats
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
words_to_pick = list(player.current_distribution[:10]['word'])

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Wordle Game Statistics"))),
    dbc.Row([
        dcc.Dropdown(words_to_pick, words_to_pick[0], id='word-picker'),
        html.P(id='picked-word'),
        html.Div(id='dd-output-container')
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='keyboard-status')),
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='word-histogram'), width=9),
        dbc.Col(html.Div(id='actual-possibilities'), width=3)

    ]),
    dbc.Row([
        dbc.Col(html.Div(id='actual-num-possibilities'))
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    )
])


def play_game() -> object:
    global game, player
    game.play(player, random.choice(game.VALID_SOLUTIONS))


game_thread = threading.Thread(target=play_game)
game_thread.start()


@app.callback(
    Output('word-picker', 'options'),
    Output('actual-possibilities', 'children'),
    Output('actual-num-possibilities', 'children'),
    Output('keyboard-status', 'children'),
    Input('interval-component', 'n_intervals'),
)
def update_dropdown(value):
    current_words = player.current_distribution
    words = list(current_words['word'])
    keyboard_row = create_colorful_letters_row(player.keyboard_status)
    return words[:20], create_current_words_table(current_words), \
        f"Numbers of actual possible words: {len(words)}", \
        keyboard_row,


@app.callback(
    Output('word-histogram', 'children'),
    Input('word-picker', 'value'),
)
def update_metrics(word):
    # Assuming player.current_distribution and player.keyboard_status don't change often,
    # consider updating them outside the callback if possible

    # Check if word is selected, if not, avoid computations
    if word:
        current_words = player.current_distribution
        try:
            dist = sorted(str_to_float_list(current_words[current_words['word'] == word]['distribution'].values[0]),
                          reverse=True)
        except:
            dist = []
        if len(dist) > 0:
            histogram = go.Figure(data=[go.Bar(y=dist)])
        else:
            histogram = go.Figure()
    else:
        histogram = go.Figure()
    return (
        dcc.Graph(id="hist", figure=histogram),
    )


if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
    app.run_server(debug=False)
