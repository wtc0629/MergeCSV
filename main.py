import pathlib
import json
import pandas as pd

pd.options.display.float_format = '{:}'.format


with pathlib.Path("C:\\Users\\51004\\Desktop\\MergeCSV\\Felix").joinpath("info.player.json").open() as file:
    meta_info = json.load(file)

start_timestamp_unix = meta_info["start_time_system_s"]
start_timestamp_pupil = meta_info["start_time_synced_s"]
start_timestamp_diff = start_timestamp_unix - start_timestamp_pupil

pupil_path = pathlib.Path('C:\\Users\\51004\\Desktop\\MergeCSV\\Felix\\pupil_positions.csv')
pupil_positions_df = pd.read_csv(pupil_path)

pupil_positions_df["pupil_timestamp_unix"] = pupil_positions_df["pupil_timestamp"] + start_timestamp_diff
pupil_positions_df["pupil_timestamp_datetime"] = pd.to_datetime(pupil_positions_df["pupil_timestamp_unix"], unit="s")

gaze_path = pathlib.Path('C:\\Users\\51004\\Desktop\\MergeCSV\\Felix\\gaze_positions.csv')
gaze_positions_df = pd.read_csv(gaze_path)
gaze_positions_df["gaze_timestamp_unix"] = gaze_positions_df["gaze_timestamp"] + start_timestamp_diff
gaze_positions_df["gaze_timestamp_datetime"] = pd.to_datetime(gaze_positions_df["gaze_timestamp_unix"], unit="s")

instruction_path = pathlib.Path('C:\\Users\\51004\\Desktop\\MergeCSV\\Felix\\instruction.csv')
instruction_df = pd.read_csv(instruction_path)
instruction_df["gaze_timestamp_datetime"] = pd.to_datetime(instruction_df["gaze_timestamp_unix"], unit="s")
print(gaze_positions_df)

print(instruction_df)
df_merged_gaze = pd.merge_asof(gaze_positions_df, instruction_df.sort_values('gaze_timestamp_datetime'),
                               on="gaze_timestamp_datetime", direction="nearest")
df_merged_pos = pd.merge_asof(pupil_positions_df, instruction_df.sort_values('gaze_timestamp_datetime'),
                              left_on="pupil_timestamp_datetime", right_on="gaze_timestamp_datetime",
                              direction="nearest")

# print(df_merged_pos)
df_merged_gaze.to_csv("C:\\Users\\51004\\Desktop\\MergeCSV\\Felix\\gaze_merged.csv")
df_merged_pos.to_csv("C:\\Users\\51004\\Desktop\\MergeCSV\\Felix\\pos_merged.csv")
