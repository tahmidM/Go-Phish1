from imapclient import IMAPClient
import email
import re
import tkinter.messagebox
from tkinter import scrolledtext
from newWindowFunction import new_window
import customtkinter
import customtkinter as ctk
from bs4 import BeautifulSoup
from VT import check_urls_virustotal
from URL_Screenshot import take_screenshot
import json
import customtkinter
from log_Checker import search_logs
from ML import machine_learning
import requests


p = re.compile(r'http[s]?://\S+') # this line is used to find a URL and is regex code

# Global variable to keep track of email index
email_index = [0]
current_json = {} # contains the value of the the current URL in a JSON format
#sets global variables to be accessed anywhere in the code
current = None
redirect = None

def display_email_details(index_list):
    #establishes connection to IMAP server to retieve email
    index = index_list[0]

    # Account credentials
    username = "phishing_referrals@outlook.com"  # Replace with your actual email address
    password = ("Manchester123*")  # Replace with your actual password

    # New IMAP server details
    imap_server = "outlook.office365.com"
    imap_port = 993

    # Connect to the IMAP server
    with IMAPClient(imap_server, port=imap_port, use_uid=True, ssl=True) as client:
        client.login(username, password)

        # Select the inbox
        client.select_folder("inbox")

        # Search for all emails and retrieve the specified one
        email_id_list = client.search(["ALL"])
    #validation testing to check if the emails exist
        if not email_id_list or index < 0 or index >= len(email_id_list):
            # No emails or invalid index
            print("No emails or invalid index. Email index:", index)
            return

        email_id = email_id_list[index]

        # collects the email data using RFC822 which is the ascii format for emails
        raw_message_data = client.fetch([email_id], ["RFC822"])
        raw_message = raw_message_data[email_id][b"RFC822"]

        # Parse the email data
        message = email.message_from_bytes(raw_message)
        sender_email = email.utils.parseaddr(message.get('From'))[1]
        recipient_email = email.utils.parseaddr(message.get('To'))[1]
        date = message.get('Date')
        #code in the function below gets the subject line from the email and decodes it into latin so it us plain engish
        def get_subject():
            subject = message.get('Subject')
            if subject:
                decoded_subject = email.header.decode_header(subject)[0][0]
                if isinstance(decoded_subject, bytes):
                    # If the subject is bytes, decode it to string using UTF-8
                    subject = decoded_subject.decode('latin1')
            else:
                # If the subject is already a string, keep it as is
                subject = decoded_subject
            return subject

        subject = get_subject()
    #the function below loops through the message to find URLs within the content
    def update_urls_label():
        from bs4 import BeautifulSoup
        urls1 = ""
        for part in message.walk():
            if part.get_content_type() == "text/plain": #if content is in plain text
                test_str = part.as_string()
                urls0 = p.findall(test_str) #searches entire message to look for URLS using 'p' which is the regx for a url
                urls1 = "\n".join(urls0) #gets a list of urls and appends to string each time a new URL is found
            elif part.get_content_type() == "text/html": #if text is in html the data need to be pasred so it can be read in plain english
                html_content = part.get_payload(decode=True).decode(part.get_content_charset())
                soup = BeautifulSoup(html_content, 'html.parser')
                # Extract text content from BeautifulSoup object
                text_content = soup.get_text()
                urls00 = [link.get('href') for link in soup.find_all('a', href=True)]
                urls1 = "\n".join(urls00)

        urls1 = "\n".join(url.lstrip() for url in urls1.splitlines()) # This splits the string urls1 into a list of strings based on newline characters (\n)

        return urls1  # Return the value after the loop

    urls1 = update_urls_label()  # Call the function
    urls_list = urls1.split('\n')#Split the 'urls1' string into a list of URLs using newline character ('\n') as the delimiter
    urls_json = json.dumps(urls_list) # turns it into a JSON
    urls_list = json.loads(urls_json) #Parse the JSON-formatted string back into a Python list and assign it back to 'urls_list'
    print(urls_list)

