import requests
from bs4 import BeautifulSoup
import csv


def web_search(urls):
    """
    Search for urls from webpage of SIGGRAPH
    :param urls: url of the website
    """
    # Use beautifulSoup to grab the tags, first with the article tag (to avoid all the links from above the
    # article section)
    grab = requests.get(urls)
    soup = BeautifulSoup(grab.text, 'html.parser')
    div = soup.find('article')

    # Prepare header for csv file
    header = ['Title', 'Link', 'Category']

    # Open csv file, and find the "a" and "h3" tag where resides the titles and links
    # When the link is not there (None), we have the titles, otherwise all the sections have links
    with open('links.csv', 'w', encoding = 'UTF8', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        category = ''
        for link in div.find_all(["a", "h3"]):
            title = link.get_text()
            link = link.get('href')
            if link == None:
                category = title
            else:
                if 'http' in link:
                    if category == '':
                        pass
                    else:
                        writer.writerow([title, link, category])
    f.close()


if __name__ == '__main__':
    web_search('https://blog.selfshadow.com/')
