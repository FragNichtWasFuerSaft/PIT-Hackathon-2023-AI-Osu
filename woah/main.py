from dataclasses import dataclass
from math import sqrt, pow

@dataclass
class HitObject:
    x: int
    y: int
    time: int
    object_type: int
    
    def from_string(string):
        segments = string.split(',')
        x = HitObject(
            int(segments[0]),
            int(segments[1]),
            int(segments[2]),
            int(segments[3]),
        )
        return x

MAP_ATTRIBUTES_CSV_HEAD = "\
min cursor speed, \
max cursor speed, \
avg cursor speed, \
map length seconds, \
hitobject type count 0, \
1, \
2, \
3, \
4, \
5, \
6, \
7, \
hitobject types per second 0, \
1, \
2, \
3, \
4, \
5, \
6, \
7, \n"

@dataclass
class MapAttributes:
    min_cursor_speed: float
    max_cursor_speed: float
    avg_cursor_speed: float
    map_length_seconds: float
    hitobject_type_counts: list[int]
    hitobject_types_per_second: list[float]
    
    def to_csv_row(self):
        hitobject_type_counts_str = ", ".join([str(x) for x in self.hitobject_type_counts])
        hitobject_types_per_second_str = ", ".join([str(x) for x in self.hitobject_types_per_second])
        return f"\
{self.min_cursor_speed}, \
{self.max_cursor_speed}, \
{self.avg_cursor_speed}, \
{self.map_length_seconds}, \
{hitobject_type_counts_str}, \
{hitobject_types_per_second_str}"

def analyze_map(hitobjects_text: str) -> MapAttributes:
    hitobjects = [HitObject.from_string(x.strip()) for x in hitobjects_text.split('\n') if len(x.strip()) > 0]
    
    if len(hitobjects) == 0:
        raise ValueError("No hit objects :(")
    
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
        
        print(f"hitobject {i}: object_type={hitobject.object_type} {delta_distance=} {delta_time_s=} {speed=}")
        
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
    
    map_length_s = float(map_length_ms) / 1000.0
    object_types_per_s = [x / map_length_s for x in object_type_counts]
    
    return MapAttributes(
        min_cursor_speed = min_speed,
        max_cursor_speed = max_speed,
        avg_cursor_speed = avg_speed,
        map_length_seconds = map_length_s,
        hitobject_type_counts = object_type_counts,
        hitobject_types_per_second = object_types_per_s,
    )

def main():
    print("hello world")
    
    with open("woah/hitobjects.txt", "r") as f:
        hitobjects = f.read()
    
    attributes: MapAttributes = analyze_map(hitobjects)
    
    with open("woah/properties.csv", "w") as f:
        f.write(MAP_ATTRIBUTES_CSV_HEAD)
        f.write(attributes.to_csv_row())
        
    print(attributes)

if __name__ == "__main__":
    main()