import cv2
import subprocess
import logging

from utils import timed_log
from typing import Tuple
from pathlib import Path
from tkinter import filedialog, END

from configparser import ConfigParser
config = ConfigParser()
config.read('application/app_config.ini')

logger = logging.getLogger('app_logger')


def select_save_path(entry, dirictory:bool=False, init_dir:str='', init_file_name:str='', defaultextension:str=''):
    """Creates ask window to select files or, if directory == True, get directory name"""
    if not Path(init_dir).is_dir():
        logger.debug(f'Init dir {init_dir} is not definded save dir')
        init_dir = ''

    if dirictory:
        if init_dir == '':
            file_path = filedialog.askdirectory()
        else:
            file_path = filedialog.askdirectory(initialdir=init_dir)
        logger.debug('Ask save directory window created')
    else:
        if init_dir == '':
            file_path = filedialog.asksaveasfilename(initialfile=init_file_name, defaultextension=defaultextension)
        else:
            file_path = filedialog.asksaveasfilename(initialdir=init_dir, initialfile=init_file_name, defaultextension=defaultextension)
        logger.debug('Ask save file path window created')
    if file_path == None or file_path == '':
        logger.debug('Empty path, nothing changes')
        return
    
    entry.delete(0, END)
    entry.insert(0, file_path)
    logger.debug('Entry is rewritten')
    return file_path


def select_file_path(entry, init_dir:str=''):
    if not Path(init_dir).is_dir():
        logger.debug(f'Init dir {init_dir} is not definded ask open')
        init_dir = ''

    if init_dir == '':
        file_path = filedialog.askopenfilename()
        logger.debug('Init dir is not definded open file')
    else:
        file_path = filedialog.askopenfilename(initialdir=init_dir)

    logger.debug('Ask open file window created')
    if file_path == None or file_path == '':
        logger.debug('Empty path, nothing changes')
        return
    entry.delete(0, END)
    entry.insert(0, file_path)
    logger.debug('Entry is rewritten')
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
    logger.info(f'Max video size is calculated as {int(video_width)}, {int(video_height)}')
    return int(video_width), int(video_height)


def get_init_video_info(input_file: Path):
    video = cv2.VideoCapture(str(input_file))
    if not video.isOpened():
        return None
    frame_num = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video.release()
    return frame_num
    

@timed_log(logger)
def video_redecoding(input_file: Path, temp_video_file: Path, video_box: Tuple[int, int]):
    ffmpeg_path = Path.cwd()/'ffmpeg/bin/ffmpeg'
    ffmpeg_logger_folder = Path(config['internal.files']['applications_loggers'][1:-1]).absolute()
    ffmpeg_logger_path = str(ffmpeg_logger_folder / Path('ffmpeg_logger.log'))
    widht, height = video_box

    # ffmpeg command makes scalig, decreasing bitrate and
    # makes every frame - keyframe
    command = f'''{ffmpeg_path} -y -i {input_file} -vf "scale='min({widht}, iw)':'min({height}, ih)':force_original_aspect_ratio=decrease" \
        -vsync passthrough \
        -g 1 -keyint_min 1 -sc_threshold 0 -c:v libx264 -preset faster -crf 28 \
        {temp_video_file} > {ffmpeg_logger_path} 2>&1'''
        # -c:a copy  {temp_video_file} > {ffmpeg_logger_path} 2>&1'''

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