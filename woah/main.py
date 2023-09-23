from dataclasses import dataclass
from math import sqrt, pow
from os import listdir
from json import loads

@dataclass
class HitObject:
    x: int
    y: int
    time: int
    object_type: int
    
    def from_string(string):
        segments = string.split(',')
        return HitObject(
            int(segments[0]),
            int(segments[1]),
            int(segments[2]),
            int(segments[3]),
        )

@dataclass
class TimingPoint:
    time: float
    beatLength: float
    meter: int
    sampleSet: int
    sampleIndex: int
    volume: int
    uninherited: bool
    effects: int
    
    def from_string(string):
        segments = string.split(',')
        return TimingPoint(
            float(segments[0]),
            float(segments[1]),
            int(segments[2]),
            int(segments[3]),
            int(segments[4]),
            int(segments[5]),
            bool(int(segments[6])),
            int(segments[7]),
        )

MAP_ATTRIBUTES_CSV_HEAD = "\
min cursor speed, \
max cursor speed, \
avg cursor speed, \
map length seconds, \
hitobject types per second 0, \
1, \
2, \
3, \
4, \
5, \
6, \
7, \
inherited timing points, \
uninherited timing points, \
bpm changes, \
slider multiplier changes, \
min slider multiplier, \
max slider multiplier, \
avg slider multiplier, \
meter changes, \
min meter, \
max meter, \
avg meter\n"

@dataclass
class MapAttributes:
    beatmap_id: int
    bpm: int
    mode: int
    approach_rate: int
    overall_difficulty: int
    circle_size: int
    hp_drain_rate: int
    total_length: int
    hit_length: int
    min_cursor_speed: float
    max_cursor_speed: float
    avg_cursor_speed: float
    map_length_seconds: float
    hitobject_types_per_second: list[float]
    timing_point_inherited_counts_per_s: int
    timing_point_uninherited_counts_per_s: int
    bpm_changes_per_s: int
    slider_m_changes_per_s: int
    min_slider_multiplier: float
    max_slider_multiplier: float
    avg_slider_multiplier: float
    meter_changes_per_s: int
    min_meter: int
    max_meter: int
    avg_meter: float
    
    def to_csv_row(self):
        hitobject_types_per_second_str = ", ".join([str(x) for x in self.hitobject_types_per_second])
        return f"\
{self.min_cursor_speed}, \
{self.max_cursor_speed}, \
{self.avg_cursor_speed}, \
{self.map_length_seconds}, \
{hitobject_types_per_second_str}, \
{self.timing_point_inherited_counts_per_s}, \
{self.timing_point_uninherited_counts_per_s}, \
{self.bpm_changes_per_s}, \
{self.slider_m_changes_per_s}, \
{self.min_slider_multiplier}, \
{self.max_slider_multiplier}, \
{self.avg_slider_multiplier}, \
{self.meter_changes_per_s}, \
{self.min_meter}, \
{self.max_meter}, \
{self.avg_meter}"

