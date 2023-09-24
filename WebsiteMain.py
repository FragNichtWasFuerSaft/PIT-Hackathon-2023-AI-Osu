from dash import Dash, dcc, html, Input, Output, exceptions, callback
import pandas as pd
import dash_bootstrap_components as dbc
from main import getLevelDifficulty 

# 3 tab: korrelation zwischen achsen als diagramm

app = Dash(__name__)
#app.scripts.config.serve_locally = True
#app.css.config.serve_locally = True
#app.config.suppress_callback_exceptions = True
#callback = app.callback

app.layout = html.Div(
    
    children=[

        dcc.Input(
            id="input",
            type="text",
            placeholder="input..."
        ),
        html.Div(
            id="ergebnis"
        ),


        ##HEATMAAAP einbetten uwu uwu
        html.Iframe(
            src="PIT-Hackathon-2023-AI-Osu/figures/heatmap.html",
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-left": "25px",
                "margin-right": "25px",
            },
        )    
    ],
)

@callback(Output("ergebnis","children"),  Input("input", "value"))
def getPrediction(pInput):
    try:
        return getLevelDifficulty(pInput) 
    except:
        return "Falsche Eingabe!"

#application = app.server
#application.run(debug=False)
app.run()