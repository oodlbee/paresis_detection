from typing import Tuple

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