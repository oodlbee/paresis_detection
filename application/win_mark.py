import logging

import tkinter as tk
import customtkinter as ctk

from pathlib import Path
from json import load as json_load

from tkinter import ttk, Menu
from tkinter.messagebox import showerror

from PIL import Image
from pandas import DataFrame

from application.app_handlers import TkinterVideo
from application.app_handlers import select_save_path, video_redecoding, get_max_video_size, find_windows_center, get_init_video_info
from application.win_exercise import ExerciseWindow


class MarkWindow(tk.Toplevel):
    def __init__(self, parent, config, init_save_folder, video_path):
        super().__init__(parent)
        self.logger = logging.getLogger('app_logger')
        self.logger.debug("Opened mark window")
        self.parent = parent
        self.video_path = video_path
        self.init_save_folder = init_save_folder
        self.video_name = Path(self.video_path).stem
        self.config_file = config
        self.data_folder = Path(self.config_file['internal.files']['application_data'][1:-1]).absolute()
        self.icons_folder = Path(self.config_file['internal.files']['application_icons'][1:-1]).absolute()
        video_box = get_max_video_size(self)

        # decoding video for display
        temp_video_path = self.data_folder/'_temp_ffmpeg.mp4'
        video_redecoding(self.video_path, temp_video_path, video_box)

        self.focus_set()
        self.config(cursor="")
        self.title(f'Разметка видео {self.video_name}')   

        self.videoplayer = TkinterVideo(master=self, keep_aspect=True)
        self.videoplayer.load(str(temp_video_path))
        self.video_info = self.videoplayer.video_info()
        print(self.video_info)
        self.bind("<<Ended>>", self._video_ended)

        # debug moment
        init_fm = get_init_video_info(self.video_path)
        self.logger.info(f'Init video frame nums - {init_fm}')
        if init_fm != self.video_info['frames_num']:
            self.logger.error(f'Critical missmatch of frame nums: {init_fm} != {self.video_info["frames_num"]}')
            raise Exception('Critical missmatch of frame nums')
        
        self.tools_hight = 110
        width = self.video_info['framesize'][0]
        hight = self.video_info['framesize'][1] + self.tools_hight
        center_x, center_y = find_windows_center(self, width, hight)
        self.geometry(f'{width}x{hight}+{center_x}+{center_y}')
        self.minsize(width, hight)
        
        # Some flags
        self.glob_pause = True

        self.markup_dict = {}
        # Construction of self.markup_dict:
        #   {
        #       'exercise name 1': {
        #                   'begin': frame number,
        #                   'end': frame number
        #       },
        #       'exercise name 1' {...}
        #   }
        self.create_menu()
        self.create_widgets()
        self.create_buttons_bindings()
        

    def _on_destoy(self):
        self.logger.debug("Delete temp video file")
        self.temp_video_file.delete()


    def create_menu(self):
        self.menubar = Menu(self)
        self.config(menu=self.menubar)

        self.markup_menu = Menu(self.menubar)

        self.markup_menu.add_command(
            label='Редактор разметки',
            command=lambda: ExerciseWindow(self, self.config_file),
        )

        self.markup_menu.add_command(
            label='Очистить текущую разметку',
            command=self.clear_markup,
        )

        self.markup_menu.add_command(
            label='Очистить всю разметку',
            command=self.clear_all_markup,
        )

        self.menubar.add_cascade(
            label="Разметка",
            menu=self.markup_menu,
        )
        self.logger.debug("Menu is created")


    def _fromat_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        milliseconds = seconds % 1 * 100
        return "{:02}:{:02}:{:02}".format(int(minutes), int(seconds), int(milliseconds))

    def _update_time_label(self, frame_num):
        self.start_time["text"] = self._fromat_seconds(frame_num/self.video_info['framerate'])
        self.num_frame["text"] = frame_num

    def on_close_exercise_window(self):
        with open(str(self.data_folder/'exercises_current.json'), 'r') as file:
            exercises = json_load(file)
        
        if exercises == self.cb_exercise_list:
            return
        new_exercises = list(set(exercises) - set(self.cb_exercise['values']))
        drop_exercises = list(set(self.cb_exercise['values']) - set(exercises))
        
        for exercise in drop_exercises:
            self.markup_dict.pop(exercise)
        for exercise in new_exercises:
            self.markup_dict[exercise] = {'begin': None, 'end': None}

        self.cb_exercise_list = exercises
        self.cb_exercise['value'] = self.cb_exercise_list
        self.cb_exercise.current(0)
        self.change_exercise_buttons()
        

    def compile_markup_excel(self):
        video_name = Path(self.video_path).stem
        df_markup = {'file_name': video_name}
        for exercise in self.markup_dict.keys():
            if self.markup_dict[exercise]['begin'] == None:
                self.logger.warning(f"There is no markup of begining of exersize {exercise}")
                showerror(title='Ошибка', message=f'Нет разметки начала упражнения {exercise}')
                return
            if self.markup_dict[exercise]['end'] == None:
                self.logger.warning(f"There is no markup of ending of exersize {exercise}")
                showerror(title='Ошибка', message=f'Нет разметки конца упражнения {exercise}')
                return
            df_markup[exercise + '_begin'] = [self.markup_dict[exercise]['begin']]
            df_markup[exercise + '_end'] = [self.markup_dict[exercise]['end']]
        df_markup = DataFrame(df_markup)    
        result_path = select_save_path(self.parent.entry_mark, init_dir=self.init_save_folder,
                                       init_file_name=self.video_name + '_markup.xlsx', defaultextension='.xlsx')
        if result_path == None:
            self.logger.warning(f"Markup is not saved. Empty selected path")
            return
        df_markup.to_excel(result_path, index=False)
        self.logger.info(f"Markup is saved on path {result_path}")


    def change_exercise_buttons(self, event=None):
        exercise = self.cb_exercise.get()
        begin_frame = self.markup_dict[exercise]['begin']
        begin_frame = '--' if begin_frame == None else begin_frame
        end_frame = self.markup_dict[exercise]['end']
        end_frame = '--' if end_frame == None else end_frame
        self.exercise_begin.configure(text=f'Начало: {begin_frame}')
        self.exercise_end.configure(text=f'Конец: {end_frame}')


    def update_markup(self, is_begin: bool = False):
        exercise = self.cb_exercise.get()
        frame_num = self.videoplayer.current_frame_number()
        if exercise == "":
            return
        
        if is_begin:
            self.markup_dict[exercise]['begin'] = frame_num
        else:
            self.markup_dict[exercise]['end'] = frame_num
        self.change_exercise_buttons()
        
    def clear_markup(self):
        exercise = self.cb_exercise.get()
        if exercise == "":
            return
        
        self.markup_dict[exercise]['begin'] = None
        self.markup_dict[exercise]['end'] = None
        self.exercise_begin.configure(text='Начало: --')
        self.exercise_end.configure(text='Конец: --')

    def clear_all_markup(self):
        for exercise in self.cb_exercise_list:
            self.markup_dict[exercise]['begin'] = None
            self.markup_dict[exercise]['end'] = None
            self.exercise_begin.configure(text='Начало: --')
            self.exercise_end.configure(text='Конец: --')    


    def update_scale(self, event=None):
        cur_frame = self.videoplayer.current_frame_number()
        self.progress_slider.set(cur_frame)
        self._update_time_label(cur_frame)


    def update_video(self, event=None):
        cur_frame = int(self.progress_slider.get())
        self.videoplayer.seek(cur_frame)
        self._update_time_label(cur_frame)


    def slider_seek_begin(self, event):
        """Function realised when first click on slider"""
        self.unbind('<<FrameGenerated>>')
        self.progress_slider.configure(command=self.update_video)
        if self.videoplayer.pause() == False:
            self.videoplayer.pause()


    def slider_seek_end(self, event):
        """Function realised when click realised from slider"""
        self.update_video()
        self.progress_slider.configure(command=None)
        self.bind('<<FrameGenerated>>', self.update_scale)
        if self.glob_pause == False:
            self.videoplayer.play()


    def skip(self, backward: bool=False):
        """ Skip seconds """
        cur_frame = self.videoplayer.current_frame_number()
        if cur_frame <= 0 or cur_frame > self.video_info['frames_num']:
            self.logger.error(f"Current frame - {cur_frame} <= 0 or > video frame num - {self.video_info['frames_num']}")
            return
        if backward:
            self.videoplayer.seek(cur_frame - 1)
            self.logger.debug(f"Skipped backward to frame number {cur_frame - 1}")
        else:
            if cur_frame == self.video_info['frames_num']:
                self.logger.warning(f"Trying to seek forward when video has been ended")
                return
            self.videoplayer.seek(cur_frame + 1)
            self.logger.debug(f"Skipped forward to frame number {cur_frame + 1}")
        self.update_scale()


    def play_pause(self, event=None):
        """ Pauses and plays """
        cur_frame = self.videoplayer.current_frame_number()
        if self.videoplayer.is_paused():
            # If continue button pressed when video ended - go to begining
            if cur_frame == self.video_info['frames_num']:
                self.videoplayer.restart_video()
                self.progress_slider.set(1)
            self.glob_pause = False
            self.bind('<<FrameGenerated>>', self.update_scale)
            self.videoplayer.play()
            self.play_pause_btn.configure(image=self.pause_image)
            self.logger.debug("Video unpaused")
        else:
            self.glob_pause = True
            self.unbind('<<FrameGenerated>>')
            self.videoplayer.pause()
            self.play_pause_btn.configure(image=self.play_image)
            self.logger.debug("Video paused")


    def _video_ended(self, event=None):
        """ Handle video ended """
        # self.progress_slider.set(1)
        self.play_pause()
        self.logger.debug("Video ended")


    def create_widgets(self):
        self.play_image = ctk.CTkImage(Image.open(str(self.icons_folder/'play.png')), size=(30, 30))
        self.pause_image = ctk.CTkImage(Image.open(str(self.icons_folder/'pause.png')), size=(30, 30))
        self.skip_fw_image = ctk.CTkImage(Image.open(str(self.icons_folder/'skip_forward.png')), size=(30, 15))
        self.skip_bw_image = ctk.CTkImage(Image.open(str(self.icons_folder/'skip_backward.png')), size=(30, 15))

        self.main_frame = ttk.Frame(self)
        self.tools_frame = ttk.Frame(self.main_frame, height=self.tools_hight)
        self.play_frame = ttk.Frame(self.tools_frame)
        self.time_frame = ttk.Frame(self.tools_frame)
        self.tools_frame.columnconfigure(0, weight=1)
        self.tools_frame.columnconfigure(1, weight=1)
        self.tools_frame.columnconfigure(2, weight=2)
        self.tools_frame.columnconfigure(3, weight=2)

        self.progress_slider = ctk.CTkSlider(self.main_frame, from_=0, to=self.video_info['frames_num'], button_color="#51A1FF")
        self.progress_slider.set(0)
        self.progress_slider.bind("<Button-1>", self.slider_seek_begin)	      
        self.progress_slider.bind("<ButtonRelease-1>", self.slider_seek_end)
    

        self.play_pause_btn = ctk.CTkButton(self.play_frame, text='', image=self.play_image, command=self.play_pause, fg_color="transparent", width=40)
        self.forward_frame = ctk.CTkButton(self.play_frame, text='', image=self.skip_fw_image, command=self.skip, fg_color="transparent", width=40)
        self.backward_frame = ctk.CTkButton(self.play_frame, text='', image=self.skip_bw_image, command=lambda: self.skip(backward=True), fg_color="transparent", width=40)
        
        exercise_label = ttk.Label(self.tools_frame, text="Упражнение:")
        self.cb_exercise_list = []
        with open(str(self.data_folder/'exercises_current.json'), 'r') as file:
            self.cb_exercise_list = json_load(file)
            for exercise in self.cb_exercise_list:
                self.markup_dict[exercise] = {'begin': None, 'end': None}
        self.cb_exercise = ttk.Combobox(self.tools_frame, values=self.cb_exercise_list)
        self.cb_exercise.bind("<<ComboboxSelected>>", self.change_exercise_buttons)

        self.cb_exercise['state'] = 'readonly'
        self.cb_exercise.current(0)
        
        self.exercise_begin = ttk.Button(self.tools_frame, text=f"Начало: --", width=10, command=lambda: self.update_markup(is_begin=True), takefocus=False)
        self.exercise_end = ttk.Button(self.tools_frame, text=f"Конец: --", width=10, command=lambda: self.update_markup(False), takefocus=False)

        self.start_time = ttk.Label(self.time_frame, text="00:00:00", width=7)
        self.end_time = ttk.Label(self.time_frame, text=self._fromat_seconds(self.video_info['duration']), width=7)
        self.num_frame_label = ttk.Label(self.time_frame, text='Номер кадра:')
        self.num_frame = ttk.Label(self.time_frame, text=0, width=7)

        self.save_button = ttk.Button(self.time_frame, text="Сохранить", width=10, command=self.compile_markup_excel, takefocus=False)

        self.videoplayer.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, ipady=self.tools_hight)
        self.progress_slider.pack(fill=tk.X, padx=10, pady=5)

        self.tools_frame.pack(side=tk.TOP, fill=tk.BOTH)

        exercise_label.grid(column=0, row=0, sticky=tk.SW, padx=(20,))
        self.cb_exercise.grid(column=0, row=1, sticky=tk.EW, padx=(10,), pady=(0,10))

        self.exercise_begin.grid(column=1, row=0, sticky=tk.EW)
        self.exercise_end.grid(column=1, row=1, sticky=tk.EW)

        self.play_frame.grid(column=2, row=0, rowspan=2, sticky=tk.NS)

        self.backward_frame.pack(side=tk.LEFT)
        self.play_pause_btn.pack(side=tk.LEFT)
        self.forward_frame.pack(side=tk.LEFT)

        self.time_frame.grid(column=3, row=0, rowspan=2, sticky=tk.E)

        self.start_time.grid(column=0, row=0, sticky=tk.E)
        self.end_time.grid(column=1, row=0, sticky=tk.W, padx=(0, 20))
        self.save_button.grid(column=0, row=1, columnspan=2, sticky=tk.EW, padx=(0, 20))
        self.logger.debug("Widgets are created")
        # self.num_frame_label.grid(column=0, row=1, sticky=tk.E)
        # self.num_frame.grid(column=1, row=1, sticky=tk.W)
        # self.end_time.pack(side=tk.RIGHT, padx=(0, 10))
        # self.start_time.pack(side=tk.RIGHT)


    def create_buttons_bindings(self):
        self.bind("<Left>", lambda x: self.backward_frame.invoke())
        self.bind("<Right>", lambda x: self.forward_frame.invoke())
        self.bind("<space>", lambda x: self.play_pause_btn.invoke())
        self.bind("<KeyPress-w>", lambda x: self.exercise_begin.invoke())
        self.bind("<KeyPress-s>", lambda x: self.exercise_end.invoke())
