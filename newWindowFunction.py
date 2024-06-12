import customtkinter
import customtkinter as tk
import tkinter


def new_window(page_title, label):
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.title(page_title)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))

    # Create and place the title label
    label = customtkinter.CTkLabel(master=root, text=label, font=("Roboto", 45))
    label.place(relx=0.0, rely=0.0, anchor=tk.NW)
    root.mainloop()

    return root

#new_window("hello","hello")


