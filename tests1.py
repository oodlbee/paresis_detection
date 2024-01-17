import tkinter as tk

window = tk.Tk()

frame_a = tk.Frame(window, bg="red")
frame_a.pack(fill=tk.BOTH, expand=True)

frame_b = tk.Frame(window, bg="green")
frame_b.pack(fill=tk.BOTH, expand=True)
window.geometry(f"{500}x{600}")
window.minsize(200, 200)
window.mainloop()