import tkinter as tk


def click() -> None:
    print("clicked")


def bad_click() -> None:
    print("bad click")


root = tk.Tk()
root.title("Hugo's GUI")
root.geometry("2560x1080")

user_name = tk.Label(root, text="Username").pack(side="bottom", fill="x")

agb = tk.Button(root, text="Click", command=click).place(x=40, y=80)
abb = tk.Button(root, text="Bad Click", command=bad_click).place(x=80, y=80)


root.mainloop()
