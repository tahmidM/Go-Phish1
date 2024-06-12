import customtkinter
import customtkinter as ctk


def about():
    root = customtkinter.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    rootx = (screen_width - 700) // 2
    rooty = (screen_height - 400) // 2
    root.title("About")
    root.geometry("1400x700")
    root.maxsize(700, 400)
    root.geometry(f"+{rootx}+{rooty}")

    label = customtkinter.CTkLabel(master=root, text="About", font=("Helvetica", 70, "bold"))
    label.place(relx=0.5, rely=0.05, anchor=ctk.N)

    r="GO-Phish is an email-based phishing detection tool that can be connected to your mailbox. It has the capabilities to investigate a potential phishing URL through the VirusTotal API or its very own custom built machine learning model. If you want to see what the potential Phishing webpage looks like, just simply select a URL and click the screenshot button which will show you the webpage in seconds ! And if you’re worried someone has clicked the link or received the same email just click on the search logs button to investigate further 😊"

    label1 = customtkinter.CTkLabel(master=root, text=str(r), font=("Helvetica", 17, "bold"),wraplength=700)
    label1.place(relx=0.5, rely=0.35, anchor=ctk.N)

    root.mainloop()


def helpInfo():
    root = customtkinter.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    rootx = (screen_width - 750) // 2
    rooty = (screen_height - 400) // 2
    root.title("Help")
    root.geometry("1400x700")
    root.maxsize(750, 400)
    root.geometry(f"+{rootx}+{rooty}")

    # Create and place the label
    label = customtkinter.CTkLabel(master=root, text="Help", font=("Helvetica", 70, "bold"))
    label.grid(row=0, column=0, columnspan=2, pady=(20, 0))

    r = """1. Virus Total is a service that can take a URL and check it against multiple security vendors and report back if the URL may be malicious or clean! 
Remember: The API is an open-source intelligence tool so it's important you do not just use this technique by itself as it very well could tell you a link is clean but in reality, it is not!

2. The machine learning in this tool is a smart bit of code that can take a URL and predict if it can be phishing or not, it will give you a prediction score to tell you how likely it is a phishing URL.

3. The redirect label is populated when you scan a URL, it checks that there are no redirects within the link that might take you to another webpage! 
Hint: If the redirect link is very different from the URL in the email, it is likely they are directing you to a phishing website!

4. The ‘search logs’ button searches through your mail server logs for any emails that have the same sender. It can also check for anyone who has visited the URL within your business. 
Hint: This can help you find more phishing emails; if the email you are exploring is phishing and the logs show this sender has sent other emails, it is likely these emails are also phishing!

    Tips:
    - Check the grammar of the email.
    - Check the sender of the email, is it trying to pretend to be someone it isn’t?
    - Is the webpage trying to redirect you?
    - Think of Web Proxy Logs as your search history, but just for every website you and anyone on your network might visit!
    - POST 200 connections on the web-proxy checks indicate a user might have entered their credentials into a site """

    root.grid_rowconfigure(1, weight=1)  # Adjusted row configuration

    tk_textbox = customtkinter.CTkTextbox(root, activate_scrollbars=False, width=730)
    tk_textbox.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
    tk_textbox.insert("1.0", r)

    ctk_textbox_scrollbar = customtkinter.CTkScrollbar(root, command=tk_textbox.yview)
    ctk_textbox_scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 20))

    tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

    root.mainloop()

