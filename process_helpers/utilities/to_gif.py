import glob
import os
import imageio
import numpy as np
import pandas as pd
from PIL import Image, ImageSequence
from pygifsicle import optimize

from tqdm import tqdm

from process_helpers.utilities.plotting import render_gantt_json


def unique_makespans(cols, csv_path):
    df = pd.read_csv(csv_path, names=cols)
    # Total Rows
    total_rows = len(df.index)
    # Count how often each cost appears
    makespans = df["cost"].value_counts()
    # print(makespans)
    # Keep the makespans that appear only once
    single_appearance = makespans[makespans == 1]
    # print(f"Found {len(single_appearance)} costs that only appear once")
    # print(f"\t\t{total_rows - len(single_appearance)} appear more than once")
    # Get the schedule ids where the cost is in the unique_makespans
    unique_schedule_ids = df[df["cost"].isin(single_appearance.index)]["schedule_id"]
    # print(unique_schedule_ids)
    # @TODO, look at the other schedules to find remaining unique schedules
    # Could json dump the "Packages part of the json
    return unique_schedule_ids


def to_gif(images_dir, gif_path, filename):
    path = images_dir + "*.png"

    imgs = glob.glob(path)

    name = gif_path + filename

    # Ensure the files are ordered by name
    # costs = [int(img.split("\\")[-1].split("-")[0]) for img in imgs]
    imgs = sorted(imgs, key=lambda x: int(x.split("\\")[-1].split("-")[0]))

    kargs = {'fps': 10}

    with imageio.get_writer(name, mode='I', **kargs) as writer:
        for id in tqdm(imgs):
            image = imageio.v2.imread(id)
            writer.append_data(image)

    # optimise_gif(name)


def optimise_gif(name):
    if os.name == 'nt':
        return
    print(f"Starting file size: {os.path.getsize(name) / 1000000} mb")

    # new_name = gif_path + filename.split('.')[0] + "optimized.gif"
    # optimize(gif_path + filename, new_name)
    optimize(name)

    print(f"Ending file size: {os.path.getsize(name) / 1000000} mb")


def gif_to_mp4(gif_path, filename):
    # starting file size

    # Convert to mp4
    # https://gist.github.com/gvoze32/95f96992a443e73c4794c342a44e0811
    # Ex. ffmpeg -i animated.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4
    no_ext = gif_path + filename.split('.')[0]
    os.system(
        f"ffmpeg -i {gif_path + filename} -movflags faststart -pix_fmt yuv420p -vf \"scale=trunc(iw/2)*2:trunc(ih/2)*2\" {no_ext}.mp4")
    print(f"Saved {no_ext}.mp4")
    print(f"Starting file size: {os.path.getsize(gif_path + filename) / 1000000} mb")
    print(f"Ending file size: {os.path.getsize(no_ext + '.mp4') / 1000000} mb")
    print(f"Factor of compression: {os.path.getsize(gif_path + filename) / os.path.getsize(no_ext + '.mp4')}")


def merge_gifs(prefix, gifs, output_filename):
    # merge the gifs in list files to a single sequential gif
    # Create an empty list to store the frames of the output GIF

    print(f"Creating {output_filename} from {prefix}")
    gif_paths = [prefix + "\\base\\" + name for name in gifs]
    imgs = np.vstack([imageio.v3.imread(path) for path in gif_paths])

    # Note: loop=0 means loop forever
    # Note2: duration = 1/fps * 1000 (ie. gap between two frames in ms)
    imageio.v3.imwrite(prefix + output_filename, imgs, duration=100, loop=0)

    print(f"Saved {prefix + output_filename}")


if __name__ == '__main__':
    pass
    # print("Rendering Gantt Charts as GIF")
    # dir_path = "/home/kali/PycharmProjects/Capstone/jobs/output/genetic/img/gif/abz5/"
    # gif_path = "/home/kali/PycharmProjects/Capstone/jobs/results/genetic/"
    # filename = "abz5_genetic.gif"
    # # to_gif(dir_path, gif_path, filename)
    # optimise_gif(gif_path + filename)
    # # gif_to_mp4(gif_path, filename)
