import requests,sys
from bs4 import BeautifulSoup
from pyexcel_ods3 import save_data
from collections import OrderedDict
lot_url = "https://kurser.lth.se/lot/?val=program&lasar=21_22&prog=Pi&forenk=0"
course_url = "https://kurser.lth.se/kursplaner/21_22/"
#page = requests.get(lot_url)
html = ""
for line in sys.stdin:
    html+=line

soup = BeautifulSoup(html, 'html.parser')
titles = soup.find_all("a")
courses = []
for title in titles:
    if "val=kurs&amp" in str(title):
        course_name = str(title).split("kurskod=")[1]
        courses.append(course_name.split("\"")[0])
#print(courses)

String_bar =["Kurskod", "Kursnamn","HP", "Nivå","År", "Specialiseringar"]
Grundblock = [String_bar]
Other_courses = [String_bar]
course_set = set()
print("FMAN61" in courses)
for key,course in enumerate(courses):
    if course in course_set:
        continue
    page = requests.get(course_url+course)
    course_info = soup = BeautifulSoup(page.content, 'html.parser')
    name_part =  str(course_info.find('h1'))
    other_part = str(course_info.find('h2'))
    if "högskolepoäng" not in str(other_part):
        print(course)
        continue
    course_set.add(course)
    spec_part = str(course_info.find_all('p',limit = 2)[1])
    name = name_part.split(">")[1].split("<br/")[0]
    hp = other_part.split(", ")[1].split(" hög")[0]
    hp = hp.replace(",",".")
    level = other_part.split("äng, ")[1].split(" (")[0]
    year = 4
    progs, specs,optional = [],[], []
    if "bligatorisk" in spec_part:
        progs = spec_part.split("bligatorisk för: </span>")[1].split("<br")[0].split(", ")
    if "Valfri" in spec_part:
        optional= spec_part.split("Valfri för: </span>")[1].split("<br")[0].split(", ")
    mandatory = False
    for prog in progs+optional:
        if prog in progs:
            mandatory = True
        if prog[0:2] == "Pi":
            year = int(prog[2])
            if len(prog)>3:
                specs.append(prog[4:])
    info = [course, name, float(hp), level, year, ", ".join(specs)]
    Other_courses.append(info)
    if year<=3 and mandatory:
        Grundblock.append(info)
    #print(info)

data = OrderedDict()
data.update({"Sheet1":Grundblock})
data.update({"Sheet2":Other_courses})
save_data("Course_sheet.ods", data)
