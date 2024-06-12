import pickle
import tkinter as tk
import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk


def preprocess_url(url):  # to help with accuracy scores it removes urls beginging wiht https and https
    if url.startswith("http://"):
        url = url[len("http://"):]
    elif url.startswith("https://"):
        url = url[len("https://"):]
    return url


def machine_learning(url, model_path='phishing.pkl'):
    # set cooridnates for root page
    x = 800
    y = 500

    if url is not None:  # added this clause to check that the URL in the combo select is not empty
        currentURL = ''.join(
            url)  # takes code from json dictinary to a normal string and then is passed through as a parameter
        print(currentURL)
    else:
        currentURL = ""  # if it is empty then we as=dd this clause so that if statement picks it up and creates an error

    if not currentURL or currentURL == "Select a URL" or currentURL is None:  # loading error popup if no URL has been selected
        error_window = tk.Tk()
        error_window.title("Error")
        error_window.geometry("350x90")
        error_label = tk.Label(error_window, text="Please select a URL first!", font=("Helvetica", 20))
        error_label.pack()
        error_window.geometry(f"+{x}+{y}")
        return

    currentURL = preprocess_url(
        currentURL)  # remove http/https from URL if it contains it and store this in current URL

    # following code is used for a loading screen once the popup is opened
    loading_window = tk.Tk()
    loading_window.geometry("250x100")
    loading_window.overrideredirect(True)
    loading_window.geometry(f"+{x}+{y}")
    loading_label = tk.Label(loading_window, text="Loading...", font=("Helvetica", 30))
    loading_label.pack(pady=0)
    loading_window.title("Loading...")
    loading_window.update()

    load_model = pickle.load(open(model_path, 'rb'))  # load pickle file
    result = load_model.predict([currentURL])  # use predict function against the current URL
    score = load_model.predict_proba([currentURL])  # store the probabibility statistics
    prediction_score = load_model.predict_proba([currentURL])
    prediction_score_percentage = [f"{round(score * 100, 2)}%" for score in
                                   prediction_score[0]]  # turn this into a percentage to be user friendly

    # concatenate some strings together to be displayed on screen in the labels
    r = f"Machine learning Predicts this URL to be - {result[0]} "
    p = f"Prediction Score: The Model predicts there is a- \n {prediction_score_percentage[0]} chance it is phishing \n {prediction_score_percentage[1]} chance it is not phishing"
    print(r, p)

    ##########################################################################################################################
    # create root page
    root = customtkinter.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    rootx = (screen_width - 700) // 2
    rooty = (screen_height - 400) // 2
    root.title("Machine Learning")
    root.geometry("1400x700")
    root.maxsize(700, 400)
    root.geometry(f"+{rootx}+{rooty}")

    label = customtkinter.CTkLabel(master=root, text="Machine Learning", font=("Helvetica", 70, "bold"))
    label.place(relx=0.5, rely=0.05, anchor=ctk.N)

    label1 = customtkinter.CTkLabel(master=root, text=str(r), font=("Helvetica", 25, "bold"))
    label1.place(relx=0.5, rely=0.35, anchor=ctk.N)

    label2 = customtkinter.CTkLabel(master=root, text=str(p), font=("Helvetica", 25, "bold"))
    label2.place(relx=0.5, rely=0.5, anchor=ctk.N)

    loading_window.destroy()
    root.mainloop()

    return result, score[0]


#############################################################################################################################################################
"""
predict = 'https://quiz-electrolux.com'  # Example URL
result, prediction_score = machine_learning(predict)
print(result)
print("Prediction Score:", prediction_score)
"""