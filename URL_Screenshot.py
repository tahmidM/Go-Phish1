from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import customtkinter
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox

screenshot = None


def take_screenshot(current):
    global screenshot
    if current is not None: # added this clause to check that the URL in the combo select is not empty
        current1 = ''.join(current) #takes code from json dictinary to a normal string and then is passed through as a parameter
        print(current1)
    else:
        current1 = "" # if it is empty then we as=dd this clause so that if statement picks it up and creates an error

    url_screenshot = 'screenshot.png' #screenshot name
    width = 1400

    x = 800
    y = 500
#error window is no URL is selected
    if not current1 or current1 == "Select a URL" or current1 is None:
        error_window = tk.Tk()
        error_window.title("Error")
        error_window.geometry("350x90")
        error_label = tk.Label(error_window, text="Please select a URL first!", font=("Helvetica", 20))
        error_label.pack()
        error_window.geometry(f"+{x}+{y}")
        return
#loading popup
    loading_window = tk.Tk()
    loading_window.geometry("250x100")
    loading_window.overrideredirect(True)

    loading_window.geometry(f"+{x}+{y}")
    loading_label = tk.Label(loading_window, text="Loading...", font=("Helvetica", 30))
    loading_label.pack(pady=0)
    loading_window.title("Loading...")

    loading_window.update()
    #browser type is chrome and uses a headless broswer so no window appears
    chrome_options = Options()
    chrome_options.add_argument(f'--window-size={1400},{700}')  # Set window size
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # Initialize the Chrome browser
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to the specified URL
        driver.get(current1)

        # Waits for the page to load completely
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Set the window size to capture the entire page
        driver.set_window_size(width, driver.execute_script('return document.body.scrollHeight'))

        # Take a full page screenshot
        driver.save_screenshot(url_screenshot)
        print(f'Screenshot saved to: {url_screenshot}')

        # Load and resize the image
        screenshot1 = Image.open("screenshot.png")
        screenshot1 = screenshot1.resize((1400, 5000))
        ss = ImageTk.PhotoImage(screenshot1)

        # Update the global variable with the new PhotoImage object
        screenshot = ss

        make_display(loading_window)

    finally:
        # Close the browser
        driver.quit()
        loading_window.destroy()


def make_display(loading_window):
    if screenshot:
        # Creates top level window to contain the screenshot
        popUp = tk.Toplevel()
        popUp.title("Screenshot")
        popUp.geometry("1400x700")

        screen_width = popUp.winfo_screenwidth()
        screen_height = popUp.winfo_screenheight()
        #code below places the page
        rootx = (screen_width - 1200) // 2
        rooty = (screen_height - 600) // 2
        popUp.geometry(f"+{rootx}+{rooty}")

        canvas = tk.Canvas(popUp)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adds a vertical scrollbar
        scrollbar = tk.Scrollbar(popUp, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Creates a frame inside the canvas to hold the image
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        # Display the image in a label
        ss_label = tk.Label(frame, image=screenshot)
        ss_label.pack()

        # Configure canvas scrolling region
        frame.update_idletasks()  # Update frame to get correct size
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

        def close_screenshot():
            popUp.destroy()
            # After closing the screenshot window the loading window is destroyed
            loading_window.destroy()
        popUp.protocol("WM_DELETE_WINDOW", close_screenshot)
        popUp.mainloop()
    else:
        print("No screenshot available.")

#current = ["http://www.google.com"]
#take_screenshot(current)