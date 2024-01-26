from dash import html, dcc
import dash_bootstrap_components as dbc
import wordle


def letter_states_to_colors(letter_states_dict):
    # Define a mapping from the enum to string
    state_to_string = {
        wordle.LetterStates.CORRECTPOSITION: 'green',
        wordle.LetterStates.NOTPRESENT: 'black',
        wordle.LetterStates.NOTGUESSEDYET: 'grey',
        wordle.LetterStates.INCORRECTPOSITION: 'orange'
    }
    # Use dictionary comprehension to create a new dictionary with the string values
    return {letter: state_to_string[state] for letter, state in letter_states_dict.items()}


def create_colorful_letters_row(letters_to_colors: dict):
    return dbc.Row(
        [dbc.Col(html.Div(letter, style={
            'color': 'white',
            'background-color': color,
            'border': '1px solid black',
            'text-align': 'center',
            'margin': '2px',
            'padding': '10px',
            'font-size': '20px',
            'width': '40px',
            'height': '40px',
            'display': 'inline-block'
        }), width=1) for letter, color in letter_states_to_colors(letters_to_colors).items()],
        justify="center"
    )


def str_to_float_list(input_str):
    input_str = str(input_str)
    # Remove square brackets and split the string by spaces
    stripped_str = input_str.strip("[]")
    split_str = stripped_str.split()

    # Convert each non-empty string to a float
    float_list = [float(num) for num in split_str if num]

    return float_list


def create_current_words_table(current_words):
    selected_df = current_words[['word', 'entropy']]
    size = selected_df.shape[0]
    if size > 15:
        size = 15
    try:
        return html.Div([
            html.Table(
                # Represent the DataFrame as a HTML table
                children=[html.Tr([
                    html.Th(col) for col in selected_df.columns
                ])] + [html.Tr([
                    html.Td(selected_df.iloc[i][col]) for col in selected_df.columns
                ]) for i in range(size)]
            )
        ])
    except:
        print("The number of words was", size)
        print(selected_df)
        return None
