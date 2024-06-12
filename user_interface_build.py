from newWindowFunction import new_window
from version4emailFetch import display_email_details
import customtkinter
import customtkinter as tk
from PIL import Image, ImageTk
from about import about
from about import helpInfo

#following code is simply making a customTkinter page and adding labels and a button to it
def welcomepage():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root = customtkinter.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - 1400) // 2
    y = (screen_height-700) // 2
    root.geometry(f"+{x}+{y}")

    def open_first_email():
        root.after(2000, root.destroy)
        display_email_details([0])

    image = customtkinter.CTkImage(Image.open("hello1.png"), size=(600, 600))

    root.title("Go-Phish")
    root.geometry("1400x700")
    root.maxsize(1400, 700)

    button_font = ("Helvetica", 36, "bold")

    # Create and place the title label
    label = customtkinter.CTkLabel(master=root, text="Go-Phish",font= ("Helvetica", 126, "bold"))
    label.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    button = customtkinter.CTkButton(root, text="Start"
                                     , height=60, width=120, command=open_first_email,
                                     font=button_font)
    button.place(relx=0.7, rely=0.6, anchor=tk.CENTER)

    about_button = customtkinter.CTkButton(root, text="About", height=40, width=100, font=("Helvetica", 24, "bold"),
                                           command=lambda: about())
    about_button.place(relx=0.66, rely=0.72, anchor=tk.CENTER)

    help_button = customtkinter.CTkButton(root, text="Help", height=40, width=100, font=("Helvetica", 24, "bold"),
                                          command=lambda: helpInfo())

    help_button.place(relx=0.74, rely=0.72, anchor=tk.CENTER)

    image = customtkinter.CTkLabel(master=root, text="", image=image)
    width_pixels = root.winfo_width()
    gap_relx = 50 / width_pixels
    image.place(relx=gap_relx, rely=0.5, anchor=tk.CENTER)

    root.mainloop()

welcomepage()

