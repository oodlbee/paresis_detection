
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from multiprocessing import Queue, Process, Event
from threading import Thread
import gc
import logging
from application.app_handlers import find_windows_center
from computation.start_calculations import main_start
from customtkinter import  CTkProgressBar

logger = logging.getLogger('app_logger')

class ComputeWindow(tk.Toplevel):
    def __init__(self, parent, video_file_path, markup_file_path, save_to_path):
        super().__init__(parent)
        logger.debug("Opened compute window")
        self.parent = parent
        self.title('Идет расчет...')
        self.protocol('WM_DELETE_WINDOW', self._on_exit)
        self.bind('<Destroy>', self._on_destroy)
        self.window_width = 340
        self.window_height = 100
        center_x, center_y = find_windows_center(self, self.window_width , self.window_height)
        self.geometry(f'{self.window_width }x{self.window_height}+{center_x}+{center_y}')

        self.columnconfigure(0, weight=1)
        
        self.progress_persantage = tk.Label(self, text='0 %')
        self.progress_persantage.grid(column=0, row=0, sticky=tk.EW, padx=0, pady=(10, 4))

        self.progress_bar = CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=(0, 5))

        self.cancel_button = ttk.Button(self,
                text='Отмена',
                command=self._on_exit)
        self.cancel_button.grid(column=0, row=2, sticky=tk.E, padx=8, pady=10)
        self.update()

        self.is_process_ended = False
        self.event_update = Event()
        self.progress_queue = Queue()

        self.update_thread = Thread(target=self.update_progress_thread, args=(self.event_update, self.progress_queue))
        self.update_thread.start()

        self.compute_process = Process(
            target=main_start,
            args=[self.event_update, self.progress_queue, video_file_path, markup_file_path, save_to_path]
            )
        self.compute_process.start()
        self._check_alive()
        logger.debug("Computation started...")

    def _check_alive(self):
        if not self.compute_process.is_alive():
            self.event_update.set()
            self.is_process_ended = True
        self.after(200, self._check_alive)


    def update_progress_thread(self, update_event, progress_queue):
        while True:
            update_event.wait()
            if self.is_process_ended:
                logger.debug("Computation ended successfully")
                self.progress_persantage['text'] = f'100 %'
                self.progress_bar.set(1)
                self.compute_process.kill()
                gc.collect()
                self.title('Расчет завершен')
                self.cancel_button.configure(text='Ок')
                return

            update_event.clear()
            if not progress_queue.empty():
                
                progress_value = progress_queue.get()
    
                self.progress_persantage['text'] = f'{int(progress_value * 100)} %'
                self.progress_bar.set(progress_value)
                self.update_idletasks()
        

    def _on_destroy(self, event=None):
        logger.debug("Compute window closed by force")
        self.compute_process.kill()
        gc.collect()
    

    def _on_exit(self, event=None):
        logger.debug(f"Trying to exit! Compute_process is alive = {self.compute_process.is_alive()}, \
                      update thread is alive = {self.update_thread.is_alive()}")
        
        if not self.compute_process.is_alive() and not self.update_thread.is_alive():
            logger.debug("Compute window closed by user")
            self.destroy()
            return

        result = askyesno("Выход", "Вы хотите прервать процесс?")
        if result:
            logger.debug("Compute window closed by force by user")
            self.parent.count_processes -= 1
            self.compute_process.kill()
            gc.collect()
            self.destroy()
            return