import os

def find_line_start(all_lines, start_line):
    for i, line in enumerate(all_lines):
        if line.strip() == start_line:
            print(i+1)
            return i+1

    # Get the current directory where your Python script is located
script_dir      = os.path.dirname(__file__)
folder_name     = 'osu_files'  
folder_path     = os.path.join(script_dir, folder_name)
file_names      = os.listdir(folder_path)
start_line      = "[TimingPoints]"
end_line        = "\n"
keynames        = {}

for file_name in file_names:
    
    if file_name.endswith('.osu'):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r") as f:
            all_lines = f.readlines()
            imp_lines = []
            #Selecting important lines
            for line in all_lines[find_line_start(all_lines, start_line):]:
                    imp_lines.append(line)
                    if line == end_line:
                        break      
        imp_file_name = os.path.join(folder_name, file_name[:-4]+".json")
        with open(imp_file_name, "w") as data:
           print("Created File!")
           for imp_line in imp_lines:
            data.write(imp_line)
    ##Now The Difficulty tab is in the data file
