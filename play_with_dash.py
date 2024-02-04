import threading
import random
import logging
import dash
import dash_daq as daq
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import wordle
from inf_player import InfPlayer
from utils import create_colorful_letters_row, create_current_words_table, str_to_float_list

game = wordle.Game()
player = InfPlayer(game)

# Dash App for displaying stats
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
words_to_pick = list(player.current_distribution[:10]['word'])

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Wordle Game Statistics"))),
    dbc.Row([
        dbc.Col(html.Div(id='keyboard-status')),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                daq.ToggleSwitch(
                    id='is_dist_sorted-switch',
                    value=False)
            ),
            md=2),

        dbc.Col(
            html.Div(
                dcc.Input(
                    placeholder='Enter a valid, five letter word to see its distribution...',
                    type='text',
                    value='',
                    id='word-picker',
                    style={'width': '100%'},  # Input field filling the outer div
                )),
            md=8),
        dbc.Col(
            html.Div(
                daq.ToggleSwitch(
                    id='entropy_ascending-switch',
                    value=False)
            ),
            md=2),
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='entropy-info'), width=2),
        dbc.Col(html.Div(id='word-histogram'), width=8),
        dbc.Col(html.Div(id='actual-possibilities'), width=2)

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
    input("")
    game.play(player, random.choice(game.VALID_SOLUTIONS))


game_thread = threading.Thread(target=play_game)
game_thread.start()


@app.callback(
    Output('actual-possibilities', 'children'),
    Output('actual-num-possibilities', 'children'),
    Output('keyboard-status', 'children'),
    Input('entropy_ascending-switch', "value"),
    Input('interval-component', 'n_intervals'),
)
def update_dropdown(entropies_sorted, value):
    current_words = player.current_distribution.copy().sort_values(by="entropy", ascending=entropies_sorted)
    words = list(current_words['word'])
    keyboard_row = create_colorful_letters_row(player.keyboard_status)
    return \
        create_current_words_table(current_words), \
            f"Numbers of actual possible words: {len(words)}", \
            keyboard_row,


@app.callback(
    Output('entropy-info', 'children'),
    Output('word-histogram', 'children'),
    Input('is_dist_sorted-switch', "value"),
    Input('word-picker', 'value'),
)
def update_metrics(dist_sorted, word):
    # Assuming player.current_distribution and player.keyboard_status don't change often,
    # consider updating them outside the callback if possible
    # Check if word is selecte  d, if not, avoid computations
    word = word.upper()
    if len(player.actual_possibilities) <= 1:
        return html.H1("You won. Congratulations.")
    if word and len(word) == 5:
        current_words = player.current_distribution
        try:
            if dist_sorted:
                dist = sorted(str_to_float_list(current_words[current_words['word'] == word]['distribution'].values[0]),
                              reverse=True)
            else:
                dist = str_to_float_list(current_words[current_words['word'] == word]['distribution'].values[0])
        except:
            dist = []
        if len(dist) > 0:
            histogram = go.Figure(data=[go.Bar(y=dist)],
                                  layout=go.Layout(xaxis=dict(showticklabels=False)))  # Hide x-axis labels
        else:
            return None,html.H3("Word is not valid.")
    elif len(word) > 5:
        return None,html.H3("Word is too long. Pick five letter word.")
    else:
        return None,None
    try:
        return (
            html.H3(f"H(X) =  {current_words[current_words['word'] == word]['entropy'][0]}",style={"align":"center"}),dcc.Graph(id="hist", figure=histogram),
        )
    except:
        return ( html.P(),dcc.Graph(id="hist", figure=histogram))


if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
    app.run_server(debug=False)