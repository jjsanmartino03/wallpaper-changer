import shutil
import os
import pathlib
import sys
import ctypes
from random import choice as random_choice
import re

import requests
from bs4 import BeautifulSoup


sections = [
    "https://quotefancy.com/motivational-quotes",
    "https://quotefancy.com/inspirational-entrepreneurship-quotes",
    "https://quotefancy.com/startup-quotes",
    "https://quotefancy.com/positive-quotes",
    "https://quotefancy.com/inspirational-quotes"
]


wallpapers_dir = os.path.join(pathlib.Path(__file__).parent.absolute(),"quotefancy-wallpapers")
if not os.path.exists(wallpapers_dir):
    os.mkdir(wallpapers_dir)

selected_section = random_choice(sections)

directory = os.path.join(wallpapers_dir, selected_section.split('/')[-1])

if not os.path.exists(directory):
    os.mkdir(directory)


response = requests.get(selected_section)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    hyperlinks = soup.find_all("a")

    img_links = []
    for link in hyperlinks:
        img = link.find("img")
        if img and img.get("data-original"):
            img_links.append(img['data-original'])

    if img_links:
        selected_image_link = random_choice(img_links)

        pattern = re.compile(r'(\d+x\d+)')

        selected_image_link = re.sub(pattern, '3840x2160', selected_image_link)
        print(selected_image_link)

        name = selected_image_link.split("/")[-1]
        res = requests.get(selected_image_link, stream=True)
        path = os.path.join(directory, name)

        with open(path, 'wb') as out_file:
            shutil.copyfileobj(res.raw, out_file)
        del res

    if sys.platform.startswith("win"):  # If running on windows
        SPI_SETDESKWALLPAPER = 20

        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, path, 0)

    elif sys.platform.startswith("linux"):  # If running on linux
        
        os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri " +
                  path.replace(' ', '\\ '))
