import glob
import os
from io import BytesIO
import imageio
from PIL import Image
from tqdm import tqdm


def to_gif(dir_path, gif_path, filename):

    path = dir_path + "*.png"
    imgs = glob.glob(path)

    # Ensure the files are ordered by name # List comprehension to get cost
    costs = [int(img.split("/")[-1].split("-")[0]) for img in imgs]

    imgs = sorted(imgs, key=lambda x: int(x.split("/")[-1].split("-")[0]))

    # Framerate: 60fps 16.6 ms per frame
    # Pass as kwarg
    kargs = {'fps': 60}

    with imageio.get_writer(gif_path + filename, mode='I', **kargs) as writer:

        for id in tqdm(imgs):
            image = imageio.v2.imread(id)
            writer.append_data(image)
    print(f"Saved {gif_path + filename}")


def gif_to_mp4(gif_path, filename):
    # starting file size

    size_as_bytes = os.path.getsize(gif_path + filename)


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
    to_gif(dir_path, gif_path, filename)
    gif_to_mp4(gif_path, filename)