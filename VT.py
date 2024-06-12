import tkinter
import requests
import json
import time
from newWindowFunction import new_window
import customtkinter
import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


##########################################################################################################################
def check_urls_virustotal(urls_json):
    x = 800
    y = 500

    #error window if no URL selected
    if not urls_json or "Select a URL" in urls_json:
        error_window = tk.Tk()
        error_window.title("Error")
        error_window.geometry("350x90")
        error_label = tk.Label(error_window, text="Please select a URL first!", font=("Helvetica", 20))
        error_label.pack()
        error_window.geometry(f"+{x}+{y}")
        return
    #api keys and API endpoints
    apiKey = "19158fdcdb7b9101963ee83037a7c62201aabb0202d442ceb7fffbd5c0762389"
    url_report = 'https://www.virustotal.com/vtapi/v2/url/report'
    url_scan = 'https://www.virustotal.com/vtapi/v2/url/scan'
##########################################################################################################################
    root = customtkinter.CTk()
    #code for loading screen
    loading_window = tk.Toplevel(root)
    loading_window.geometry("250x100")
    loading_window.overrideredirect(True)
    # Get the screen width and height for label placements
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    #these 2 lines of code are for screengometry basically where to place the root page
    rootx = (screen_width - 1400) // 2
    rooty = (screen_height - 700) // 2
    loading_window.geometry(f"+{x}+{y}")
    #create loading pop up
    loading_label = tk.Label(loading_window, text="Loading...", font=("Helvetica", 30))
    loading_label.pack(pady=0)
    loading_window.title("Loading...")
    loading_window.update()
    #create root page here
    root.title("VT")
    root.geometry("1400x700")
    root.maxsize(1400, 700)
    root.geometry(f"+{rootx}+{rooty}")

#############################################################################################################################################################
    # Initialize an empty string to store the classification results and a variable for each classification
    result_text = ""
    clean = 0
    malicious = 0
    spam = 0
    phishing = 0
    unrated = 0
##########################################################################################################################
    for website in urls_json:
        website = website.rstrip('>') #removing <> to make it into a string
        print(website)
        scan_request_parameters = {'apikey': apiKey, 'url': website} #using apikey and website it passeses these as parameters
        scan_response = requests.post(url_scan, data=scan_request_parameters) #send posts request using reuqest parameters
        json_data = scan_response.json() #scans URL

        if json_data.get('response_code') == 1: # checks there has been a successful response
            resource = json_data.get('resource')
            report_request = {'apikey': apiKey, 'resource': resource} #send parameters this time to retrieve the report
            report_response = requests.get(url_report, params=report_request)
            report_json = report_response.json() #stores JSON response from the report request

        vendorData = report_json.get('scans', {}) #Extract the 'scans' data from the report
        vendorDetails = ""
        for vendor, result in vendorData.items(): #Iterate through the vendors data items and concatenate vendor names and results
            vendorDetails += f"{vendor}: {result['result']}\n"

            #this block of codes counts the classifcation type of the url from each vendor
            classification = result['result']
            if classification == "clean site":
                clean += 1
            elif classification == "unrated site":
                unrated += 1
            elif classification == "malicious site":
                malicious += 1
            elif classification == "spam site":
                spam += 1
            elif classification == "phishing site":
                phishing += 1
        result_text += f"Vendor Info:\n{vendorDetails}\n\n"
        website1= "Url: ", website
##############################################################################################################################################
        # designing the root page here with labels and texboxes
        label = customtkinter.CTkLabel(master=root, text="Virus Total", font=("Helvetica", 80, "bold"))
        label.place(relx=0.02, rely=0.05, anchor=ctk.NW)

        label_frame = ctk.CTkScrollableFrame(root, orientation="horizontal", width=550, height=39)
        label_frame.place (relx=0.03, rely=0.2, anchor=ctk.NW)

        websitenamelabel = customtkinter.CTkLabel(label_frame, text=str(website), font=("Helvetica", 14, "bold"))
        websitenamelabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        text_box = scrolledtext.ScrolledText(master=root, font=("Helvetica", 14), height=25, width=60)
        text_box.place(relx=0.04, rely=0.3, anchor=ctk.NW)

##########################################################################################################################
        #this code makes a bar chart from the vendor information
        data = {'Rated as Clean': clean, 'Unrated': unrated, 'Rated as Malicious': malicious, 'Rated as Spam': spam, 'Rated as Phishing': phishing,}
        courses = list(data.keys())
        values = list(data.values())
        fig = plt.figure(figsize=(8, 4))
        colours = ['green', 'orange', 'red', 'red', 'red'] #set the colours of the bars here green = clean , red= bad

        # creating the bar plot
        bars = plt.bar(courses, values, color=colours, width=0.4)
        #plt.show()
        for bar in bars:
            plt.annotate(format(bar.get_height()),
                       (bar.get_x() + bar.get_width() / 2,
                        bar.get_height()), ha='center', va='center',
                       size=9, xytext=(0, 5),
                       textcoords='offset points')
        #makes a canvas to store the bar chart
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=ctk.NW)

##########################################################################################################################
        text_box.insert(tkinter.END, result_text) #inserts data into textbox
        time.sleep(1)
        root.after(1000, root.mainloop)


urls_json = None
##########################################################################################################################
# Example usage:
#URLS = ["https://click.email.edenred.co.uk/?qs=e6fdbf17f59eb9e1be5d6049c467ca8c53ddec87485da7dc303a82e19144d13919a0aa38d646e1212ab0d7bd6efe4bb3e2ccb85ae1ab738a47b04c588d27d796>"]
#check_urls_virustotal(URLS)