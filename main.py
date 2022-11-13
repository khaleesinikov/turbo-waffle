import requests
from bs4 import BeautifulSoup
import validators


class Spider:
    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.url_list = [starting_url]

    # Pretty print full list, alerting user if it did not reach 100
    def __str__(self):
        full_list = "\n".join(self.url_list)
        return full_list if len(self.url_list) == 100 else full_list + "\nCouldn't reach 100 URLs"

    def scrape_all(self):
        for url in self.url_list:
            if len(self.url_list) == 100:
                break
            self.scrape(url)

    def scrape(self, url):
        try:
            html = requests.get(url)
        # If connection is unsuccessful, skip over current URL
        except requests.exceptions.ConnectionError:
            return
        if html.status_code != 200:
            return
        html.encoding = 'utf-8'
        sp = BeautifulSoup(html.text, 'lxml')

        links = sp.find_all('a')
        for item in links:
            link = item.get('href')
            # Check if href attribute exists and is a valid URL
            if link and validators.url(link):
                if link not in self.url_list:
                    self.url_list.append(link)
                    if len(self.url_list) == 100:
                        return


if __name__ == "__main__":
    spider = Spider(starting_url="https://reddit.com")
    spider.scrape_all()
    print(spider)
