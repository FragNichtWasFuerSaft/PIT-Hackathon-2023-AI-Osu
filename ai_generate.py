import sklearn
from sklearn.datasets import load_diabetes
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import plotly.express as px 
from pandas import io
import pickle

def train_ai():
    #Daten einlesen
    data = pd.read_csv("woah/properties.csv").fillna(0)

    print(data.columns)
    #data_x, data_y = data(return_X_y= True, as_frame= True)
    data_x = data[["bpm", "mode", "approach_rate", "overall_difficulty", "circle_size", "hp_drain_rate", "total_length", "hit_length", "min_cursor_speed", "max_cursor_speed", 
    "avg_cursor_speed", "map_length_seconds", "hitobject_types_per_second_0", "1", "2", "3", "4", "5", "6", "7", "inherited_timing_points", "uninherited_timing_points", 
    "bpm_changes", "slider_multiplier_changes", "min_slider_multiplier", "max_slider_multiplier", "avg_slider_multiplier", "meter_changes", "min_meter", "max_meter", "avg_meter"]]

    data_y = data[["difficulty_rating"]]



    #Correllation matrix
    #Copy() notwendig, sonst zeigt data_merge auf data_x und data_y wird daran angehangen. Somit wäre das difficulty_rating Teil des Inputs,
    #das wollen wir nicht! :)
    data_merge = data_x.copy()
    data_merge["Target"]= data_y["difficulty_rating"]
    corr_matrix = data_merge.corr(numeric_only = True)

    print(data_x)
    print(data_x.describe())
    print(data_merge)
    print(corr_matrix)
    heatmap = px.imshow(corr_matrix.round(2), text_auto = True, title="Correlation Matrix")
    heatmap.show()
    heatmap.write_html("figures/heatmap.html")

    #Aufteilen der Daten in Test und Training
    #data_x = data_x[["age", "sex", "bmi", "bp", "s1", "s4", "s5", "s6"]]
    x_train, x_test, y_train, y_test = train_test_split(
        data_x, 
        data_y,
        test_size= 0.15
        )
    #Trainieren des Modells mit linearer Regression
    linear_model = LinearRegression()
    linear_model.fit(x_train, y_train)

    #Prediction des Modells gegen Target-Wert abgleichen
    print(linear_model.predict(x_test))
    print(y_test)

    #Genauigkeit des Modells ausgeben 
    y_true = y_test
    y_pred = linear_model.predict(x_test)
    print(r2_score(y_true, y_pred))

    #ToDo: Höhere Genauigkeit erzielen
    #-data_x und data_y auf Werte zwischen 0 und 1 bringen. -> Werte sind bereits normalisiert
    #DataFrames einmal anschauen

    pickle.dump(linear_model, open("OsuAI.pickle", "wb"))


def AI_query(pfad):
    linear_model = pickle.load(open("OsuAI.pickle", "rb"))

    #Daten einlesen, ohne "difficulty"
    data = pd.read_csv(pfad).fillna(0)
    data_x = data[["bpm", "mode", "approach_rate", "overall_difficulty", "circle_size", "hp_drain_rate", "total_length", 
    "hit_length", "min_cursor_speed", "max_cursor_speed", "avg_cursor_speed", "map_length_seconds",
    "hitobject_types_per_second_0", "1", "2", "3", "4", "5", "6", "7", "inherited_timing_points", "uninherited_timing_points", 
    "bpm_changes", "slider_multiplier_changes", "min_slider_multiplier", "max_slider_multiplier", "avg_slider_multiplier",
    "meter_changes", "min_meter", "max_meter", "avg_meter"]]

    #Modell macht seine Vorhersage
    prediction = linear_model.predict(data_x)

    #Correllation Matrix + ausgeben
    #data_merge = data_x.copy()
    #data_merge["Target"]= data[["difficulty_rating"]]
    #corr_matrix = data_merge.corr(numeric_only = True)
    #heatmap = px.imshow(corr_matrix.round(2), text_auto = True, title="Correlation Matrix")
    #heatmap.show()
    print(prediction)
    return prediction

if __name__ == "__main__":
    train_ai()