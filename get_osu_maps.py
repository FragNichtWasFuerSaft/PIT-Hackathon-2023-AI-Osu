import requests
import zipfile
import io
import os

def get_many_maps():
    count = 0
    sets = 1143
    downloaded = set()
    current = None
    try:
        while(count < 10001):
            response = requests.get(f"https://api.chimu.moe/v1/search?amount=100&offset={sets}&min_diff=8&max_diff=10&min_bpm=0&max_bpm=999")
            if not response.status_code == 200:
                print("server problem or something fuck")
                sets += 1
                continue
            files = response.json()["data"]
            for osu_set in files:
                if osu_set["HasVideo"]:
                    print("osu_set had video -> skip")
                    continue
                for osu_map in osu_set["ChildrenBeatmaps"]:
                    if osu_map['BeatmapId'] in downloaded:
                        continue
                    else:
                        downloaded.add(osu_map['BeatmapId'])
                    with open(file=f"data/osumap{osu_map['BeatmapId']}.json", mode="w", encoding="utf-8") as map_file:
                        current = map_file
                        map_file.write(str(osu_map))
                    link = f"https://api.chimu.moe/v1{osu_map['DownloadPath']}"
                    print(link)
                    map_zip_file = requests.get(link)
                    if not map_zip_file.status_code == 200:
                        print("Unable to get map_file_zip")
                        os.remove(map_file.name)
                        continue
                    with zipfile.ZipFile(io.BytesIO(map_zip_file.content), mode="r") as zip:
                        for z in zip.infolist():
                            if z.filename.endswith(".osu"):
                                z.filename = f"osumap{osu_map['BeatmapId']}.osu"
                                zip.extract(z, path="data/")
                    count += 1
                sets += 1
            print(sets)
    except KeyboardInterrupt :
        print(sets)
        if not os.path.exists(current.name.replace(".json", ".osu")):
            os.remove(current.name)

def get_single_map(map_id):
    response = requests.get(f"https://api.chimu.moe/v1/map/{map_id}")
    if response.status_code == 500:
        print("internal server error")
        raise ConnectionError
    if response.status_code == 404:
        print("Map not found")
        raise ValueError
    if not response.status_code == 200:
        print("There is a problem with the server")
        raise ValueError
    osu_map = response.json()
    with open(file=f"tests/osumap{osu_map['BeatmapId']}.json", mode="w", encoding="utf-8") as map_file:
        map_file.write(str(osu_map))
    link = f"https://api.chimu.moe/v1{osu_map['DownloadPath']}"
    map_zip_file = requests.get(link)
    if not map_zip_file.status_code == 200:
        print("Unable to get map_file_zip")
        os.remove(map_file.name)
        raise ValueError
    with zipfile.ZipFile(io.BytesIO(map_zip_file.content), mode="r") as zip:
        for z in zip.infolist():
            if z.filename.endswith(".osu"):
                z.filename = f"osumap{osu_map['BeatmapId']}.osu"
                zip.extract(z, path="tests/")
                print(f"successful map download {z.filename=}")
                break

if __name__ == "__main__":
    get_many_maps()