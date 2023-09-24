from woah import csv_refactor
import get_osu_maps, osu_file_filter, ai_generate

loaded_maps = ["3274515", "4043165", "4161318", "4197260", "4286288", "4315261"]

def main():
    osu_map_id = input("Map id: ")
    getLevelDifficulty(osu_map_id)


def getLevelDifficulty(osu_map_id):
    try:
        if osu_map_id not in loaded_maps:
            get_osu_maps.get_single_map(osu_map_id)
            osu_file_filter.filter_files(folder_name="tests", is_training=False)
            csv_refactor.create_csv(is_training=False)
        path = f"presentation/request{osu_map_id}.csv"
        with open(path, "r") as request:
            actual_value = request.readlines()[1].split(",")[0]
        prediction = ai_generate.AI_query(path)[0][0]
        result = f"Die vorhergesagte Schwierigkeit ist {str(round(prediction, 2))}, die eigentliche Schwierigkeit ist {actual_value}."
        print(result)
        return result
    except (ValueError, UnicodeDecodeError):
        print("Bitte Versuche eine andere id")
    except ConnectionError:
        print("Die API ist zur Zeit offline")
    
if __name__ == "__main__":
    main()