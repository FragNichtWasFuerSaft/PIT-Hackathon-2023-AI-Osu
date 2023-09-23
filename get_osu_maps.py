import requests
import zipfile
import io
import os
import time

count = 0
sets = 3601
while(count < 10001):
    response = requests.get(f"https://api.chimu.moe/v1/search?amount=100&offset={sets}&min_diff=1&max_diff=8&min_bpm=0&max_bpm=999")
    if not response.status_code == 200:
        print("server problem or something fuck")
        time.sleep(5)
        sets += 1
        continue
    files = response.json()["data"]
    for osu_set in files:
        for osu_map in osu_set["ChildrenBeatmaps"]:
            with open(file=f"data/osumap{osu_map['BeatmapId']}.json", mode="w") as map_file:
                map_file.write(str(osu_map))
            link = f"https://api.chimu.moe/v1{osu_map['DownloadPath']}"
            print(link)
            map_zip_file = requests.get(link)
            if not map_zip_file.status_code == 200:
                print("Unable to get map_file_zip")
                os.remove(map_file.name)
                time.sleep(1)
                continue
            with zipfile.ZipFile(io.BytesIO(map_zip_file.content), mode="r") as zip:
                for z in zip.infolist():
                    if z.filename.endswith(".osu"):
                        z.filename = f"osumap{osu_map['BeatmapId']}.osu"
                        zip.extract(z, path="data/")
            count += 1
        sets += 1
    print(sets)
