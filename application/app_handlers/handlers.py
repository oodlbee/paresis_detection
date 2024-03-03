from typing import Tuple
from datetime import datetime
from pathlib import Path
import subprocess
from tkinter import filedialog, END


def select_save_path(entry, dirictory:bool=False, init_file_name:str='', defaultextension:str=''):
    if dirictory:
        file_path = filedialog.askdirectory()
    else:
        file_path = filedialog.asksaveasfilename(initialfile=init_file_name, defaultextension=defaultextension)
    if file_path == None:
        return None
    entry.delete(0, END)
    entry.insert(0, file_path)
    return file_path


def select_file_path(entry):
    file_path = filedialog.askopenfilename()
    if file_path == None:
        return None
    entry.delete(0, END)
    entry.insert(0, file_path)
    return file_path


def find_windows_center(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    return center_x, center_y


def get_max_video_size(root, padx: int = 200, pady: int = 250):
    video_width, video_height = root.winfo_screenwidth() - padx, root.winfo_screenheight() - pady
    if video_width >= 1280:
        video_width = 1280
    if video_height >= 720:
        video_height = 720
    return int(video_width), int(video_height)


def video_redecoding(input_file: Path, temp_video_file: Path, video_box: Tuple[int, int]):
    ffmpeg_path = Path.cwd()/'ffmpeg/bin/ffmpeg'
    widht, height = video_box
    command = f"{ffmpeg_path} -y -i {input_file} -vf scale={widht}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2 -c:v libx264 -g 1 -b:v 720k {temp_video_file}"
    subprocess.run(command, shell=True)
    return temp_video_file

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