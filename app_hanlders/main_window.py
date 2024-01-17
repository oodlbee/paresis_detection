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
        self.min_size = (300, 150)
        self.minsize(self.min_size[0], self.min_size[1])

        self.video_frame = tk.Frame(self, bd=10,  relief=tk.SOLID)
        self.videoplayer = TkinterVideo(master=self.video_frame, keep_aspect=True)
        self.videoplayer.load(video_path)
        self.video_frame.pack(fill=tk.X, expand=True)
        self.videoplayer.pack(fill=tk.X, expand=True)
        
        self.video_info = self.videoplayer.video_info()
        print(self.video_info)

        width = self.video_info['framesize'][0]
        hight = self.video_info['framesize'][1] + self.min_size[1]
        self.geometry(f"{width}x{hight}")
        
        self.glob_pause = True
        self.create_widgets()
        

    def update_scale(self, event=None):
        cur_frame= self.videoplayer.current_frame_number()
        self.progress_slider.set(cur_frame)

        td = timedelta(milliseconds=int(cur_frame/self.video_info["framerate"]*1000))
        self.start_time["text"] = f"{td.seconds//3600}:{td.seconds}:{td.microseconds//1000}"


    def update_video(self, event=None):
        cur_frame = int(self.progress_slider.get())
        self.videoplayer.seek(cur_frame)
        td = timedelta(milliseconds=int(cur_frame/self.video_info["framerate"]*1000))
        self.start_time["text"] = f"{td.seconds//3600}:{td.seconds}:{td.microseconds//1000}"

    def slider_seek_begin(self, event):
        """Function realised when first click on slider"""
        if self.videoplayer.pause() == False:
            self.videoplayer.pause()
        self.progress_slider.configure(command=self.update_video)


    def slider_seek_end(self, event):
        """Function realised when click realised from slider"""

        self.update_video()
        self.progress_slider.configure(command=None)
        # if self.glob_pause == False:
        #     self.videoplayer.play()
        



    def skip(self, value: int):
        """ skip seconds """
        self.media_player.next_frame()
        self.update_scale()
        print(self.media_player.get_position())



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



    def _resize(self, event):
        print("kek")
        self.main_frame.configure(width=event.width, height=150)
        # if self.main_frame.winfo_width() < self.min_size[0] or self.main_frame.winfo_height() < self.min_size[1]:
        #     self.main_frame.config(width=self.min_size[0], height=self.min_size[1])

    def create_widgets(self):

        self.main_frame = tk.Frame(self, borderwidth=10)
        self.tools_frame = tk.Frame(self.main_frame, borderwidth=2)
        # self.frame_tools = ttk.Frame(self, height=150)
        # self.frame_tools.pack(fill=tk.X, expand=True)
        # self.frame_tools.bind("<Configure>", self.resize)

        self.progress_slider = ctk.CTkSlider(self.main_frame, from_=0, to=self.video_info['frames_num'], button_color="#51A1FF")
        self.progress_slider.set(0)
        self.progress_slider.bind("<Button-1>", self.slider_seek_begin)
        self.progress_slider.bind("<ButtonRelease-1>", self.slider_seek_end)
    
        

        # self.exercise_frame = ttk.Frame(self)
        # self.to_from_frame = ttk.Frame(self)
        # self.play_frame = ttk.Frame(self)
        # self.time_save_frame = ttk.Frame(self)


        self.play_pause_btn = ttk.Button(self.tools_frame, text="Play", command=self.play_pause)
        self.skip_minus_5sec = ttk.Button(self.tools_frame, text="Skip -5 sec", command=lambda: self.skip(-5))
        self.skip_plus_5sec = ttk.Button(self.tools_frame, text="Skip +5 sec", command=lambda: self.skip(+5))
        

        exercise_label = ttk.Label(self.tools_frame, text="Выбор упражнения:")

        self.select_exercise = tk.StringVar()
        self.cb_exercise = ttk.Combobox(self.tools_frame, textvariable=self.select_exercise)
        self.cb_exercise['state'] = 'readonly'

        self.start_time = ttk.Label(self.tools_frame, text="00:00:00")

        td = timedelta(milliseconds=int(self.video_info["duration"]*1000))
        self.end_time = ttk.Label(self.tools_frame, text=f"{td.seconds//3600}:{td.seconds}:{td.microseconds//1000}")


        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.progress_slider.pack(fill=tk.X, padx=10, pady=(5, 5))

        self.tools_frame.pack(fill=tk.X, padx=10, pady=(5, 5))

        # self.exercise_frame.pack(side="left", expand=True)
        # self.to_from_frame.pack(side="left", expand=True)
        # self.play_frame.pack(side="left", expand=True)
        # self.time_save_frame.pack(side="left", expand=True)

        self.skip_minus_5sec.pack(side="left")
        self.play_pause_btn.pack(side="left")
        self.skip_plus_5sec.pack(side="left")

        exercise_label.pack(side="top")
        self.cb_exercise.pack(side="top")

        self.end_time.pack(side="right")
        self.start_time.pack(side="right")
        
        self.bind("<Configure>", self._resize)
        

        

        

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