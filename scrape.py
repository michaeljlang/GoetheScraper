# import requests
# import urllib.request
import re
import time
import json
import os 

from utils import *
from meta import *
from goethe_scraper import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs

#create/set directory
current_path = os.getcwd()
if os.path.exists("Goethe") == False:
    os.mkdir("Goethe")
    os.chdir("Goethe")
    print("New folder created: Goethe")
    print("New working directory:", os.getcwd())
elif current_path.split("/")[-1] != "Goethe":
    os.chdir("Goethe")
    print("New working directory:", os.getcwd())


# ------------ Obtaining links to the articles ------------
# Only get Spanish links
url = "https://www.goethe.de/ins/es/es/kul/mag.html"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)

while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")       
        WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.ID, 'loadMore')))
        time.sleep(5)
        driver.find_element(By.ID, 'loadMore').click()
        time.sleep(8)
    except NoSuchElementException:
        print("Error! Element not found.")
        break
    except ElementClickInterceptedException:
        print("Warning! It is likely that the process did complete correctly.\nYou may want to rerun the program.")
        break
    except:
        break

html = driver.page_source
driver.quit()
soup = bs(html, 'html5lib')

# Find all the links on the page
links = soup.find_all("a")

all_links = []
for link in links:
    href = link.get("href")
    if href:
        all_links.append(href)

# select valid links and exclude pages that are only videos (marked with drf)
final_links = [x for x in all_links if x.startswith('https:') and x.endswith('html') and "drf" not in x] 

# save links
with open("links.txt","w") as f:
    for item in final_links:
        f.write(item + "\n")

# create set of links to German articles:
final_links_de = []
for link in final_links:
    de_link = re.sub("es/es","es/de",link)
    final_links_de.append(de_link)


# ------------ Processing the articles ------------
# extract texts
texts_es = goethe_scraper(final_links)
texts_de = goethe_scraper(final_links_de)

# eliminate discarded articles and reorder the article ids
all_discard = set()
[all_discard.add(item) for item in texts_es[3].keys()]
[all_discard.add(item) for item in texts_de[3].keys()]

remove_discarded = (lambda x: [x.pop(key) for key in all_discard])
[remove_discarded(item) for item in texts_es[:3]]
[remove_discarded(item) for item in texts_de[:3]]

spanish_articles = reorder(texts_es[0])
spanish_metadata = reorder(texts_es[1])
spanish_titles = reorder(texts_es[2])

german_articles = reorder(texts_de[0])
german_metadata = reorder(texts_de[1])
german_titles = reorder(texts_de[2])

# write all texts to txt and json files
with open("articles_es.txt", "w") as f:
    for k,v in spanish_articles.items():
        f.write(k + "\n" + v + "\n")

with open("articles_es.json", "w") as f:
    f.write(json.dumps(spanish_articles,ensure_ascii=False))

with open("articles_de.txt", "w") as f:
    for k,v in german_articles.items():
        f.write(k + "\n" + v + "\n")

with open("articles_de.json", "w") as f:
    f.write(json.dumps(german_articles,ensure_ascii=False))

# get and write metadata to file
get_meta(spanish_metadata, german_metadata, spanish_titles, german_titles)

