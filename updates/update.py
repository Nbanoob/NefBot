from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
from datetime import date, timedelta, datetime
import os
import sys


main_url = "https://dragalialost.gamepedia.com"
bs_features = "html.parser"
db_location = "/database/master.db"
elements = {"Icon Element Flame.png": 1, "Icon Element Water.png": 2,
            "Icon Element Wind.png": 3, "Icon Element Light.png": 4,
            "Icon Element Shadow.png": 5}
weapons = {"Icon Weapon Sword.png": 1, "Icon Weapon Blade.png": 2,
           "Icon Weapon Dagger.png": 3, "Icon Weapon Axe.png": 4,
           "Icon Weapon Lance.png": 5, "Icon Weapon Bow.png": 6,
           "Icon Weapon Wand.png": 7, "Icon Weapon Staff.png": 8}
unit_types = {"Icon Type Row Attack.png": 1, "Icon Type Row Defense.png": 2,
              "Icon Type Row Healing.png": 3, "Icon Type Row Support.png": 4}
rarities = {"Icon Rarity Row 1.png": 1, "Icon Rarity Row 2.png": 2,
            "Icon Rarity Row 3.png": 3, "Icon Rarity Row 4.png": 4,
            "Icon Rarity Row 5.png": 5}
co_ops = {1: "Dragon Haste +15%", 2: "Strength +10%", 3: "Critical Rate +10%",
          4: "Defense +15%", 5: "HP +15%", 6: "Skill Haste +15%",
          7: "Skill Damage +15%", 8: "Recovery Potency +15%"}


def remove_tooltip_info(text):
    return text[text.index(')') + 1:text.index('(', text.index(')')) - 1]


def db_update_adventurers(names):
    for name in names:
        url = main_url + '/' + name
        content = urlopen(url).read()
        soup = BeautifulSoup(content, bs_features)
        panels = soup.find_all("div", class_="panel-heading")
        title = panels[0].find_all("div")[0].text
        images = soup.find_all("img")
        element = elements[images[0]["alt"]]
        weapon = weapons[images[1]["alt"]]
        unit_type = unit_types[images[4]["alt"]]
        rarity = rarities[images[5]["alt"]]
        hp_str_tooltips = soup.find_all("span", class_="tooltip")
        hp = remove_tooltip_info(hp_str_tooltips[0].text)
        strength = remove_tooltip_info(hp_str_tooltips[1].text)
        details = soup.find_all("div", class_="dd-description")
        defense = details[2].text.strip()
        release_date = details[12].text.strip()
        limited = 1
        if details[13].text.strip() == "Permanent":
            limited = 0
        co_op = co_ops[weapon]


def db_update_dragons(names):
    pass


def db_update_wyrmprints(names):
    pass


def db_update_weapons(names):
    pass


def pretty_print_name(name):
    return name.strip('/').replace('_', ' ').replace('%27', "'")


def get_first_table(sub_url):
    url = main_url + '/' + sub_url
    content = urlopen(url).read()
    soup = BeautifulSoup(content, features=bs_features)
    table = soup.find_all("table")[0]
    return table


def get_filtered_names(sub_url, from_date):
    table = get_first_table(sub_url)
    result = {}
    for tr in table.find_all("tr", class_="character-grid-entry grid-entry"):
        tds = tr.find_all("td")
        s_date = tds[-1].string.strip()
        true_date = datetime.strptime(s_date, "%b %d, %Y").date()
        if true_date > from_date:
            result[tds[0].find_all('a')[0]["href"]] = tr
    return result


def get_portraits(names, directory):
    print("--- Getting portraits for " + directory + " ---")
    os.makedirs(directory, exist_ok=True)
    for name, tr in names.items():
        pretty_name = pretty_print_name(name)
        print("Processing " + pretty_name)
        image = tr.find_all("a")[0].find_all("img")[0]["srcset"].split()[2]
        urlretrieve(image, directory + pretty_name + ".png")


def get_pictures(names, directory, i=0):
    print("--- Getting pictures for " + directory + " ---")
    os.makedirs(directory, exist_ok=True)
    for name, _ in names.items():
        pretty_name = pretty_print_name(name)
        print("Processing " + pretty_name)
        new_url = main_url + name
        new_content = urlopen(new_url).read()
        new_soup = BeautifulSoup(new_content, features="html.parser")
        new_url = main_url + new_soup.find_all("a", class_="image")[i]["href"]
        new_content = urlopen(new_url).read()
        new_soup = BeautifulSoup(new_content, features="html.parser")
        full_image_div = new_soup.find_all("div", class_="fullImageLink")[0]
        image = full_image_div.find_all("a")[0]["href"]
        urlretrieve(image, directory + pretty_name + ".png")


def update_items(item, sub_url, lookback_period_days):
    from_date = date.today() - timedelta(days=lookback_period_days)
    names = get_filtered_names(sub_url, from_date)
    get_portraits(names, item + "/portraits/")
    if item == "wyrmprints":  # Wyrmrpints have 2 pictures
        get_pictures(names, item + "/base/")
        get_pictures(names, item + "/full/", 1)
        db_update_wyrmprints(names)
        return
    elif item == "weapons":  # Weapons have no pictures
        db_update_weapons(names)
        return
    elif item == "dragons":
        db_update_dragons(names)
    elif item == "adventurers":
        db_update_adventurers(names)
    get_pictures(names, item + "/full/")


if __name__ == "__main__":
    retrieval_list = {"adventurers": "Adventurer_List",
                      "wyrmprints": "Wyrmprint_List",
                      "weapons": "Weapon_List",
                      "dragons": "Dragon_List"}
    lookback_period_days = 7
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        lookback_period_days = int(sys.argv[1])
    for k, v in retrieval_list.items():
        update_items(k, v, lookback_period_days)
