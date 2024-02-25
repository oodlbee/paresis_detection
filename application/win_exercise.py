import json
import re
import tkinter as tk
from pathlib import Path
from tkinter import ttk, Menu
from application.app_handlers import EditableListbox
from tkinter.messagebox import showerror, askyesnocancel


class ExerciseWindow(tk.Toplevel):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.config_file = config
        self.data_folder = Path(self.config_file['internal.files']['application_data'][1:-1]).absolute()
        self.parent = parent
        self.grab_set()
        self.title("Редактор списка упражнений")
        self.protocol('WM_DELETE_WINDOW', self.on_close)


        with open(str(self.data_folder/'exercises_current.json')) as file:
            self.exercise_list = json.load(file)
        self.exercise_list_initial = self.exercise_list
        self.create_menu()
        self.create_widgets()
    
    def _spell_check(self, word:str):
        if bool(re.search(r'\s', word)):
            showerror(title='Ошибка', message=f'В названии присутствуют пробельные символы')
            return False
        elif bool(re.search(r'[а-яА-Я]', word)):
            showerror(title='Ошибка', message=f'В названии присутствуют не латинские буквы')
            return False
        elif not bool(re.fullmatch(r'[a-zA-z0-9_]+', word)):
            showerror(title='Ошибка', message=f"Название должно содержать только латинские буквы, цифры и символы '_'")
            return False
        return True
    

    def _duplication_check(self, word=None):
        exercises = list(self.listbox.get(0, tk.END))
        if word == None:
            seen = set()
            duples = [x for x in exercises if x in seen or seen.add(x)] 
            if duples != []:
                showerror(title='Ошибка', message=f"В списке присутствуют дубликаты упражнений: {', '.join(duples)}")
                return False
            return True
        if word in exercises:
            showerror(title='Ошибка', message=f"Название упражнения {word} уже имеется в списке")
            return False
        return True
        

    def create_menu(self):
        # Сreate main menu
        self.menubar = Menu(self)
        self.config(menu=self.menubar)

        # Сreate file menu
        self.file_menu = Menu(self.menubar)
        # Add file options
        self.file_menu.add_command(
            label='Сбросить упражнения',
            command=self.reset_exercise_list
        )
        self.file_menu.add_command(
            label='Выход',
            command=self.destroy
        )

        self.menubar.add_cascade(
            label="Файл",
            menu=self.file_menu
        )


    def create_widgets(self):
        # Create widget frame
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        # Create editable listbox
        self.listbox = EditableListbox(frame, width=40)
        for exercise in self.exercise_list:
            self.listbox.insert("end", exercise)
        self.listbox.pack(side=tk.LEFT, padx=10)

        # Create scrollbar for listbox
        self.scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Attaching a scrollbar to a list
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Create buttons and entry
        self.entry = ttk.Entry(self, width=30)
        self.entry.bind("<Return>", self.add_item)
        self.entry.pack(pady=5)
        add_button = ttk.Button(self, text="Добавить", command=self.add_item)
        add_button.pack(side=tk.LEFT, padx=5)
        remove_button = ttk.Button(self, text="Удалить", command=self.remove_item)
        remove_button.pack(side=tk.LEFT, padx=5)
        self.bind("<BackSpace>", self.remove_item)
        edit_button = ttk.Button(self, text="Сохранить", command=self.save_list)
        edit_button.pack(side=tk.RIGHT, padx=5)

        self.mainloop()

    def reset_exercise_list(self):
        with open(str(self.data_folder/'exercises_template.json')) as file:
            self.exercise_list = json.load(file)
        self.listbox.delete(0, tk.END)
        for exercise in self.exercise_list:
            self.listbox.insert("end", exercise)

    def add_item(self, event=None):
        item = self.entry.get()
        if not self._spell_check(item):
                return
        if not self._duplication_check(item):
            return
        if item:
            self.listbox.insert(tk.END, item)
            self.entry.delete(0, tk.END)

    def remove_item(self, event=None):
        selected = self.listbox.curselection()
        if selected:
            self.listbox.delete(selected)


    def save_list(self):
        exercises = list(self.listbox.get(0, tk.END))
        for exercise in exercises:
            if not self._spell_check(exercise):
                return False
        if not self._duplication_check():
            return False
        with open(str(self.data_folder/'exercises_current.json'), 'w') as file:
            json.dump(exercises, file)
        self.exercise_list_initial = exercises

    def on_close(self):
        if self.exercise_list_initial == list(self.listbox.get(0, tk.END)):
            self.parent.on_close_exercise_window()
            self.destroy()
            return

        response = askyesnocancel('Выход', 'Сохранить изменения в списке упражнений перед выходом?')
        if response == None:
            return
        elif response:
            if not self.save_list():
                return
        self.parent.on_close_exercise_window()
        self.destroy() 

            
# if __name__ == '__main__':

#     root = tk.Tk()
#     root.title("Внешнее окно")
#     capture_window = ExerciseWindow(root)
#     root.mainloop()