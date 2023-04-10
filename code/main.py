from tkinter import *
from tkinter import ttk
import json
import requests
from bs4 import BeautifulSoup
import webbrowser

# create the main window
root = Tk()
root.title("Job Listing Manager")

# create a frame to hold the listings
mainframe = ttk.Frame(root, padding = 10)
mainframe.pack()

def scrape(listing_url: str) -> dict:
    page = requests.get(listing_url)

    soup = BeautifulSoup(page.content, "html.parser")

    try:
        name = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > div > div.offer-viewgQQ3bw > div > h1").text
    except AttributeError:
        name = "N/A"
    try:
        employer = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > div > div.offer-viewgQQ3bw > div > h2").contents[0]
    except AttributeError:
        employer = "N/A"
    try:
        location = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(1) > div > div > a").text
    except AttributeError:
        location = "N/A"
    try:
        end_date = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(2) > div > div > div.offer-viewDZ0got").text.split(": ")[1]
    except AttributeError:
        end_date = "N/A"
    
    try:
        contract_types = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(3) > div > div > div").text
        contract_type = {
            "coe": "umowa o pracę" in contract_types.lower(),
            "b2b": "b2b" in contract_types.lower(),
            "coc": "zlecenie" in contract_types.lower(),
        }
    except AttributeError:
        contract_type = "N/A"
    
    try:
        seniorities = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(5) > div > div > div").text
        seniority = {
            "senior": "senior" in seniorities.lower(),
            "mid": "mid" in seniorities.lower(),
            "junior": "junior" in seniorities.lower(),
        }
    except AttributeError:
        seniority = "N/A"
    
    try:
        work_from_home_options = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(6) > div > div > div").text
        work_from_home = {
            "on_site": "stacjonarna" in work_from_home_options.lower(),
            "hybrid": "hybrydowa" in work_from_home_options.lower(),
            "remote": "zdalna" in work_from_home_options.lower(),
        }
    except AttributeError:
        work_from_home = "N/A"
    
    # change to etat: pelny/częściowy
    try:
        full_time_text = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(4) > div > div > div").text
        full_time = "pełny etat" in full_time_text.lower()
    except AttributeError:
        full_time = "N/A"
    
    try:
        remote_recruitment_text = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(9) > div > div > div").text
        remote_recruitment = "rekrutacja zdalna" in remote_recruitment_text.lower()
    except AttributeError:
        remote_recruitment = "N/A"

    try:
        pay_info = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > div > div.offer-viewiafL8R > div > strong").find_all("span", recursive = False)
        pay = [filter(str.isdigit, pay_info[0].text), filter(str.isdigit, pay_info[1].text)]
        pay = [int("".join(pay)) for pay in pay]
    except AttributeError:
        pay = "N/A"

    try:
        pay_regularity_options = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > div > div.offer-viewiafL8R > div > span").text
        pay_regularity = {
            "yearly": "rocznie" in pay_regularity_options.lower(),
            "monthly": "mies" in pay_regularity_options.lower(),
            "hourly": "godz" in pay_regularity_options.lower(),
        }
    except AttributeError:
        pay_regularity = "N/A"
        
    try:
        required_skills = []
        required_skills_list = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div:nth-child(3) > div:nth-child(2) > ul")
        for required_skill in required_skills_list.contents:
            required_skills.append(required_skill.contents[0].text)
    except AttributeError:
        required_skills = "N/A"

    try:
        nice_to_haves = []
        nice_to_haves_list = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div:nth-child(3) > div:nth-child(4) > ul")
        for nice_to_have in nice_to_haves_list.contents:
            nice_to_haves.append(nice_to_have.contents[0].text)
    except AttributeError:
        nice_to_haves = "N/A"

    try:
        benefits = []
        benefits_list = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > section.offer-viewJsKTWk > ul")
        for benefit in benefits_list.contents:
            benefits.append(benefit.contents[0].contents[1].text)
    except AttributeError:
        benefits = "N/A"

    return {
        "name": name,
        "employer": employer,
        "location": location,
        "end_date": end_date,
        "contract_type": contract_type,
        "seniority": seniority,
        "work_from_home": work_from_home,
        "full-time": full_time,
        "remote_recruitment": remote_recruitment,
        "pay": pay,
        "pay_regularity": pay_regularity,
        "required_skills": required_skills,
        "nice_to_haves": nice_to_haves,
        "benefits": benefits,
    }

def scrape_new_button_click():
    # create a new window
    submit_url_window = Toplevel(root)
    submit_url_window.geometry("500x100")
    submit_url_window.title("Submit url for scraping")

    # create the text input box and submit button
    input_label = Label(submit_url_window, text="Enter url:")
    input_label.pack(pady = 10)
    input_box = Entry(submit_url_window, width = 70)
    input_box.pack(pady=5)

    def submit_button_click():
        url = input_box.get()
        listing = scrape(url)
        with open("code\listings.json", "r", encoding = "utf-8") as file:
            listings = json.loads(file.read())
            listings[url] = listing
            with open("code\listings.json", "w", encoding = "utf-8") as file:
                file.write(json.dumps(listings, indent=4))

        display_listings()
        submit_url_window.destroy()


    submit_button = Button(submit_url_window, text="Submit", command = submit_button_click)
    submit_button.pack(pady=5)

scrape_new_button = ttk.Button(mainframe, text="Scrape new", command = scrape_new_button_click)
scrape_new_button.pack()

listings_frame = ttk.Frame(mainframe)
listings_frame.pack()

