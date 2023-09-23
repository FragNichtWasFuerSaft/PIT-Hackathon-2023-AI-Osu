import os
import json
import ast

def find_line_start(all_lines, start_line):
    for i, line in enumerate(all_lines):
        if line.strip() == start_line:
            return i+1
    
    # nothing was found
    return None

    # Get the current directory where your Python script is located
script_dir      = os.path.dirname(__file__)
folder_name     = 'data'  
folder_path     = os.path.join(script_dir, folder_name)
file_names      = os.listdir(folder_path)
keynames        = {}

for file_name in file_names:
    if not file_name.endswith('.osu'):
        continue
    
    file_path = os.path.join(folder_path, file_name)
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
    except UnicodeDecodeError as e:
        print(f"Error in file {file_path=}")
        print(e)
        raise UnicodeDecodeError
    
    timing_points = []
    timing_point_start = find_line_start(all_lines, "[TimingPoints]")
    
    if timing_point_start is not None:
        for line in all_lines[timing_point_start:]:
            if line.strip() == "":
                break
            
            timing_points.append(line.strip())
    
    hit_objects = []
    hit_object_start = find_line_start(all_lines, "[HitObjects]")
    
    if hit_object_start is not None:
        for line in all_lines[hit_object_start:]:
            if line.strip() == "":
                break
            
            hit_objects.append(line.strip())
    
    json_file_path = file_path[:-4] + ".json"
    
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            corrected_file_content = json.dumps(ast.literal_eval(f.read()))
            json_content = json.loads(corrected_file_content)
    except FileNotFoundError as e:
        print(e)
    except UnicodeDecodeError as e:
        print(f"Issue in file {file_name=}")
        print(e)
        continue
    
    beatmap_id = json_content["BeatmapId"]
    difficulty_rating = json_content["DifficultyRating"]
    bpm = json_content["BPM"]
    mode = json_content["Mode"]
    approach_rate = json_content["AR"]
    overall_difficulty = json_content["OD"]
    circle_size = json_content["CS"]
    hp_drain_rate = json_content["HP"]
    total_length = json_content["TotalLength"]
    hit_length = json_content["HitLength"]
    
    out_json = {
        "beatmap_id": beatmap_id,
        "difficulty_rating": difficulty_rating,
        "bpm": bpm,
        "mode": mode,
        "approach_rate": approach_rate,
        "overall_difficulty": overall_difficulty,
        "circle_size": circle_size,
        "hp_drain_rate": hp_drain_rate,
        "total_length": total_length,
        "hit_length": hit_length,
        "timing_points": timing_points,
        "hit_objects": hit_objects,
    }
    
    imp_file_name = os.path.join("osu_files", file_name[:-4]+"_out.json")
    with open(imp_file_name, "w", encoding="utf-8") as data:
        # print("Created File!")
        data.write(json.dumps(out_json))
    ##Now The Difficulty tab is in the data file
