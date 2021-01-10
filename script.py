#  Modules used for the Web Scraper
    """
    This list comprises of a short description fo each module and usage.

    1. **Requests** - The requests module allows you to send HTTP requests using Python.
   
    The HTTP request returns a Response Object with all the response data (content, encoding, status, etc).
    
    2. **JSON** - If you have a Python object, you can convert it into a JSON string by using the json.load() method(line148).
    
    3. **YAML** - YAML is a data serialization format designed for human readability and interaction with scripting languages.
    
    4. **BeautifulSoup4** - Beautiful Soup is a Python library for pulling data out of HTML and XML files.
    
    5. **Console** - package that makes it easy to generate the inline codes used to display colors and character styles in ANSI-compatible terminals and emulators.
    
    6. **Table** - Python interface to the Casacore tables module. A casacore table is similar to a relational data base table with the extension that table cells can contain n-dimensional arrays.
    
    7. **Yaspin** - Yaspin provides a full-featured terminal spinner to show the progress during long-hanging operations.
    """
    
    
import requests
import json
import yaml
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import time
from yaspin import yaspin

# The URL to send requests to using the requests module
language = "python"
URL = "https://summerofcode.withgoogle.com/organizations/"
organization_list = []

# The Class that is responsible for the data management.
'''
1. **Self** - The self is used to represent the instance of the class. With this keyword, you can access the attributes and methods of the class in python.

2. **Name** - argument to store the name of the organization.

3. **IRC** - store the url of the IRC channel.

4. **org_page** - Store the class page.

5. **tech_stack** - store the languages used.
'''
class Organization:
    def __init__(self, name, irc, org_page, tech_stack, count):
        self.name = name
        self.irc = irc
        self.org_page = org_page
        self.tech_stack = tech_stack
        self.count = count
# Count is used to find the number of times the org has been found in the URL.
    def __str__(self):
        return self.name + "count= " + str(self.count)

    def __eq__(self, other):
        return self.count == other.count

    def __lt__(self, other):
        return self.count < other.count

#Filter the Organiation as mentioned by the user. Search is done as well.
def language_filter(tech_stack_list):
    for tech_stack in tech_stack_list:
        if language in tech_stack:
            return True
    return False

#Check the frequency of the organization's participation.
'''
This is the central module to manage the data from the URL.
'''
def check_previous():
    for year in range(2016, 2021):
        archive_url = (
            "https://summerofcode.withgoogle.com/archive/"
            + str(year)
            + "/organizations/"
        )
#Send the HTTPS request to the page to retrive infomation.
        response = requests.get(archive_url)
        soup = BeautifulSoup(response.content, "html.parser")
        orgs = soup.find_all("li", {"class": "organization-card__container"})
#Find the number of occurences from 2016 to 2020.
        for org in orgs:
            name = org["aria-label"]
            for organization in organization_list:
                if organization.name.strip() == name.strip():
                    organization.count += 1
                    # link = org.find("a",{"class":"organization-card__link"})["href"].split('/')[-2]
                    # print(archive_url + str(link))

#Definition responsible for holding all the infomation.
'''
1. **Table** is imported from the table module.
2. 6 Columns,each for a characteristic.
3. for organization in sorted(organization_list, reverse=True): is used to find the tech stack.
4.  x = 1
    while x != -1: is responsible to check for indexing the array and print details of the desired orgs.
'''

def print_list():
    table = Table(title="GSoC orgs")
    table.add_column("S.No", justify="right", style="cyan")
    table.add_column("Org-name", style="magenta")
    table.add_column("Count", style="white")
    table.add_column("IRC", style="red", width=20)
    table.add_column("Org Link", style="blue", width=20)
    table.add_column("Tech stack", justify="right", style="green")
    index = 1
    for organization in sorted(organization_list, reverse=True):
        tech = ""
        for t in organization.tech_stack:
            tech = tech + " " + t
        table.add_row(
            str(index),
            str(organization.name),
            str(organization.count),
            str(organization.irc),
            str(organization.org_page),
            str(tech),
        )
        index += 1
    Console().print(table)
    x = 1
    while x != -1:

        x = int(input("Enter the index no. for getting complete links(-1 to quit): "))
        if x == -1:
            continue
        org_x = sorted(organization_list, reverse=True)[x - 1]
        try:
            print("Name: " + org_x.name)
            print("IRC: " + org_x.irc)
            print("Organisation Link: " + org_x.org_page)
            print("Tech Stack: " + (" ").join(org_x.tech_stack))
            print("Count: " + str(org_x.count))
            print("===========================================\n")
        except:
            print("Organisation is missing some value. Kindly check on GSoc Website")

#To add HTTP headers to a request, simply pass in a dict to the headers parameter.

headers = {
    "authority": "summerofcode.withgoogle.com",
    "accept": "application/json, text/plain, */*",
    "x-content-type-options": "nosniff",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://summerofcode.withgoogle.com/organizations/",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
}
page_no = 1
org_index = 1
language = str(input("Enter the language you want to filter out: "))

try:
#Yaspin is used to produce the spinning moment on the CLI.
'''
With yaspin is used to index the Yaspin module.

as spinner is the function used to show the spinning animation.
'''

    with yaspin(text="Loading current orgs", color="yellow") as spinner:
        while True:
            params = (
                ("page", str(page_no)),
                ("page_size", "48"),
            )
            page_no += 1

            response = requests.get(
                "https://summerofcode.withgoogle.com/api/program/current/organization/",
                headers=headers,
                params=params,
            )
#Using the JSON module along with YAML,we get access to the data extracted from year_wise.py(line 70 onwards)
'''
1. We can parse the above JSON string using json.loads() method from the json module. The result is a Python dictionary.
2. Using json.dumps() we can convert Python Objects to JSON.
3. def json() - Returns the json-encoded content of a response, if any.
4. yaml.safe_load() should be used in future releases,as yaml.load is depreciated
                    
'''
            json_data = yaml.load(json.dumps(response.json()), yaml.Loader)

            for index in range(len(json_data["results"])):
                if language_filter(json_data["results"][index]["technology_tags"]):

                    name = json_data["results"][index]["name"]
                    tech_stack = json_data["results"][index]["technology_tags"]
                    irc = json_data["results"][index]["irc_channel"]
                    org_page = URL + str(json_data["results"][index]["id"])
                    count = 1
                    current_org = Organization(name, irc, org_page, tech_stack, count)
                    organization_list.append(current_org)

            if json_data["results"] == []:
                break

    spinner.ok("✅ ")
    with yaspin(text="Counting previous year selection", color="yellow") as spinner:
        check_previous()
    spinner.ok("✅ ")
    print_list()

except Exception as e:
    print(e)

finally:

    print("Script ran successfully!")

    quit()
