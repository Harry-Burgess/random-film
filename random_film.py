import random
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import webbrowser
import os
from time import sleep
import secrets as s
chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.default_content_settings.popups": 0,
    "download.default_directory": os.getcwd() + os.path.sep,
    "directory_upgrade": True
}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)
print(prefs)

def pick_film():
    driver.get("https://letterboxd.com/sign-in/")
    sleep(2)
    driver.find_element_by_xpath("//span[contains(text(), 'Continue to Site')]").click()
    driver.find_element_by_xpath("//input[@name='username']").send_keys(s.login["username"])
    driver.find_element_by_xpath("//input[@name='password']").send_keys(s.login["password"])
    driver.find_element_by_xpath("//input[@value='Sign in']").click()
    sleep(4)
    driver.get(f"https://letterboxd.com/{s.login['username'].lower()}/watchlist/export/")

    with open("watchlist.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        total_list = list(csv_reader)
        r_num = random.randint(1, len(total_list))
        selected_film = total_list[r_num - 1]

    title = selected_film['Name']
    year = selected_film['Year']
    URL = selected_film['Letterboxd URI']
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    poster = soup.find(attrs={"alt": selected_film['Name']})["src"]
    director = soup.find(id="featured-film-header").p.span.text
    runtime = soup.find(attrs={"class": "text-footer"}).text.strip().split("mins", 1)[0]
    runtime_hours = f"{int(runtime) // 60} hours {int(runtime) % 60} minutes"

    pb_link = f"https://thepiratebay.org/search.php?q={(selected_film['Name'] + '+' + selected_film['Year']).replace(' ', '+')}&all=on&search=Pirate+Search&page=0&orderby="
    jw_link = f"https://www.justwatch.com/uk/search?q={selected_film['Name'].replace(' ', '%20')}"

    html_output = ""
    html_output += f"\t\t<h1>{title} ({year})</h1>\n"
    html_output += f"\t\t<div class=\"frame\"><img src=\"{poster}\" alt=\"\"></div>\n"
    html_output += f"\t\t<span>Directed by {director} — {runtime_hours}</span>\n"
    html_output += f"\t\t<div class=\"links\">\n"
    html_output += f"\t\t\t<a href=\"{URL}\" target=\"_blank\">View on Letterboxd</a>\n"
    html_output += f"\t\t\t<a href=\"{jw_link}\" target=\"_blank\">How to watch</a>\n"
    html_output += f"\t\t\t<a href=\"{pb_link}\" target=\"_blank\">TPB</a>\n"
    html_output += f"\t\t</div>\n"
    html_output += f"\t</div>\n"
    html_output += f"</body>\n"
    html_output += f"</html>"

    index = "site-files/index.html"

    with open('site-files/before.html', 'r', encoding='utf-8') as before:
        before = before.read()

    with open(index, 'w') as filetowrite:
        filetowrite.write(before + html_output)

    webbrowser.open('file://' + os.path.realpath(index), new=2)


pick_film()
