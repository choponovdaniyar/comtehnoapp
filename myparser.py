import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class Parser:
    def headers(self):
        return {
            "user-agent": UserAgent().random
        }
    
    def get_soup(self,url):
        html = requests.get(url, headers=self.headers()).text
        return BeautifulSoup(html,"lxml")

    async def parse_journal(self, url="https://comtehno.kg/electronic-journal/"):
        soup = self.get_soup(url)
        taga = soup.find_all("a", class_="elementor-button-link")
        res = list()
        for tag in taga:
            if "журнал" not in tag.text:
                continue
            txt = tag.text.strip()
            link = tag.attrs["href"]
            res.append(
                f"{txt},{link}"
            )
        with open("data/journal.txt", "w", encoding="utf-8") as f:     
            f.write("\n".join(res))   
                
        