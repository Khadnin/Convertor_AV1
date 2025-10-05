import numpy as np
import pandas as pd
import json
import sys

#přečtu JSON z stdin
#data_input example: {'video': 'path\\video.mp4', 'resolution': 8294400, 'frame_rate': '30', 'codec': 'h264', 'bit_rate': '47831095'}
#data_input = json.load(sys.stdin)

data_input = {"video": "path\\video.mp4", "resolution": 8294400, "frame_rate": "59.9", "codec": "h264", "bit_rate": "37831095"}

df = pd.read_excel("Bitrates_codecs.xlsx", sheet_name="bitrates")

bitrates = df.to_dict(orient="records")

resolutions_sorted = sorted(int(i) for i in df['Resolution'].unique())
fps_sorted = sorted(int(i) for i in df['FPS'].unique())


def checking_resolution(resolution_list, checked_resolution):
    i = 0
    j = 0
    while j == 0:
        if checked_resolution in resolution_list:
            result = {"max_res" : checked_resolution, "min_res" : checked_resolution}
            j += 1
        elif checked_resolution < resolution_list[-(i+1)] and checked_resolution > resolution_list[-(i+2)]:
            result = {"max_res" : resolution_list[-(i+1)], "min_res" : resolution_list[-(i+2)]}
            j += 1
        elif checked_resolution < resolution_list[i]:
            result = {"max_res" : resolution_list[i], "min_res" : 0}
            j += 1
        elif checked_resolution > resolution_list[-(i+1)]:
            result = {"max_res" : checked_resolution, "min_res" : resolution_list[-(i+1)]}  
            j += 1     
        i += 1
    return(result)

def checking_fps(fps_sorted, checked_fps):
    i = 0
    j = 0
    while j == 0:
        if checked_fps in fps_sorted:
            result = {"max_fps" : checked_fps, "min_fps" : checked_fps}
            j += 1
        elif checked_fps < fps_sorted[-(i+1)] and checked_fps > fps_sorted[-(i+2)]:
            result = {"max_fps" : fps_sorted[-(i+1)], "min_fps" : fps_sorted[-(i+2)]}
            j += 1
        elif checked_fps < fps_sorted[i]:
            result = {"max_fps" : fps_sorted[i], "min_fps" : 0}
            j += 1
        elif checked_fps > fps_sorted[-(i+1)]:
            result = {"max_fps" : checked_fps, "min_fps" : fps_sorted[-(i+1)]}
            j += 1
        i += 1
    return(result)

bitrate = int(data_input["bit_rate"]) / 1000000

codec_video = {"codec" : data_input["codec"]}
resolution_video = (checking_resolution(resolutions_sorted, int(data_input["resolution"])))
fps_video = (checking_fps(fps_sorted, float(data_input["frame_rate"])))


def border_points(codec_video, resolution_video, fps_video, bitrates):
    combination = []
    for k1, v1 in codec_video.items():
        for k2, v2 in resolution_video.items():
            for k3, v3 in fps_video.items():
                combo = (v1, v2, v3)
                combination.append(combo)
    border_points_data = []
    i = 0
    for combo in combination:
        for codecs_bitrate in bitrates:
            if codecs_bitrate["Codec"] == combination[i][0] and codecs_bitrate["Resolution"] == combination[i][1] and codecs_bitrate["FPS"] == combination[i][2]:
                border_points_data.append(codecs_bitrate)
            else:
                pass
        i += 1
    return(border_points_data)

def bilinear_interpolation(res, fps, res1, res2, fps1, fps2, q11, q21, q12, q22):
    calculation = (q11 * (res2 - res) * (fps2 - fps) + q21 * (res - res1) * (fps2 - fps) + q12 * (res2 - res) * (fps - fps1) + q22 * (res - res1) * (fps - fps1)) / ((res2 - res1) * (fps2 - fps1))
    return(calculation)

def classify_video(borders, video_data):
    resolution_points = sorted({point['Resolution'] for point in borders})
    fsp_points = sorted({point['FPS'] for point in borders})
    res1, res2 = resolution_points[0], resolution_points[-1]
    fps1, fps2 = fsp_points[0], fsp_points[-1]

    def find_val(category, rx, ry):
            for row in borders:
                if int(row['Resolution'])==int(rx) and float(row['FPS'])==float(ry):
                    return float(row[category])

    categories = {}
    for category in ("Excelent", "Good", "OK", "Bad"):
        q11 = find_val(category, res1, fps1)
        q21 = find_val(category, res2, fps1)
        q12 = find_val(category, res1, fps2)
        q22 = find_val(category, res2, fps2)
        val = bilinear_interpolation(video_data['resolution'], float(video_data['frame_rate']), res1, res2, fps1, fps2, q11, q21, q12, q22)
        categories[category] = float(val)

    # convert video bitrate to Mbps
    bitrate = float(data_input["bit_rate"]) / 1000000

    # classify (Excelent highest)
    if bitrate >= categories['Excelent']:
        clas = "Excelent"
    elif bitrate >= categories['Good']:
        clas = "Good"
    elif bitrate >= categories['OK']:
        clas = "OK"
    else:
        clas = "Bad"

    return {data_input["video"]: clas}

result = classify_video(border_points(codec_video, resolution_video, fps_video, bitrates), data_input)
print(result)

#data_output = XXX

#pošlu zpět
#json.dump(data_output, sys.stdout)