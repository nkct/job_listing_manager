from tkinter import *
from tkinter import ttk
import json

# create the main window
root = Tk()
root.title("Job Listing Manager")

# create a frame to hold the listings
mainframe = ttk.Frame(root, padding=10)
mainframe.pack()

# load listings from file
with open("code\listings.json", "r", encoding="utf-8") as file:
    listings = json.loads(file.read())

for listing in listings:
    link = listing
    listing = listings[listing]

    main_box = ttk.Frame(mainframe, borderwidth=5, relief="groove")
    main_box.pack(pady=5)

    header_text = f'{listing["name"]} - {listing["employer"]} - {listing["location"]}'
    header_label = Label(main_box, text=header_text, padx=5, pady=5)
    header_label.pack(side="left")


# start the main loop
root.mainloop()
