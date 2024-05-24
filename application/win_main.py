import logging
from cv2 import VideoCapture
from os import path
from pathlib import Path
from sys import platform

from mimetypes import guess_type
from configparser import ConfigParser
from multiprocessing import Queue, Process, cpu_count

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from application.win_mark import MarkWindow
from application.win_compute import ComputeWindow
from application.app_handlers import find_windows_center, select_file_path, select_save_path
from application.app_handlers import LoadingWindow

logger = logging.getLogger('app_logger')


class Application(tk.Tk):
    def __init__(self, app_config: ConfigParser):
        super().__init__()
        logger.debug("Opened main window")
        self.app_config_file = app_config
        self.title('Детекция асимметрии')

        window_width, window_height = 850, 300
        center_x, center_y = find_windows_center(self, window_width, window_height)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)

        ttk.Style().configure("TButton", relief="flat")

        icons_folder = Path(self.app_config_file['internal.files']['application_icons'][1:-1]).absolute()
        self.iconphoto(True, tk.PhotoImage(file=str(icons_folder/f'icon.png')))
        
        self.video_folder = tk.StringVar()
        self.mark_folder = tk.StringVar()
        self.save_folder = tk.StringVar()

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.create_widgets()

        # list of computation processes, keep 2 cores alive to avoid overloadting
        self.max_cores = cpu_count() - 2
        self.count_processes = 0

    def open_compute_window(self):
        video_file_path = self.entry_video.get()
        markup_file_path = self.entry_mark.get()
        save_to_path = self.entry_save.get()

        if '' in [video_file_path, markup_file_path, save_to_path]:
            logger.warning("Error while trying to open compute window: There are empty fields")
            showerror(title='Ошибка', message='Не все поля заполнены')
            return
        
        if self.count_processes > self.max_cores:
            logger.warning("Error while trying to open compute window: Cores limit is exceeded")
            showerror(title='Ошибка', message='Превышен лимит по количеству используемых ядер. Осталось 2 свободных ядра.')
            return
        ComputeWindow(self, video_file_path, markup_file_path, save_to_path)
        self.count_processes += 1



    def check_video_path(self):
        logger.debug("Checking video path existance")
        video_path = self.video_folder.get()

        # Check if file exists
        if not path.isfile(video_path):
            logger.warning(f"Video file doesn't exits on {video_path}")
            return "Видеофайл не найден"
        
        # Check if file is a video
        mime_type, _ = guess_type(video_path)
        if not (mime_type and mime_type.startswith('video')):
            logger.warning(f"Wrong format of videofile on {video_path}")
            return "Неверный формат видеофайла"
        
        video = VideoCapture(video_path)
        if not video.isOpened():
            logger.warning(f"Cant open CV with videofile on {video_path}")
            return "Неверный формат видеофайла"
        video.release()


    def open_mark_window(self):
        video_status = self.check_video_path()
        logger.debug("Trying to open video file")
        if video_status:
            showerror(title='Ошибка', message=video_status)
        else:
            loading_window = LoadingWindow(self)
            self.update()
            mark_window = MarkWindow(self, self.app_config_file, self.video_folder.get())
            loading_window.destroy()
            mark_window.grab_set()
            self.wait_window(mark_window)
        

    def create_widgets(self):
        def create_video_row(self, label_text:str, pad_hight:int):
            row = 0
            pady = (pad_hight, 8)

            label = ttk.Label(self, text=label_text, anchor="e", width=12)
            label.grid(row=row, column=0, pady=pady, sticky=tk.E)

            self.entry_video = ttk.Entry(self, width=50, textvariable=self.video_folder, takefocus=False)
            self.entry_video.focus()
            self.entry_video.grid(row=row, column=1, padx=5, pady=pady, sticky=tk.EW)

            button_folder = ttk.Button(self, text="Поиск", command=lambda: select_file_path(self.entry_video), takefocus=False)
            button_folder.grid(row=row, column=2, padx=5, pady=pady, sticky=tk.EW)


        def create_mark_row(self, label_text:str):
            row = 1
            pady = 8

            label = ttk.Label(self, text=label_text, anchor="e", width=12)
            label.grid(row=row, column=0, pady=pady, sticky=tk.E)

            self.entry_mark = ttk.Entry(self, width=50, textvariable=self.mark_folder, takefocus=False)
            self.entry_mark.grid(row=row, column=1, padx=(5, 5), pady=pady, sticky=tk.EW)

            button_folder = ttk.Button(self, text="Поиск", command=lambda: select_file_path(self.entry_mark), takefocus=False)
            button_folder.grid(row=row, column=2, padx=5, pady=pady, sticky=tk.EW)

            button_marking = ttk.Button(self, text="Разметка", command=self.open_mark_window, takefocus=False)
            button_marking.grid(row=row, column=3, padx=(5, 30), pady=pady, sticky=tk.EW)

        def create_save_row(self, label_text:str):
            row = 2
            pady = 8

            label = ttk.Label(self, text=label_text, anchor="e", width=12)
            label.grid(row=row, column=0, pady=pady, sticky=tk.E)

            self.entry_save = ttk.Entry(self, width=50, textvariable=self.save_folder, takefocus=False)
            self.entry_save.grid(row=row, column=1, padx=5, pady=pady, sticky=tk.EW)

            button_folder = ttk.Button(self, text="Поиск", command=lambda: select_save_path(self.entry_save, dirictory=True), takefocus=False)
            button_folder.grid(row=row, column=2, padx=5, pady=pady, sticky=tk.EW)

            button_video = ttk.Button(self, text="Запуск", command=self.open_compute_window, takefocus=False)
            button_video.grid(row=row, column=3, padx=(5, 30), pady=pady, sticky=tk.EW)

        create_video_row(self, "Видеофайл: ", pad_hight=80)
        create_mark_row(self, "Разметка: ")
        create_save_row(self, "Сохранять в: ")

        logger.debug("Widgets are created")


if __name__ == "__main__":
    app_config = ConfigParser()
    app_config.read('application/app_config.ini')
    config = ConfigParser()
    config.read('../config.ini')
    application = Application(app_config, config)
    application.mainloop()