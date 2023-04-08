from tkinter import *
from tkinter import ttk
import json
import requests
from bs4 import BeautifulSoup

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

def scrape(listing_url: str) -> dict:
    page = requests.get(listing_url)

    soup = BeautifulSoup(page.content, "html.parser")

    name = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > div > div.offer-viewgQQ3bw > div > h1").text
    employer = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > div > div.offer-viewgQQ3bw > div > h2").text
    location = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(1) > div > div > a").text
    end_date = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(2) > div > div > div.offer-viewDZ0got").text.split(": ")[1]
    
    contract_types = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(3) > div > div > div").text
    contract_type = {
        "coe": "umowa o pracę" in contract_types.lower(),
        "b2b": "b2b" in contract_types.lower(),
        "coc": "zlecenie" in contract_types.lower(),
    }

    seniorities = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(5) > div > div > div").text
    seniority = {
        "senior": "senior" in seniorities.lower(),
        "mid": "mid" in seniorities.lower(),
        "junior": "junior" in seniorities.lower(),
    }

    work_from_home_options = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(6) > div > div > div").text
    work_from_home = {
        "on_site": "stacjonarna" in work_from_home_options.lower(),
        "hybrid": "hybrydowa" in work_from_home_options.lower(),
        "remote": "zdalna" in work_from_home_options.lower(),
    }

    full_time = "pełny etat" in soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(4) > div > div > div").text.lower()
    remote_recruitment = "rekrutacja zdalna" in soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > ul > li:nth-child(9) > div > div > div").text.lower()

    pay_info = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > div > div.offer-viewiafL8R > div > strong").find_all("span", recursive = False)
    pay = [filter(str.isdigit, pay_info[0].text), filter(str.isdigit, pay_info[1].text)]
    pay = [int("".join(pay)) for pay in pay]
    pay_regularity_options = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div.offer-view8N6um9 > div > div.offer-viewiafL8R > div > span").text
    pay_regularity = {
        "yearly": "rocznie" in pay_regularity_options.lower(),
        "monthly": "mies" in pay_regularity_options.lower(),
        "hourly": "godz" in pay_regularity_options.lower(),
    }

    try:
        required_skills = []
        required_skills_list = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div:nth-child(3) > div:nth-child(2) > ul")
        for required_skill in required_skills_list.findChildren():
            required_skills.append(required_skill.find("p").text)
    except AttributeError:
        required_skills = "N/A"

    try:
        nice_to_haves = []
        nice_to_haves_list = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > div:nth-child(3) > div:nth-child(3) > ul")
        for nice_to_have in nice_to_haves_list.findChildren():
            nice_to_haves.append(nice_to_have.find("p").text)
    except AttributeError:
        nice_to_haves = "N/A"

    try:
        benefits = []
        benefits_list = soup.select_one("#kansas-offerview > div > div.offer-viewzxQhTZ.offer-viewT4OXJG > section.offer-viewJsKTWk > ul")
        for benefits in benefits_list.findChildren():
            benefits.append(benefits.find("article").find("p").text)
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

test_url = "https://www.pracuj.pl/praca/junior-programista-c%23-developer-warszawa-cybernetyki-9,oferta,1002444152"
test_listing = scrape(test_url)
with open("./code/actual_listings.json", "w") as file:
    test_listings = {test_url: test_listing}
    file.write(json.dumps(test_listings, indent=4))