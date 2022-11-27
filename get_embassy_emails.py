from bs4 import BeautifulSoup
import csv
import re
import sys
from termcolor import colored
import urllib3


def create_foreign_emabssy_email_csv():
    print("\nWe will read through " + colored("travel.state.gov", 'red') + " to get email address of all "+ colored("Foreign Embassies", "green")+" in US.\n\n")
    http = urllib3.PoolManager()

    content_url = "/content/travel/en/consularnotification/ConsularNotificationandAccess"
    dot_html = ".html"

    url = 'https://travel.state.gov/content/travel/en/consularnotification/ConsularNotificationandAccess.html'
    countries = []
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="lxml")

    for link in soup.findAll('a'):
        href_content = link.get('href')
        if href_content is not None:
            if content_url in href_content and href_content not in countries:
                countries.append(href_content)

    url = 'https://travel.state.gov{country}'
    f = open('foreign_embassies_in_us.csv', 'w')
    writer = csv.writer(f)
    no_of_countries_read = 0
    for country in countries:
        response = http.request('GET', url.format(country=country))
        soup = BeautifulSoup(response.data, features="lxml")

        for link in soup.findAll('a'):
            href_content = link.get('href')
            if href_content is not None:
                if "mailto" in href_content:
                    country_name = re.search('{content_url}/(.*){dot_html}'.format(
                        content_url=content_url, dot_html=dot_html), country).group(1)
                    country_row = [country_name, href_content.split("mailto:",1)[1]]
                    writer.writerow(country_row)
                    no_of_countries_read += 1
                    #print(href_content.split("mailto:",1)[1])
                    if no_of_countries_read != 1:
                        sys.stdout.write("\033[F") # Cursor up one line
                        sys.stdout.write("\033[K")
                    print("Loading " + colored(country_name, 'red') + " | Loaded: " + colored(str(no_of_countries_read), 'blue') + " countries")
                    break
    f.close()

if __name__ == "__main__":
    create_foreign_emabssy_email_csv()