import glob
import os
import imageio
import pandas as pd
from PIL import Image
from pygifsicle import optimize

from tqdm import tqdm

from process_helpers.utilities.plotting import render_gantt_json


def gantt_gif_by_dataset(dataset, key, target_dir):
    """
    Identify unique schedules and create a gif for the given dataset
    """

    print("\nCreating Gantt GIF for: " + dataset)
    unique_schedule_ids = None
    csv_path = f"{target_dir}/results/{dataset}.csv"
    # Columns
    cols = key.split(",") + ["schedule_id"]
    # Load the file
    ids = unique_makespans(cols, csv_path)

    # If there are no unique schedules then we can't make a gif
    if len(ids) == 0:
        print(f"\tNo unique schedules found for {dataset}")
        return

    #
    # Create folders
    # {target_dir}/gif/{dataset}/
    # If {target_dir}/gif/{dataset}/ does not exist, create it
    img_path = f"{target_dir}/img/gif/{dataset}/"

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    for slurm in ids:
        json_path = f"{target_dir}json/{slurm}_gantt.json"
        render_gantt_json(file=json_path, outdir=img_path, img_subdir=False)

    # Create the gif

    frames = []
    path = img_path + "*.png"
    imgs = glob.glob(path)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(target_dir + dataset, format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=300, loop=0)


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


def minimal_animated_gantt(target_dir, key):
    """
    Make a gif to show each unique gantt chart
    """

    # To create the animation we need to identify unique schedules
    # if a schedule is the same then it will have the same makespan. but not all makespans are the same schedule.
    datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
    for dataset in datasets:
        gantt_gif_by_dataset(dataset, key, target_dir)

    # Create the frames
    frames = []
    path = target_dir + "img/gif/*/*.png"
    imgs = glob.glob(path)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(target_dir + "ALL.gif", format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=300, loop=0)
def to_gif(dir_path, gif_path, filename):

    path = dir_path + "*.png"
    imgs = glob.glob(path)
    name = gif_path + filename

    # Ensure the files are ordered by name # List comprehension to get cost
    costs = [int(img.split("/")[-1].split("-")[0]) for img in imgs]

    imgs = sorted(imgs, key=lambda x: int(x.split("/")[-1].split("-")[0]))

    # Framerate: 60fps 16.6 ms per frame
    # Pass as kwarg
    kargs = {'fps': 60}

    with imageio.get_writer(name, mode='I', **kargs) as writer:

        for id in tqdm(imgs):
            image = imageio.v2.imread(id)
            writer.append_data(image)
    print(f"Saved {name}")

    optimise_gif(name)


def optimise_gif(name):
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
    print(f"Ending file size: {os.path.getsize(no_ext + '.mp4')/ 1000000} mb")
    print(f"Factor of compression: {os.path.getsize(gif_path + filename) / os.path.getsize(no_ext + '.mp4')}")

if __name__ == '__main__':
    print("Rendering Gantt Charts as GIF")
    dir_path = "/home/kali/PycharmProjects/Capstone/jobs/output/genetic/img/gif/abz5/"
    gif_path = "/home/kali/PycharmProjects/Capstone/jobs/results/genetic/"
    filename = "abz5_genetic.gif"
    # to_gif(dir_path, gif_path, filename)
    optimise_gif(gif_path + filename)
    # gif_to_mp4(gif_path, filename)