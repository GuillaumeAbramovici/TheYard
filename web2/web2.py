import requests
from bs4 import BeautifulSoup
import csv

# Header used to access the website
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}


def web_search(urls):
    """
    Search for urls from webpage of SIGGRAPH
    :param urls: url of the website
    """

    # Use beautifulSoup to grab the tags, first with the dt tags where the images are
    grab = requests.get(urls, headers=headers)
    soup = BeautifulSoup(grab.text, 'html.parser')
    div = soup.find_all('dt')

    # Prepare header for csv file
    header = ['Title', 'Link']

    with open('links2.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        # Check in the "a" tag of the "dt" tags to check for the name "Source Code" and only select those ones, then
        # extract the link and write it to csv
        for link in div:
            for image in link.find_all('a'):
                if 'Source Code' in str(image):
                    titles = link.get_text()
                    source_link = image.get('href')
                    writer.writerow([titles, source_link])

    f.close()


if __name__ == '__main__':
    web_search('http://kesen.realtimerendering.com/sig2021.html')