def display_listings():
    # load listings from file
    with open("code\listings.json", "r", encoding = "utf-8") as file:
        listings = json.loads(file.read())

    for child in listings_frame.winfo_children():
        child.destroy()

    for listing in listings:
        # listings are identified by the link
        # but refering to the listing object is more convienient
        link = listing
        listing = listings[listing]

        listing_frame = ttk.Frame(listings_frame, borderwidth = 5, relief = "groove")
        listing_frame.pack()

        header_text = f'{listing["name"]} - {listing["employer"]} - {listing["location"]}'
        header_label = Label(listing_frame, text = header_text, padx = 5, pady = 5)
        header_label.grid(column = 0, row = 0, columnspan=4)

        end_date_label = Label(listing_frame, text = f'ends: {listing["end_date"]}')
        end_date_label.grid(column = 5, row = 0, sticky = "E")

        info_frame = ttk.Frame(listing_frame)
        info_frame.grid(column = 0, row = 1)

        contract_types = "N/A" if listing["contract_type"] == "N/A" or not any(contract_type[1] for contract_type in listing["contract_type"].items()) else ", ".join([contract_type[0] for contract_type in listing["contract_type"].items() if contract_type[1]])
        contract_types_label = Label(info_frame, text = f'contract types: {contract_types}')
        contract_types_label.grid(column = 0, row = 0)

        seniorities = "N/A" if listing["seniority"] == "N/A" or not any(seniority[1] for seniority in listing["seniority"].items()) else ", ".join([seniority[0] for seniority in listing["seniority"].items() if seniority[1]])
        seniorities_label = Label(info_frame, text = f'seniorities: {seniorities}')
        seniorities_label.grid(column = 0, row = 1)

        work_from_home_options = "N/A" if listing["work_from_home"] == "N/A" or not any(work_from_home_option[1] for work_from_home_option in listing["work_from_home"].items()) else ", ".join([work_from_home_option[0] for work_from_home_option in listing["work_from_home"].items() if work_from_home_option[1]])
        work_from_home_options_label = Label(info_frame, text = f'work from home options: {work_from_home_options}')
        work_from_home_options_label.grid(column = 1, row = 0)

        full_time_label = Label(info_frame, text = f'full time: {listing["full-time"]}')
        full_time_label.grid(column = 1, row = 1)

        for element in info_frame.children.values():
            element.grid(sticky = "W")

        pay_regularity = "" if listing["pay_regularity"] == "N/A" else [regularity[0] for regularity in listing["pay_regularity"].items() if regularity[1]][0]
        pay_text = "N/A" if listing["pay"] == "N/A" else f'{listing["pay"][0]} - {listing["pay"][1]} {pay_regularity}'
        pay_label = Label(listing_frame, text = pay_text)
        pay_label.grid(column = 5, row = 1)

        required_skills_frame = ttk.Frame(listing_frame)
        required_skills_frame.grid(column = 0, row = 2)
        required_skills_header_label = Label(required_skills_frame, text = "required skills:")
        required_skills_header_label.grid(column = 0, row = 0, sticky = "W")
        required_skills_text = "N/A" if listing["required_skills"] == "N/A" else ", ".join(listing["required_skills"])
        required_skills_label = Label(required_skills_frame, text = required_skills_text)
        required_skills_label.grid(column = 0, row = 1, sticky = "W")

        nice_to_haves_frame = ttk.Frame(listing_frame)
        nice_to_haves_frame.grid(column = 0, row = 3)
        nice_to_haves_header_label = Label(nice_to_haves_frame, text = "nice to haves:")
        nice_to_haves_header_label.grid(column = 0, row = 0, sticky = "W")
        nice_to_haves_text = "N/A" if listing["nice_to_haves"] == "N/A" else ", ".join(listing["nice_to_haves"])
        nice_to_haves_label = Label(nice_to_haves_frame, text = nice_to_haves_text)
        nice_to_haves_label.grid(column = 0, row = 1, sticky = "W")

        benefits_frame = ttk.Frame(listing_frame)
        benefits_frame.grid(column = 0, row = 4)
        benefits_header_label = Label(benefits_frame, text = "benefits:")
        benefits_header_label.grid(column = 0, row = 0, sticky = "W")
        benefits_text = "N/A" if listing["benefits"] == "N/A" else ", ".join(listing["benefits"])
        benefits_label = Label(benefits_frame, text = benefits_text)
        benefits_label.grid(column = 0, row = 1, sticky = "W")

        link_label = Label(listing_frame, text = link, fg = "#0000EE")
        link_label.grid(column = 0, row = 5)
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new(link))

        for element in listing_frame.children.values():
            element.grid(sticky = "W")

        def delete_listing_button_click():
            with open("code\listings.json", "r", encoding = "utf-8") as file:
                listings = json.loads(file.read())
                listings.pop(link)
                with open("code\listings.json", "w", encoding = "utf-8") as file:
                    file.write(json.dumps(listings, indent=4))
            display_listings()

        delete_listing_button = ttk.Button(listing_frame, text="Delete", command = delete_listing_button_click)
        delete_listing_button.grid(column = 0, row = 6)

        def update_listing_button_click():
            listing = scrape(link)
            with open("code\listings.json", "r", encoding = "utf-8") as file:
                listings = json.loads(file.read())
                listings[link] = listing
                with open("code\listings.json", "w", encoding = "utf-8") as file:
                    file.write(json.dumps(listings, indent=4))
            display_listings()

        update_listing_button = ttk.Button(listing_frame, text="Update", command = update_listing_button_click)
        update_listing_button.grid(column = 1, row = 6)

display_listings()

# start the main loop
root.mainloop()