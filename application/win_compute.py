
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from threading import Thread, Event


from computation.start_calculations import main_start
from customtkinter import  CTkProgressBar


class ComputeWindow(tk.Tk):
    def __init__(self, predictor_file_path, video_file_path, markup_file_path , save_to_path):
        super().__init__()
        self.predictor_file_path = predictor_file_path
        self.video_file_path = video_file_path
        self.markup_file_path = markup_file_path
        self.save_to_path = save_to_path

        self.geometry('300x100')
        self.title('Рассчет коэфициентов асимметрии')
        self.protocol("WM_DELETE_WINDOW", self._on_exit)

        self.columnconfigure(0, weight=1)
        
        self.progress_persantage = tk.Label(self, text='0 %')
        self.progress_persantage.grid(column=0, row=0, sticky=tk.EW, padx=0, pady=(0, 4))

        self.progress_bar = CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=(0, 5))

        ttk.Button(self,
                text='Отмена',
                command=self._on_exit).grid(column=0, row=2, sticky=tk.E, padx=5, pady=10)
        self.update()

        self._execute_thread = Event()
        self.compute_thread = Thread(target=self.launch_main, args=(self._execute_thread, ))
        self.compute_thread.start()
    
    def _on_exit(self):
        result = askyesno("Exit", "Вы хотите прервать процесс?")
        if result:
            self._execute_thread.set()
            self.compute_thread.join()
            self.destroy()


    def update_progress(self, value:int, lenght:int):
        cur_val = value / lenght
        if value >= lenght:
            cur_val = 0.99
        self.progress_persantage['text'] = f'{int(cur_val * 100)} %'
        self.progress_bar.set(cur_val)
        self.update_idletasks()


    def launch_main(self, execute_event):
        main_start(
         self.predictor_file_path,
         self.video_file_path, 
         self.markup_file_path,
         self.save_to_path,
         self.update_progress,
         execute_event
        )
        self.progress_persantage['text'] = f'100 %'
        self.progress_var.set(100)

        