def analyze_map(filtered_json: dict, hitobject_strings: list[str], timingpoint_strings: list[str]) -> MapAttributes:
    hitobjects = [HitObject.from_string(x) for x in hitobject_strings if len(x) > 0]
    
    if len(hitobjects) == 0:
        return None
    
    object_type_counts = [0, 0, 0, 0, 0, 0, 0, 0]
    map_length_ms = 0
    min_speed = 100000
    max_speed = -1
    # avg_speed is just a sum at first but it will be divided
    # by avg_speed_div at the end to make an average 
    avg_speed = 0
    avg_speed_div = 0
    
    prev: HitObject = hitobjects.pop(0)
    
    map_length_ms = prev.time
    
    if 0 <= prev.object_type <= 7:
        object_type_counts[prev.object_type] += 1
    
    for i, hitobject in enumerate(hitobjects):
        if 0 <= hitobject.object_type < 8:
            object_type_counts[hitobject.object_type] += 1
        
        if prev.time > map_length_ms:
            map_length_ms = prev.time
        
        delta_distance = sqrt(pow(hitobject.x - prev.x, 2) + pow(hitobject.y - prev.y, 2))
        delta_time_s = float(hitobject.time - prev.time) / 1000.0
        
        speed = None if delta_time_s == 0 else delta_distance / delta_time_s
        
        # print(f"hitobject {i}: object_type={hitobject.object_type} {delta_distance=} {delta_time_s=} {speed=}")
        
        if speed is not None:
            if speed < min_speed:
                min_speed = speed
            if speed > max_speed:
                max_speed = speed
            
            avg_speed += speed
            avg_speed_div += 1
        
        prev = hitobject
    
    if avg_speed_div > 0:
        avg_speed /= avg_speed_div
    
    map_length_s = float(map_length_ms + 1) / 1000.0
    object_types_per_s = [x / map_length_s for x in object_type_counts]
    
    
    # timing points
    timingpoints = [TimingPoint.from_string(x) for x in timingpoint_strings if len(x) > 0]
    
    timing_point_counts = [0, 0]
    bpm_changes = 0
    slider_m_changes = 0
    min_slider_multiplier = None
    max_slider_multiplier = None
    avg_slider_multiplier = 0
    avg_slider_multiplier_div = 0
    meter_changes = 0
    min_meter = None
    max_meter = None
    avg_meter = 0
    avg_meter_div = 0
    
    prev_bpm = None
    prev_slider_m = None
    prev_meter = None
    
    for timingpoint in timingpoints:
        uninherited = int(timingpoint.uninherited)
        timing_point_counts[uninherited] += 1
        
        if timingpoint.uninherited:
            bpm = 1.0 / timingpoint.beatLength * 1000 * 60
            
            if prev_bpm == None:
                prev_bpm = bpm
            elif abs(bpm - prev_bpm) > 0.01:
                prev_bpm = bpm
                bpm_changes += 1
            
            if prev_meter == None:
                prev_meter = timingpoint.meter
            elif prev_meter != timingpoint.meter:
                prev_meter = timingpoint.meter
                meter_changes += 1
            
            if min_meter == None or timingpoint.meter < min_meter:
                min_meter = timingpoint.meter
            if max_meter == None or timingpoint.meter > max_meter:
                max_meter = timingpoint.meter
            
            avg_meter += timingpoint.meter
            avg_meter_div += 1
            
        elif timingpoint.beatLength != 0.0:
            # inherited
            new_slider_m = 1.0 / (abs(timingpoint.beatLength) / 100.0)
            
            if prev_slider_m == None:
                prev_slider_m = new_slider_m
            elif abs(prev_slider_m - new_slider_m) > 0.01:
                prev_slider_m = new_slider_m
                slider_m_changes += 1
            
            if min_slider_multiplier == None or new_slider_m < min_slider_multiplier:
                min_slider_multiplier = new_slider_m
            if max_slider_multiplier == None or new_slider_m > max_slider_multiplier:
                max_slider_multiplier = new_slider_m
            
            avg_slider_multiplier += new_slider_m
            avg_slider_multiplier_div += 1
    
    if avg_meter_div > 0:
        avg_meter /= avg_meter_div
    if avg_slider_multiplier_div > 0:
        avg_slider_multiplier /= avg_slider_multiplier_div
    
    return MapAttributes(
        beatmap_id = filtered_json["beatmap_id"],
        bpm = filtered_json["bpm"],
        mode = filtered_json["mode"],
        approach_rate = filtered_json["approach_rate"],
        overall_difficulty = filtered_json["overall_difficulty"],
        circle_size = filtered_json["circle_size"],
        hp_drain_rate = filtered_json["hp_drain_rate"],
        total_length = filtered_json["total_length"],
        hit_length = filtered_json["hit_length"],
        min_cursor_speed = min_speed,
        max_cursor_speed = max_speed,
        avg_cursor_speed = avg_speed,
        map_length_seconds = map_length_s,
        hitobject_types_per_second = object_types_per_s,
        timing_point_inherited_counts_per_s = timing_point_counts[0] / map_length_s,
        timing_point_uninherited_counts_per_s = timing_point_counts[1] / map_length_s,
        bpm_changes_per_s = bpm_changes / map_length_s,
        slider_m_changes_per_s = slider_m_changes / map_length_s,
        min_slider_multiplier = min_slider_multiplier,
        max_slider_multiplier = max_slider_multiplier,
        avg_slider_multiplier = avg_slider_multiplier,
        meter_changes_per_s = meter_changes / map_length_s,
        min_meter = min_meter,
        max_meter = max_meter,
        avg_meter = avg_meter,
    )

def main():
    print("hello world")
    
    osu_out_filepaths = ["osu_files/" + x for x in listdir("osu_files") if x.endswith("_out.json")]
    print(osu_out_filepaths)
    
    def handle_out_filepath(filepath) -> MapAttributes:
        print(f"handling {filepath}")
        with open(filepath, "r") as f:
            filtered_json = loads(f.read())
        
        return analyze_map(filtered_json, filtered_json["hit_objects"], filtered_json["timing_points"])
    
    total_map_attributes = [handle_out_filepath(x) for x in osu_out_filepaths]
    
    with open("woah/properties.csv", "w") as f:
        f.write(MAP_ATTRIBUTES_CSV_HEAD)
        
        for attributes in total_map_attributes:
            if attributes is not None:
                f.write(attributes.to_csv_row() + "\n")
        
if __name__ == "__main__":
    main()