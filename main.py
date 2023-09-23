from woah import csv_refactor
import get_osu_maps, osu_file_filter, ai_generate


def main(osu_map_id):
    get_osu_maps.get_single_map(osu_map_id)
    osu_file_filter.filter_files("tests")
    csv_refactor.create_csv(is_training=False)
    