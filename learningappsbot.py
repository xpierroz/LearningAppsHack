import requests 
import random
import re

from selenium import webdriver
from time import sleep

option = webdriver.ChromeOptions()
option.binary_location = "chromedriver.exe"
driver = webdriver.Chrome()

link = input("LearningApps.org link: ")
namex = input("Name: ")
nameid = input("Name ID (is after id= in the url, exemple: watch?id=pxvfz1nw523, ths ID is pxvfz1nw523): ")

print("Scraping the list of exercices...")
driver.get(link)
sleep(0.5)

itemListLength = driver.execute_script("""
    return itemList.length;
""")

with open("scrap_data.txt", "w") as data:
    for i in range(itemListLength):
        item = driver.execute_script(f"""
        return itemList[{i}]
        """)
        data.write(f"{item[0]}, {item[1]}\n")

driver.quit()

print("Regexing the list of exercices...")
f = "https://learningapps.org/collection.php"
exo = open("scrap_data.txt", "r+").read()

def use_regex():
    pattern = re.findall(r"v=(.{11})", exo)
    return pattern
    
def main():
    m = use_regex()
    print("Starting the requests...")
    for j in m:
        params2 = {
            "u": namex,
            "a": j,
            "c": nameid,
            "t": random.randint(60,200),
        }

        x = requests.post(f, data=params2)
        if x.status_code == 200:
            print(f"Succesfully made {j} for you baby :D")
        else:
            print("Error: " + x.status_code + " | " + x.text)
  

main()