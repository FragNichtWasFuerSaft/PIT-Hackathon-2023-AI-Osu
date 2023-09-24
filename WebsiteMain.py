from dash import Dash, dcc, html, Input, Output, callback
from main import getLevelDifficulty

app = Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1(
            children = ["osu!Brokkoli"],
            style = {
                "text-align": "center"
            }
        ),
        html.Div(
            style={
                "width": "600px",
                "margin": "100px auto"
            },
            children=[
                dcc.Input(
                    id="_inputLevel",
                    type="text",
                    placeholder="input..."
                ),
                html.Div(
                    id="ergebnis"
                ),
                ##HEATMAAAP einbetten uwu uwu
                #html.Iframe(
                    #src="PIT-Hackathon-2023-AI-Osu/figures/heatmap.html",
                #    style={
                        #"display": "flex",
                        #"flex-direction": "column",
                #        "margin-left": "25px",
                #        "margin-right": "25px",
                #    },
                #),    
            ]
        )
    ]
)

@callback(Output("ergebnis","children"),  Input("_inputLevel", "value"))
def getPrediction(pInput):
    print("Hallo!")
    #try:
    temp =getLevelDifficulty(pInput)
    print(repr(temp))
    return temp
    #except:
    #    return "Falsche Eingabe!"


def update_output_div(input_value):
    return f"Output: {input_value}"


if __name__ == "__main__":
    app.run(debug=True)