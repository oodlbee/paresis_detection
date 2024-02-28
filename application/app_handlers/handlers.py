from typing import Tuple
from datetime import datetime
from pathlib import Path
import tempfile
import subprocess
from tkinter import filedialog, END


def select_file_path(entry, save=False, markup=False):
    if save:
        if markup:
            init_file = 'markup.xlsx'
            file_path = filedialog.asksaveasfilename(initialfile=init_file)
        file_path = filedialog.askdirectory()
    else:
        file_path = filedialog.askopenfilename()
    entry.delete(0, END)
    entry.insert(0, file_path)
    return file_path


def find_windows_center(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    return center_x, center_y


def get_max_video_size(root, video_size: Tuple[int, int], pading: int = 200):
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    video_width, video_height = video_size
    aspect_ratio = video_width / video_height

    if screen_width > screen_height:
        result_width = screen_width - pading*2
        result_height = result_width // aspect_ratio 
    else:
        result_height = video_height - pading*2
        result_width = aspect_ratio // result_height

    return int(result_width), int(result_height)


def video_redecoding(input_file: Path):
    print(Path.cwd())
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_file_path = temp_file.name
    # date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    # name = "temp_video_" + date_str + ".mp4"
    # output_path = str(save_folder/name)
    # ffmpeg_path = "/usr/local/Cellar/ffmpeg/4.2.1_2/bin/ffmpeg"
    ffmpeg_path = Path.cwd()/'ffmpeg/bin/ffmpeg'
    command = f"{ffmpeg_path} -y -i {input_file} -vf scale=854:-1 -c:v libx264 -g 1 -b:v 720k {temp_file_path}"
    subprocess.run(command, shell=True)
    return temp_file_path

def delete_widget(widget):
    widget.pack_forget()

# def loading_gif(gif_path:str, event:str):
#     gif = Image.open(gif_path)
#     gif_frames = [ImageTk.PhotoImage(gif.copy().convert('RGBA')) for _ in range(gif.n_frames)]

#     global frame_num, gif_frames
#     frame_num
#     frame = gif_frames[frame_num]
#     frame_num = (frame_num + 1) % len(gif_frames)
#     gif_label.configure(image=frame)
#     root.after(100, animate_gif)