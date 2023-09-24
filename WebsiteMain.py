from dash import Dash, dcc, html, Input, Output, callback

app = Dash(__name__)

app.layout = html.Div(
    children=[
        dcc.Input(
            id="_inputLevel",
            type="text",
            placeholder="input..."
        ),
        html.Div(
            id="ergebnis"
        ),
    ]
)

@callback(Output("ergebnis","children"),  Input("_inputLevel", "value"))
def getPrediction(pInput):
    try:
        return getLevelDifficulty(pInput) 
    except:
        return "Falsche Eingabe!"


def update_output_div(input_value):
    return f"Output: {input_value}"


if __name__ == "__main__":
    app.run(debug=True)