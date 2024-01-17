import mimetypes
import tkinter as tk
from videoplayer import TkinterVideo
from datetime import timedelta
import customtkinter as ctk

import time

from os import path
from handlers import find_windows_center, delete_widget
from tkinter import ttk, filedialog, PhotoImage
from tkinter.messagebox import showerror


class CaptureWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Toplevel Window')

        ttk.Button(self,
                text='Close',
                command=self.destroy).pack(expand=True)


        
class MarkWindow(tk.Toplevel):
    def __init__(self, parent, video_path):
        super().__init__(parent)
        self.title('Разметка видео')
        
        self.videoplayer = TkinterVideo(master=self, keep_aspect=True)
        self.videoplayer.load(video_path)
        self.videoplayer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.video_info = self.videoplayer.video_info()
        print(self.video_info)

        self.tools_hight = 150
        width = self.video_info['framesize'][0]
        hight = self.video_info['framesize'][1] + self.tools_hight
        self.geometry(f"{width}x{hight}")
        self.minsize(width, hight)
        
        self.glob_pause = True
        self.create_widgets()
        

    def _fromat_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        milliseconds = seconds % 1 * 100
        return "{:02}:{:02}:{:02}".format(int(minutes), int(seconds), int(milliseconds))


    def update_scale(self, event=None):
        cur_frame= self.videoplayer.current_frame_number()
        self.progress_slider.set(cur_frame)
        self.start_time["text"] = self._fromat_seconds(cur_frame/self.video_info['framerate'])


    def update_video(self, event=None):
        cur_frame = int(self.progress_slider.get())
        self.videoplayer.seek(cur_frame)
        self.start_time["text"] = self._fromat_seconds(cur_frame/self.video_info['framerate'])

    def slider_seek_begin(self, event):
        """Function realised when first click on slider"""
        if self.videoplayer.pause() == False:
            self.videoplayer.pause()
        self.progress_slider.configure(command=self.update_video)


    def slider_seek_end(self, event):
        """Function realised when click realised from slider"""

        self.update_video()
        self.progress_slider.configure(command=None)
        if self.glob_pause == False:
            self.videoplayer.play()


    def skip(self, next_frame: bool=True):
        """ skip seconds """
        cur_frame = self.videoplayer.current_frame_number()
        if next_frame:
            self.videoplayer.seek(cur_frame + 1)
        else:
            self.videoplayer.seek(cur_frame - 1)



    def play_pause(self, event=None):
        """ pauses and plays """
        if self.videoplayer.is_paused():
            self.glob_pause = False
            self.bind("<<UpdateScale>>", self.update_scale)
            self.videoplayer.play()
            self.play_pause_btn.config(text="Pause")
        else:
            self.glob_pause = True
            self.unbind("<<UpdateScale>>")
            self.videoplayer.pause()
            self.play_pause_btn.config(text="Resume")


    def video_ended(self, event):
        """ handle video ended """
        self.progress_slider.set(1)
        self.play_pause()


    def create_widgets(self):

        self.main_frame = tk.Frame(self, height=self.tools_hight)
        self.tools_frame = tk.Frame(self.main_frame)
        # self.frame_tools = ttk.Frame(self, height=150)
        # self.frame_tools.pack(fill=tk.X, expand=True)
        # self.frame_tools.bind("<Configure>", self.resize)

        self.progress_slider = ctk.CTkSlider(self.main_frame, from_=0, to=self.video_info['frames_num'], button_color="#51A1FF")
        self.progress_slider.set(0)
        self.progress_slider.bind("<Button-1>", self.slider_seek_begin)
        self.progress_slider.bind("<ButtonRelease-1>", self.slider_seek_end)
    


        self.play_pause_btn = ttk.Button(self.tools_frame, text="Play", command=self.play_pause)
        self.previous_frame = ttk.Button(self.tools_frame, text="Skip -5 sec", command=lambda: self.skip(next_frame=False))
        self.next_frame = ttk.Button(self.tools_frame, text="Skip +5 sec", command=self.skip)
        
        exercise_label = ttk.Label(self.tools_frame, text="Выбор упражнения:")

        self.select_exercise = tk.StringVar()
        self.cb_exercise = ttk.Combobox(self.tools_frame, textvariable=self.select_exercise)
        self.cb_exercise['state'] = 'readonly'

        self.start_time = ttk.Label(self.tools_frame, text="00:00:00")

        self.end_time = ttk.Label(self.tools_frame, text=self._fromat_seconds(self.video_info['duration']))


        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.progress_slider.pack(fill=tk.X, padx=10, pady=5)

        self.tools_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.previous_frame.pack(side="left")
        self.play_pause_btn.pack(side="left")
        self.next_frame.pack(side="left")

        exercise_label.pack(side="top")
        self.cb_exercise.pack(side="top")

        self.end_time.pack(side="right")
        self.start_time.pack(side="right")
        
        

        

        

    def create_mark():
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.video_folder = tk.StringVar()
        self.mark_folder = tk.StringVar()
        self.save_folder = tk.StringVar()
        self.wt_color = "#f8f8f8"
        ttk.Style().configure("TButton", relief="flat")

        window_width, window_height = 800, 400
        center_x, center_y = find_windows_center(self, window_width, window_height)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.configure(bg=self.wt_color)
        self.title('paresis detection')
        self.iconbitmap('./images/icon.ico')

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.resizable(False, False)

        self.create_widgets()


    def open_capture_window(self):
        capture_window = CaptureWindow(self)
        capture_window.grab_set()


    def check_video_path(self):
        video_path = self.video_folder.get()
        # Check if file exists
        if not path.isfile(video_path):
            return "Видеофайл не найден"
        # Check if file is a video
        mime_type, _ = mimetypes.guess_type(video_path)
        if not (mime_type and mime_type.startswith('video')):
            return "Неверный формат видеофайла"


    def open_mark_window(self):
        video_status = self.check_video_path()
        if video_status:
            showerror(title='Ошибка', message=video_status)
        else:
            capture_window = MarkWindow(self, self.video_folder.get())
            capture_window.grab_set()
        

    def create_widgets(self):

        def select_file_path(entry, save=False):
            if save:
                file_path = filedialog.asksaveasfilename(initialfile='results.csv')
            else:
                file_path = filedialog.askopenfilename()
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

        def create_video_row(self, label_text:str, pad_hight:int):
            row = 0
            pady = (pad_hight, 8)

            label = ttk.Label(self, text=label_text, anchor="e", width=12)
            label.grid(row=row, column=0, padx=(50, 0), pady=pady, sticky=tk.E)

            entry_video = ttk.Entry(self, width=50, textvariable=self.video_folder)
            entry_video.focus()
            entry_video.grid(row=row, column=1, padx=5, pady=pady, sticky=tk.EW)

            button_folder = ttk.Button(self, text="Поиск", command=lambda: select_file_path(entry_video))
            button_folder.grid(row=row, column=2, padx=5, pady=pady, sticky=tk.EW)

            button_video = ttk.Button(self, text="Запись", command=self.open_capture_window,)
            button_video.grid(row=row, column=3, padx=(5, 50), pady=pady, sticky=tk.EW)


        def create_mark_row(self, label_text:str):
            row = 1
            pady = 8

            label = ttk.Label(self, text=label_text, anchor="e", width=12)
            label.grid(row=row, column=0, padx=(50, 0), pady=pady, sticky=tk.EW)

            entry_mark = ttk.Entry(self, width=50, textvariable=self.mark_folder)
            entry_mark.grid(row=row, column=1, padx=(5, 5), pady=pady, sticky=tk.EW)

            button_folder = ttk.Button(self, text="Поиск", command=lambda: select_file_path(entry_mark))
            button_folder.grid(row=row, column=2, padx=5, pady=pady, sticky=tk.EW)

            button_marking = ttk.Button(self, text="Разметка", command=self.open_mark_window)
            button_marking.grid(row=row, column=3, padx=(5, 50), pady=pady, sticky=tk.EW)

        def create_save_row(self, label_text:str):
            row = 2
            pady = 8

            label = ttk.Label(self, text=label_text, anchor="e", width=12)
            label.grid(row=row, column=0, padx=(50, 0), pady=pady, sticky=tk.E)

            entry_save = ttk.Entry(self, width=50, textvariable=self.save_folder)
            entry_save.grid(row=row, column=1, padx=5, pady=pady, sticky=tk.EW)

            button_folder = ttk.Button(self, text="Поиск", command=lambda: select_file_path(entry_save, True))
            button_folder.grid(row=row, column=2, padx=5, pady=pady, sticky=tk.EW)

        create_video_row(self, "Видеофайл: ", pad_hight=90)
        create_mark_row(self, "Разметка: ")
        create_save_row(self, "Сохранять в: ")



if __name__ == "__main__":
    app = App()
    app.mainloop()