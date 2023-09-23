
def strip_file():
    with open("woah/properties_old(15).csv", "r") as file:
        with open("woah/properties_new.csv", "w") as new_file:
            new_file.write(file.readline())
            for line in file.readlines()[1:]:
                if not float(line.split(",")[0]) > 12:
                    new_file.write(line)
        
if __name__ == "__main__":
    strip_file()