##############################################################################################################################################
    #this function gets the redirect URL
    def get_final_url(url):
        try:
            response = requests.head(url, allow_redirects=True)
            final_url = response.url
            return final_url
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None

    ##################################################################
    def on_combobox_select(event): #repsonsible for updating the combo box selections
        global current_json
        global redirect
        current = url_value.get() #Gets the current value from the ComboBox
        if current: #check selection is not empty
            current_json = {current} #creates a json of the current URL selected
            redirect = get_final_url(current)#calls redirect function above, too find the redirect URL
            redirect_url_label.configure(text=redirect)#updates the label directly here
        else:
            # print("Current value is empty")
            return redirect, current_json # If the current value is empty, return the redirect URL and current JSON
##############################################################################################################################################
    #simply either adding 1 or taking away 1 from index to go to previous or next email
    def next_email():
        global current_json
        current_json = None
        if index + 1 < len(email_id_list):
            index_list[0] += 1
            root.after(2000, root.destroy)
            display_email_details(index_list)
        elif index == len(email_id_list) - 1:
            tkinter.messagebox.showerror("Error", "You have reached the last email.") #displays error if next is clicked whilst on last email
            return

    def previous_email():
        global current_json
        current_json = None
        if index - 1 >= 0:
            index_list[0] -= 1
            root.after(2000, root.destroy) #destroys old page after 2 seconds of new page opening to allow seamless transition
            display_email_details(index_list)
        elif index == 0:
            tkinter.messagebox.showerror("Error", "This is the first email !") ##displays error if previous is clicked whilst on first email
            return
##############################################################################################################################################
    # Create the Tkinter window here and ADD labels
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.title("Inbox View")
    root.geometry("1400x700")
    root.maxsize(1400, 700)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - 1400) // 2
    y = (screen_height-700) // 2
    root.geometry(f"+{x}+{y}")

    # Create and place the title label
    label = customtkinter.CTkLabel(master=root, text="Inbox View", font=("Helvetica", 80, "bold"))
    label.place(relx=0.02, rely=0.05, anchor=ctk.NW)
    ##############################################################################################################################################
    #setting and configuring previous and next buttons in this section of code
    button_font = ("Helvetica", 25, "bold")

    next_button = customtkinter.CTkButton(root, text="    Next    ", height=30, width=70, command=next_email,
                                          font=button_font)
    next_button.place(relx=0.2, rely=0.9, anchor=ctk.CENTER)

    previous_button = customtkinter.CTkButton(root, text="Previous", height=30, width=70, command=previous_email,
                                              font=button_font)
    previous_button.place(relx=0.1, rely=0.9, anchor=ctk.CENTER)
    ##############################################################################################################################################

    width_pixels = root.winfo_width() # to make screen size an layout consident these cooridnates are used
    gap_relx = 5 / width_pixels #works out what gap to leave between the sides of the page

    label_frame = ctk.CTkScrollableFrame(root,orientation="horizontal",width=600,height=300) #creates a frame bar to contain below code
    label_frame.place(relx=gap_relx, rely=0.2, anchor=ctk.NW)

    #adds following labels to dataframe and uses a grid for consistent layout
    label_font = ("Helvetica", 25, "bold")
    # Labels for URL, sender, and recipient fields
    sender_label = ctk.CTkLabel(label_frame, text="Sender:", font=label_font)
    sender_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    sender_value = ctk.CTkLabel(label_frame, text=sender_email, font=label_font)
    sender_value.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    recipient_label = ctk.CTkLabel(label_frame, text="Recipient:", font=label_font)
    recipient_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    recipient_value = ctk.CTkLabel(label_frame, text=recipient_email, font=label_font)
    recipient_value.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    date_label = ctk.CTkLabel(label_frame, text="Date:", font=label_font)
    date_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
    date_value = ctk.CTkLabel(label_frame, text=date, font=label_font)
    date_value.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    subject_label = ctk.CTkLabel(label_frame, text="Subject:", font=label_font)
    subject_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
    subject_value = ctk.CTkLabel(label_frame, text=subject, font=label_font,anchor="w", justify="left")
    subject_value.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    url_label = ctk.CTkLabel(label_frame, text="URL:", font=label_font,justify="left")
    url_label.grid(row=4, column=0, sticky="nw", padx=5, pady=5)
    url_value = ctk.CTkComboBox(label_frame, values=["Select a URL"] + urls_list, font=label_font, width=400,command=on_combobox_select)
    url_value.grid(row=4, column=1, sticky="w", padx=5, pady=5)

    redirect_url_label = ctk.CTkLabel(label_frame, text="Redirect Url:", font=label_font,justify="left")
    redirect_url_label.grid(row=5, column=0, sticky="nw", padx=5, pady=5)
    redirect_url_label = ctk.CTkLabel(label_frame,text="", font=label_font, width=400,anchor="w")
    redirect_url_label.grid(row=5, column=1, sticky="w", padx=5, pady=5)


    # Bind the callback function to the <<ComboboxSelected>> event
    url_value.bind("<<ComboboxSelected>>", on_combobox_select)
