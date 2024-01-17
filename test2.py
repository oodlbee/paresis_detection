import mimetypes
import tkinter as tk
import vlc
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
        self.is_paused = True
        self.loading_label = ttk.Label(self, text="loading...", anchor="e", width=12)
        self.loading_label.pack()

        self.initialize_player(video_path)
        self.loading_label.pack_forget()
        self.geometry(f"{self.media_info['framesize'][0]}x{self.media_info['framesize'][1]}")
        self.create_widgets()
        

    def initialize_player(self, video_path):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        
        
        media = self.instance.media_new(video_path)

        media.parse()
        media.get_mrl()
        self.media_player.set_media(media)
        self.media_canvas = tk.Canvas(self, bg="black", width=800, height=400)
        self.media_canvas.pack(pady=10, fill=tk.BOTH, expand=True)
        self.media_player.set_hwnd(self.media_canvas.winfo_id())
        self.media_player.play()
        time.sleep(0.001)
        self.media_paused = True
        self.media_player.set_pause(self.media_paused)
        self.media_info = {
            "duration": media.get_duration(),
            "framesize": self.media_player.video_get_size()
        }

        print(self.media_info)


    # def update_scale(self, event):
    #     """ updates the scale value """
    #     cur_frame = self.videoplayer.current_frame_number()
    #     cur_time = self.videoplayer.current_duration()
    #     self.progress_slider.set(cur_frame)
    #     print(cur_frame)
    #     print(str(timedelta(milliseconds=int(cur_time*1000))))
    #     td = timedelta(milliseconds=int(cur_time*1000))
    #     self.start_time["text"] = f"{td.seconds//3600}:{td.seconds}:{td.microseconds//1000}"
    #     # self.after(0, lambda: self.progress_slider.set(self.videoplayer.current_duration()))

    def update_scale(self, event=None):
        print('update_scale')
        if self.media_paused == False:
            self.frames += 1
            # cur_time = self.media_player.get_time()
            cur_pos = self.media_player.get_position()
            self.progress_slider.set(cur_pos)
            print(cur_pos, self.frames)
            

            td = timedelta(milliseconds=int(self.media_player.get_time()*1000))
            self.start_time["text"] = f"{td.seconds//3600}:{td.seconds}:{td.microseconds//1000}"
            # self.time_label.config(text=f"{current_time_str}/{total_duration_str}")
            # self.after(10, self.update_scale)

    def update_video(self, event=None):
        cur_pos = self.progress_slider.get()
        
        try:
            self.media_player.set_position(cur_pos)
        except Exception as e:
            print(e)

        print(cur_pos)
        print(self.media_player.get_position())
        td = timedelta(milliseconds=int(self.media_player.get_time()*1000))
        self.start_time["text"] = f"{td.seconds//3600}:{td.seconds}:{td.microseconds//1000}"

    def slider_seek_begin(self, event):
        """Function realised when first click on slider"""
        
        self.state_paused = self.media_paused # Remebering the state
        if self.media_paused == False:
            self.media_paused = True
            self.media_player.set_pause(self.media_paused)
        self.progress_slider.configure(command=self.update_video)


    def slider_seek_end(self, event):
        """Function realised when click realised from slider"""
        self.update_video()
        self.progress_slider.configure(command=None)
        self.media_paused = self.state_paused
        self.media_player.set_pause(self.media_paused)



    def skip(self, value: int):
        """ skip seconds """
        self.media_player.next_frame()
        self.update_scale()
        print(self.media_player.get_position())



    def play_pause(self, event=None):
        """ pauses and plays """
        if self.media_paused:
            self.media_paused = False
            self.media_player.set_pause(self.media_paused)
            self.play_pause_btn.config(text="Pause")
        else:
            self.media_paused = True
            self.media_player.set_pause(self.media_paused)
            self.play_pause_btn.config(text="Resume")


    def video_ended(self, event):
        """ handle video ended """
        self.progress_slider.set(1)
        self.play_pause()


    def create_widgets(self):
        self.progress_slider = ctk.CTkSlider(self, from_=.0, to=1.0, button_color="#51A1FF")
        self.progress_slider.set(0)
        self.progress_slider.bind("<Button-1>", self.slider_seek_begin)
        self.progress_slider.bind("<ButtonRelease-1>", self.slider_seek_end)
        self.progress_slider.pack(fill=tk.X, padx=10, pady=(15, 5))
        self.events = self.media_player.event_manager()
        self.frames = 0
        self.events.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.update_scale)
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.video_ended)

        

        self.exercise_frame = ttk.Frame(self)
        self.to_from_frame = ttk.Frame(self)
        self.play_frame = ttk.Frame(self)
        self.time_save_frame = ttk.Frame(self)


        self.play_pause_btn = ttk.Button(self.play_frame, text="Play", command=self.play_pause)
        self.skip_minus_5sec = ttk.Button(self.play_frame, text="Skip -5 sec", command=lambda: self.skip(-5))
        self.skip_plus_5sec = ttk.Button(self.play_frame, text="Skip +5 sec", command=lambda: self.skip(+5))
        

        exercise_label = ttk.Label(self.exercise_frame, text="Выбор упражнения:")

        self.select_exercise = tk.StringVar()
        self.cb_exercise = ttk.Combobox(self.exercise_frame, textvariable=self.select_exercise)
        self.cb_exercise['state'] = 'readonly'

        self.start_time = ttk.Label(self.time_save_frame, text="00:00:00")

        td = timedelta(milliseconds=int(self.media_info["duration"]*1000))
        self.end_time = ttk.Label(self.time_save_frame, text=f"{td.seconds//3600}:{td.seconds}:{td.microseconds//1000}")


        self.exercise_frame.pack(side="left", expand=True)
        self.to_from_frame.pack(side="left", expand=True)
        self.play_frame.pack(side="left", expand=True)
        self.time_save_frame.pack(side="left", expand=True)

        self.skip_minus_5sec.pack(side="left")
        self.play_pause_btn.pack(side="left")
        self.skip_plus_5sec.pack(side="left")

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