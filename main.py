from woah import csv_refactor
import get_osu_maps, osu_file_filter, ai_generate


def main():
    osu_map_id = input("Map id: ")
    try:
        get_osu_maps.get_single_map(osu_map_id)
        osu_file_filter.filter_files(folder_name="tests", is_training=False)
        csv_refactor.create_csv(is_training=False)
        with open("request.csv", "r") as request:
            actual_value = request.readlines()[1].split(",")[0]
        prediction = ai_generate.AI_query("request.csv")[0][0]
        result = f"Die vorhergesagte Schwierigkeit ist {str(prediction)}, die eigentliche Schwierigkeit ist {actual_value}."
        print(result)
    except (ValueError, UnicodeDecodeError):
        print("Bitte Versuche eine andere id")
    except ConnectionError:
        print("Die API ist zur Zeit offline")
    
if __name__ == "__main__":
    main()