######################################################################################################################################################################################################################
    width_pixels1 = root.winfo_width()
    gap_relx1 = 100 / width_pixels1 #adjust these figures to place the text box
    email_content = scrolledtext.ScrolledText(root, wrap=ctk.WORD, width=80, height=30) #scroll text bar to contain email content
    email_content.place(relx=gap_relx1, rely=0.05, anchor=ctk.NW)

    from bs4 import BeautifulSoup

    def update_text_box():
        email_content1 = None
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                # For plain text email content
                email_content1 = part.get_payload(decode=True).decode(part.get_content_charset())
                break  # Exit the loop once plain text is found
        if email_content1 is None:
            # If no plain text is found, try HTML content
            for part in message.walk():
                if part.get_content_type() == "text/html":
                    # For HTML email content
                    html_content = part.get_payload(decode=True).decode(part.get_content_charset())
                    # Parse HTML content using BeautifulSoup
                    soup = BeautifulSoup(html_content, 'html.parser')
                    # Extract text from the parsed HTML
                    email_content1 = '\n'.join(line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip())
                    break
        if email_content1 is not None:
            # Update the email content in the text box
            email_content.delete(1.0, ctk.END)  # Clear existing content
            email_content.insert(ctk.END, email_content1)
            # Clear existing content
            email_content.delete(1.0, ctk.END)
            # Insert the new content into the scrolled text box
            email_content.insert(ctk.END, email_content1)
    # Call the function to update the text box with email content
    update_text_box()
#############################################################################################################################################
    button_frame = ctk.CTkFrame(root, width=500, height=200) #places all buttons in a frame
    button_frame.place(relx=0.55, rely=0.77, anchor=ctk.NW)

    button1_font = ("Helvetica", 26, "bold") #all buttons share consistent font and theme

    #lambda function ised in all button commands so code from other oages are only ran when button is clicked
    #grid is used place buttons
    vt_button = ctk.CTkButton(button_frame, text="      Virus Total      ", height=60, width=120, font=button1_font,
                              command=lambda: check_urls_virustotal(current_json))
    vt_button.grid(row=0, column=0, padx=5, pady=5)

    ss_button = ctk.CTkButton(button_frame, text="  URL Screenshot  ", height=60, width=120, font=button1_font,
                              command=lambda: take_screenshot(current_json))
    ss_button.grid(row=0, column=1, padx=5, pady=5)

    ml_button = ctk.CTkButton(button_frame, text="Machine Learning", height=60, width=120, font=button1_font,
                              command=lambda: machine_learning(current_json))
    ml_button.grid(row=1, column=0, padx=5, pady=5)

    logs_button = ctk.CTkButton(button_frame, text="     Search logs      ", height=60, width=120,
                                      font=button1_font, command=lambda: search_logs(current_json, sender_email))
    logs_button.grid(row=1, column=1, padx=5, pady=5)

    root.mainloop()

##############################################################################################################################################
# Call the function to display email details with the initial index
#display_email_details(email_index)
