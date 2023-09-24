import os, json
from os import path

from woah import csv_refactor
import get_osu_maps, osu_file_filter, ai_generate

def main():
    osu_map_id = input("Map id: ")
    
    try:
        if not path.exists("tests"):
            os.makedirs("tests")
        if not path.exists("osu_files"):
            os.makedirs("osu_files")
        if not path.exists("test_osu_files"):
            os.makedirs("test_osu_files")
    except IOError as e:
        print("Could not create necessary directories.")
        print(e)
        return
    
    try:
        with open("trained_ids.json", "r") as f:
            trained_ids = json.loads(f.read())
    except IOError as e:
        print("Could not determine if the given ID has been used during training.")
        print(e)
    
    if osu_map_id in trained_ids:
        print("Your map has been used for training the AI already. Still continuing the prediction.")
    
    try:
        get_osu_maps.get_single_map(osu_map_id)
        osu_file_filter.filter_files(folder_name="tests", is_training=False)
        csv_refactor.create_csv(is_training=False)
        with open("request.csv", "r") as request:
            actual_value = request.readlines()[1].split(",")[0]
        prediction = ai_generate.AI_query("request.csv")[0][0]
        result = f"Die vorhergesagte Schwierigkeit ist {str(round(prediction, 2))}, die eigentliche Schwierigkeit ist {actual_value}."
        print(result)
    except (ValueError, UnicodeDecodeError):
        print("Bitte Versuche eine andere id")
    except ConnectionError:
        print("Die API ist zur Zeit offline")
    
if __name__ == "__main__":
    main()