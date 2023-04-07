from tkinter import *
from tkinter import ttk
import json

# create the main window
root = Tk()
root.title("Job Listing Manager")

# create a frame to hold the listings
mainframe = ttk.Frame(root, padding = 10)
mainframe.pack()

# load listings from file
with open("code\listings.json", "r", encoding = "utf-8") as file:
    listings = json.loads(file.read())

for listing in listings:
    # listings are identified by the link
    # but refering to the listing object is more convienient
    link = listing
    listing = listings[listing]

    listing_frame = ttk.Frame(mainframe, borderwidth = 5, relief = "groove")
    listing_frame.pack()

    header_text = f'{listing["name"]} - {listing["employer"]} - {listing["location"]}'
    header_label = Label(listing_frame, text = header_text, padx = 5, pady = 5)
    header_label.grid(column = 0, row = 0, columnspan=4)

    end_date_label = Label(listing_frame, text = f'ends: {listing["end_date"]}')
    end_date_label.grid(column = 5, row = 0, sticky = "E")

    info_frame = ttk.Frame(listing_frame)
    info_frame.grid(column = 0, row = 1)

    contract_types = ", ".join([contract_type[0] for contract_type in listing["contract_type"].items() if contract_type[1]])
    contract_types_label = Label(info_frame, text = f'contract types: {contract_types}')
    contract_types_label.grid(column = 0, row = 0)

    seniorities = ", ".join([contract_type[0] for contract_type in listing["seniority"].items() if contract_type[1]])
    seniorities_label = Label(info_frame, text = f'seniorities: {seniorities}')
    seniorities_label.grid(column = 0, row = 1)

    work_from_home_options = ", ".join([contract_type[0] for contract_type in listing["work_from_home"].items() if contract_type[1]])
    work_from_home_options_label = Label(info_frame, text = f'work from home options: {work_from_home_options}')
    work_from_home_options_label.grid(column = 1, row = 0)

    full_time_label = Label(info_frame, text = f'full time: {listing["full-time"]}')
    full_time_label.grid(column = 1, row = 1)

    for element in info_frame.children.values():
        element.grid(sticky = "W")

    pay_regularity = [regularity[0] for regularity in listing["pay_regularity"].items() if regularity[1]][0]
    pay_text = f'{listing["pay"][0]} - {listing["pay"][1]} {pay_regularity}'
    pay_label = Label(listing_frame, text = pay_text)
    pay_label.grid(column = 5, row = 1)

    required_skills_frame = ttk.Frame(listing_frame)
    required_skills_frame.grid(column = 0, row = 2)
    required_skills_header_label = Label(required_skills_frame, text = "required skills:")
    required_skills_header_label.grid(column = 0, row = 0, sticky = "W")
    required_skills_text = ", ".join(listing["required_skills"])
    required_skills_label = Label(required_skills_frame, text = required_skills_text)
    required_skills_label.grid(column = 0, row = 1, sticky = "W")

    nice_to_haves_frame = ttk.Frame(listing_frame)
    nice_to_haves_frame.grid(column = 0, row = 3)
    nice_to_haves_header_label = Label(nice_to_haves_frame, text = "nice to haves:")
    nice_to_haves_header_label.grid(column = 0, row = 0, sticky = "W")
    nice_to_haves_text = ", ".join(listing["nice_to_haves"])
    nice_to_haves_label = Label(nice_to_haves_frame, text = nice_to_haves_text)
    nice_to_haves_label.grid(column = 0, row = 1, sticky = "W")

    benefits_frame = ttk.Frame(listing_frame)
    benefits_frame.grid(column = 0, row = 4)
    benefits_header_label = Label(benefits_frame, text = "benefits:")
    benefits_header_label.grid(column = 0, row = 0, sticky = "W")
    benefits_text = ", ".join(listing["benefits"])
    benefits_label = Label(benefits_frame, text = benefits_text)
    benefits_label.grid(column = 0, row = 1, sticky = "W")

    link_label = Label(listing_frame, text = link)
    link_label.grid(column = 0, row = 5)

    for element in listing_frame.children.values():
        element.grid(sticky = "W")

# start the main loop
root.mainloop()
