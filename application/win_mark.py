import tkinter as tk
import customtkinter as ctk

from pathlib import Path
from json import load as json_load

from tkinter import ttk, Menu
from tkinter.messagebox import showerror

from PIL import Image
from pandas import DataFrame

from application.app_handlers import TkinterVideo
from application.app_handlers import select_file_path, video_redecoding, find_windows_center
from application.win_exercise import ExerciseWindow


class MarkWindow(tk.Toplevel):
    def __init__(self, parent, config, video_path):
        super().__init__(parent)
        self.parent = parent
        self.video_path = video_path
        self.config_file = config
        self.data_folder = Path(self.config_file['internal.files']['application_data'][1:-1]).absolute()
        self.icons_folder = Path(self.config_file['internal.files']['application_icons'][1:-1]).absolute()
        temp_video_path = video_redecoding(self.video_path)
        self.config(cursor="")
        self.title('Разметка видео')   

        self.videoplayer = TkinterVideo(master=self, keep_aspect=True)
        self.videoplayer.load(temp_video_path)
        self.video_info = self.videoplayer.video_info()
        self.bind("<<Ended>>", self._video_ended)
        
        self.tools_hight = 110
        width = self.video_info['framesize'][0]
        hight = self.video_info['framesize'][1] + self.tools_hight
        center_x, center_y = find_windows_center(self, width, hight)
        self.geometry(f'{width}x{hight}+{center_x}+{center_y}')
        self.minsize(width, hight)
        
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
                showerror(title='Ошибка', message=f'Нет разметки начала упражнения {exercise}')
                return
            if self.markup_dict[exercise]['end'] == None:
                showerror(title='Ошибка', message=f'Нет разметки конца упражнения {exercise}')
                return
            df_markup[exercise + '_begin'] = [self.markup_dict[exercise]['begin']]
            df_markup[exercise + '_end'] = [self.markup_dict[exercise]['end']]
        df_markup = DataFrame(df_markup)
        result_path = select_file_path(self.parent.entry_mark, True, True)
        df_markup.to_excel(result_path, index=False)


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
        if exercise == "":
            return
        
        if is_begin:
            self.markup_dict[exercise]['begin'] = self.num_frame["text"]
        else:
            self.markup_dict[exercise]['end'] = self.num_frame["text"]
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
        self.progress_slider.configure(command=self.update_video)
        if self.videoplayer.pause() == False:
            self.videoplayer.pause()
        # self.progress_slider.configure(command=self.update_video)


    def slider_seek_end(self, event):
        """Function realised when click realised from slider"""

        self.update_video()
        self.progress_slider.configure(command=None)
        if self.glob_pause == False:
            self.videoplayer.play()


    def skip(self, backward: bool=False):
        """ Skip seconds """
        cur_frame = self.videoplayer.current_frame_number()
        if backward:
            self.videoplayer.seek(cur_frame - 1)
        else:
            self.videoplayer.seek(cur_frame + 1)
        self._update_time_label(cur_frame)



    def play_pause(self, event=None):
        """ Pauses and plays """
        if self.videoplayer.is_paused():
            self.glob_pause = False
            self.bind('<<FrameGenerated>>', self.update_scale)
            self.videoplayer.play()
            self.play_pause_btn.configure(image=self.pause_image)
        else:
            self.glob_pause = True
            self.unbind('<<FrameGenerated>>')
            self.videoplayer.pause()
            self.play_pause_btn.configure(image=self.play_image)


    def _video_ended(self, event=None):
        """ Handle video ended """
        self.progress_slider.set(1)
        self.play_pause()


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
        
        self.exercise_begin = ttk.Button(self.tools_frame, text=f"Начало: --", width=10, command=lambda: self.update_markup(is_begin=True))
        self.exercise_end = ttk.Button(self.tools_frame, text=f"Конец: --", width=10, command=lambda: self.update_markup(False))

        self.start_time = ttk.Label(self.time_frame, text="00:00:00", width=7)
        self.end_time = ttk.Label(self.time_frame, text=self._fromat_seconds(self.video_info['duration']), width=7)
        self.num_frame_label = ttk.Label(self.time_frame, text='Номер кадра:')
        self.num_frame = ttk.Label(self.time_frame, text=0, width=7)

        self.save_button = ttk.Button(self.time_frame, text="Сохранить", width=10, command=self.compile_markup_excel)

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
        # self.num_frame_label.grid(column=0, row=1, sticky=tk.E)
        # self.num_frame.grid(column=1, row=1, sticky=tk.W)
        # self.end_time.pack(side=tk.RIGHT, padx=(0, 10))
        # self.start_time.pack(side=tk.RIGHT)


    def create_buttons_bindings(self):
        self.bind("<Left>", lambda x: self.backward_frame.invoke())
        self.bind("<Right>", lambda x: self.forward_frame.invoke())
        self.bind("<space>", lambda x: self.play_pause_btn.invoke())
