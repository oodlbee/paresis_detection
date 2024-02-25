import tkinter as tk
from re import search, fullmatch
from tkinter.messagebox import showerror

from application.app_handlers import find_windows_center

class LoadingWindow(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(parent)
        self.title('Загрузка')
        window_width = 300
        window_height = 100
        center_x, center_y = find_windows_center(self, window_width, window_height)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        label = tk.Label(self, text="Загрузка...", font=("Helvetica", 16))
        label.pack(pady=20)
        


class EditableListbox(tk.Listbox):
    """A listbox where you can directly edit an item via double-click"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.edit_item = None
        self.bind("<Double-1>", self._start_edit)

    def _start_edit(self, event):
        index = self.index(f"@{event.x},{event.y}")
        self.start_edit(index)
        return "break"

    def _spell_check(self, word:str):
        if bool(search(r'\s', word)):
            showerror(title='Ошибка', message=f'В названии присутствуют пробельные символы')
            return False
        elif bool(search(r'[а-яА-Я]', word)):
            showerror(title='Ошибка', message=f'В названии присутствуют не латинские буквы')
            return False
        elif not bool(fullmatch(r'[a-zA-z0-9_]+', word)):
            showerror(title='Ошибка', message=f"Название должно содержать только латинские буквы, цифры и символы '_'")
            return False
        return True
    

    def _duplication_check(self, word=None):
        exercises = list(self.get(0, tk.END))
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

    def start_edit(self, index):
        self.edit_item = index
        text = self.get(index)
        y0 = self.bbox(index)[1]
        entry = tk.Entry(self, borderwidth=0, highlightthickness=1)
        entry.bind("<Return>", self.accept_edit)
        entry.bind("<Escape>", self.cancel_edit)

        entry.insert(0, text)
        entry.selection_from(0)
        entry.selection_to("end")
        entry.place(relx=0, y=y0, relwidth=1, width=-1)
        entry.focus_set()
        entry.grab_set()

    def cancel_edit(self, event):
        event.widget.destroy()

    def accept_edit(self, event):
        new_data = event.widget.get()
        if self.get(self.edit_item) == new_data:
            event.widget.destroy()
            return
        if not self._spell_check(new_data):
            return
        if not self._duplication_check(new_data):
            return
        self.delete(self.edit_item)
        self.insert(self.edit_item, new_data)
        event.widget.destroy()



# class MarkFrame(ctk.CTkFrame):
#     def __init__(self, master=None, icon_path:str=None, **kwargs):
#         super().__init__(master, **kwargs,)
#         self.mask_image = Image.open(str(Path(icon_path).absolute()))
#         self.mask_image = np.array(self.mask_image)

#         self.gen_color = self._gen_color()
#         self.states = {}
#         # Construction of self.states:
#         #   {
#         #       'state1': {
#         #                   'begin': tk.label, 
#         #                   'end': tk.label, 
#         #                   'color': (r,g,b)
#         #       },
#         #       'state2' {...}
#         #   }

#     def _gen_color(self):
#         index = 0
#         pallete = Tableau_20.mpl_colors
#         while True:
#             yield list(pallete[index]) + [1]
#             index = (index + 1) % len(pallete)

#     def set_flag(self, state:str, begin:bool=True):
#         location = 'begin' if begin else 'end'
#         if not state in self.states.keys():
#             self.states[state] = {'begin': None, 'end': None, 'color': next(self.gen_color)}


#             print(self.states[state])
#             # painting mask
#             image = np.zeros((30, 30, 4), dtype=np.uint8)
#             for i in range(4):
#                 image[:, :, i] = self.mask_image * int(self.states[state]['color'][i] * 255)
#             # create button with image
#             image = ctk.CTkImage(Image.fromarray(image, 'RGBA'))
#             self.states[state][location] = ctk.CTkLabel(self, text='', image=image, fg_color="transparent")
#             self.states[state][location].place(x=10, y=0)
#             self.states[state][location].lower()
            
        
        

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.geometry("300x300")
#     # root.configure(background='black')
    
#     frame = MarkFrame(root, icon_path='images/flag_mask.png', fg_color='transparent', height=100)
#     slider = ctk.CTkSlider(frame, from_=0, to=100)


#     frame.pack(fill=tk.BOTH, pady=10, padx=10)
#     slider.grid(column=0, row=0)

#     frame.set_flag('kek')
#     root.mainloop()