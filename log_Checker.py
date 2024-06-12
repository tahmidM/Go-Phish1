import csv
import customtkinter as ctk
import tkinter as tk
import pandas as pd
from pandasgui import show

def search_logs(url, sender):#takes sender and URL as parameter,
    #x,y values to places stuff on screen
    x = 800
    y = 500
    #error popup if no URL is selected
    if not url or url == "Select a URL" or url is None:
        error_window = tk.Tk()
        error_window.title("Error")
        error_window.geometry("350x90")
        error_label = tk.Label(error_window, text="Please select a URL first!", font=("Helvetica", 20))
        error_label.pack()
        error_window.geometry(f"+{x}+{y}")
        return
    #loading window
    loading_window = tk.Tk()
    loading_window.geometry("250x100")
    loading_window.overrideredirect(True)
    loading_window.geometry(f"+{x}+{y}")
    loading_label = tk.Label(loading_window, text="Loading...", font=("Helvetica", 30))
    loading_label.pack(pady=0)
    loading_window.title("Loading...")
    loading_window.update()
    #empty arrays declared to store values from teh CSV
    urls_data = []
    senders_data = []

    if url is not None:
        stringURL = ''.join(url) #Convert the 'url' list to a single string
    else:
        stringURL = "" #to an empty string

    with open('web_proxy_logs2.csv', 'r', encoding='latin-1') as f: #reads from file
        reader = csv.reader(f, delimiter=',')
        for row in reader: #iterates through row
            if any(stringURL in column for column in row): # Check if 'stringURL' is present in any column of the current row
                urls_data.append(row)#if it does append to the array
##same process is carried out for this CSV
    with open('mail_server_logs1.CSV', 'r', encoding='latin-1') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if sender in row[3]:
                senders_data.append(row)

# Convert data to Pandas DataFrame and sets the column names this is for the web proxy logs
    Web_Proxy_Logs = pd.DataFrame(urls_data, columns=["Date", "Time", "User", "Email", "URL", "Connection", "Status"])
#code for the mail server dataframes
    columns_to_display = [0,1, 2, 3] #sets the coumns to dispay for the malil server dataframe
    Mail_Server_Logs = pd.DataFrame(senders_data) #passes the relevent array
    if not Mail_Server_Logs.empty:
        Mail_Server_Logs = Mail_Server_Logs.iloc[:, columns_to_display]
        Mail_Server_Logs.columns = ["Subject", "Sender", "Protocol", "Recipient"]
        show(Web_Proxy_Logs, Mail_Server_Logs)
        loading_window.destroy()

    else:#if the dataframe is empty then creates a popup to let the user know
        print("Mail_Server_Logs DataFrame is empty")
        emptymessage_window = tk.Tk()
        emptymessage_window.geometry("350x100")
        emptymessage_window.geometry(f"+{x}+{y}")
        label = tk.Label(emptymessage_window, text="No Logs Found", font=("Helvetica", 30))
        label.pack(pady=0)
        emptymessage_window.title("No Logs Found ")
        emptymessage_window.update()
        loading_window.destroy()

    # Display DataFrames using pandasgui
    return urls_data, senders_data

#url1 = "www.africoon.com/panel/"
#sender1 = "jobs-noreply@linkedin.com"


