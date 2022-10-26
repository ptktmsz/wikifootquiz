import requests
import statistics
import bs4
import re
import pandas as pd
import datetime

headers = {
    "User-Agent": "ptktmsz@gmail.com"
}

class Player:
    def __init__(self, name):
        self.name = name
        self.url = self.get_wiki_url()
        self.career = WikiScraper(self).get_career()
        self.views = self.get_page_views()
        self.position = WikiScraper(self).get_position()
        self.pob = WikiScraper(self).get_pob()


    def get_page_views(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        start_date_preformat = yesterday - datetime.timedelta(days=1825)
        start_date = start_date_preformat.strftime("%Y%m%d")
        end_date = yesterday.strftime("%Y%m%d")
        sliced_url = self.url.split("/")
        name = sliced_url[len(sliced_url) - 1]
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{name}/monthly/{start_date}/{end_date}"
        response = requests.get(url=url, headers=headers)
        return round(statistics.mean([month["views"] for month in response.json()["items"]]))


    def get_wiki_url(self):
        if self.name == "Álvaro González":
            return "https://en.wikipedia.org/wiki/%C3%81lvaro_Gonz%C3%A1lez_(footballer,_born_1990)"
        if self.name == "Brandão":
            return "https://en.wikipedia.org/wiki/Brand%C3%A3o_(footballer,_born_1980)"
        if self.name == "Christian Giménez":
            return "https://en.wikipedia.org/wiki/Christian_Gim%C3%A9nez_(footballer,_born_1974)"
        if self.name == "Gerson":
            return "https://en.wikipedia.org/wiki/Gerson_(footballer,_born_1997)"
        if self.name == "Hilton":
            return "https://en.wikipedia.org/wiki/Vitorino_Hilton"
        if self.name == "Koke":
            return "https://en.wikipedia.org/wiki/Koke_(footballer,_born_1983)"
        if self.name == "Lucas Mendes":
            return "https://en.wikipedia.org/wiki/Lucas_Mendes_(footballer,_born_1990)"
        if self.name == "Lucas Silva":
            return "https://en.wikipedia.org/wiki/Lucas_Silva_(footballer,_born_1993)"
        if self.name == "Luis Henrique":
            return "https://en.wikipedia.org/wiki/Luis_Henrique_(footballer,_born_2001)"
        if self.name == "Luis Suárez":
            return "https://en.wikipedia.org/wiki/Luis_Su%C3%A1rez_(footballer,_born_1997)"
        if self.name == "Mamadou Samassa":
            return "https://en.wikipedia.org/wiki/Mamadou_Samassa_(footballer,_born_1986)"
        if self.name == "Mido":
            return "https://en.wikipedia.org/wiki/Mido_(footballer)"
        if self.name == "Rolando":
            return "https://en.wikipedia.org/wiki/Rolando_(footballer)"
        if self.name == "Steven Fletcher":
            return "https://en.wikipedia.org/wiki/Steven_Fletcher_(footballer)"
        if self.name == "Maxime López":
            return "https://en.wikipedia.org/wiki/Maxime_Lopez"
        if self.name == "André Luis":
            return "https://en.wikipedia.org/wiki/Andr%C3%A9_Lu%C3%ADs_(footballer,_born_1979)"
        if self.name == "Andrés Mendoza":
            return "https://en.wikipedia.org/wiki/Andr%C3%A9s_Mendoza_(Peruvian_footballer)"
        if self.name == "Delfim":
            return "https://en.wikipedia.org/wiki/Delfim_Teixeira"
        if self.name == "Elamine Erbate":
            return "https://en.wikipedia.org/wiki/Amin_Erbati"
        if self.name == "Mohamed Dennoun":
            return "https://en.wikipedia.org/wiki/Mohamed_Amine_Dennoun"
        if self.name == "Fernandão":
            return "https://en.wikipedia.org/wiki/Fernand%C3%A3o_(footballer,_born_1978)"
        if self.name == "Manuel dos Santos":
            return "https://en.wikipedia.org/wiki/Manuel_dos_Santos_(footballer)"
        if self.name == "Alberto Rivera":
            return "https://en.wikipedia.org/wiki/Alberto_Rivera_(footballer)"
        if self.name == "André Luiz":
            return "https://en.wikipedia.org/wiki/Andr%C3%A9_Luiz_(footballer,_born_1974)"
        if self.name == "Dill":
            return "https://en.wikipedia.org/wiki/Dill_(footballer)"
        if self.name == "Dimas":
            return "https://en.wikipedia.org/wiki/Dimas_(footballer)"
        if self.name == "Edson":
            return "https://en.wikipedia.org/wiki/Edson_(footballer,_born_1977)"
        if self.name == "Jérôme Leroy":
            return "https://en.wikipedia.org/wiki/J%C3%A9r%C3%B4me_Leroy_(footballer)"
        if self.name == "Richard Martini":
            return "https://en.wikipedia.org/wiki/Richard_Martini_(footballer)"
        if self.name == "Nenad Bjeković":
            return "https://en.wikipedia.org/wiki/Nenad_Bjekovi%C4%87_(footballer,_born_1974)"
        else:
            underscored_name = self.name.replace(" ", "_")
            return "https://en.wikipedia.org/wiki/" + underscored_name

class WikiScraper:
    def __init__(self, player):
        self.player = player
        self.url = player.url
        self.rows = self.get_infobox()
        self.first_row = self.get_first_row()
        self.last_row = self.get_last_row()

    def check4d(s) -> bool:
        """
        Takes string as an input and using regex looks for a 4 digit number.
        Return True if finds one and False if it doesn't.
        """
        if re.search(r"\d{4}", s) is None:
            return False
        else:
            return True

    def get_infobox(self):
        if self.player.name == "Eric Cantona":
            response = requests.get(self.url)
            soup = bs4.BeautifulSoup(response.text, features="html.parser")
            infobox = soup.find("table", {"class": "infobox biography vcard"})
            infobox_football = infobox.find("table", {"class": "infobox-subbox infobox-3cols-child vcard"})
            return infobox_football.find_all("tr")
        response = requests.get(self.url)
        soup = bs4.BeautifulSoup(response.text, features="html.parser")
        infobox = soup.find("table", {"class": "infobox vcard"})
        rows = infobox.find_all("tr")
        return rows

    def get_first_row(self):
        for row in self.rows:
             thcell = row.find("th")
             if thcell:
                 thcell = thcell.text.strip()
                 if thcell == "Senior career*":
                     return self.rows.index(row) + 2

    def get_last_row(self):
        for row in self.rows[self.first_row:]:
             th_cell = row.find("th")
             try:
                 cell = th_cell.text
                 cell = cell.strip()
                 if WikiScraper.check4d(cell) == False:
                     return self.rows.index(row) - 1
             except AttributeError:
                 return self.rows.index(row) - 1

    def get_career(self):
        if self.player.name == "Daniel Bravo":
            self.first_row = 7
            self.last_row = 13
        workinglist = []
        for row in self.rows[self.first_row:self.last_row + 1]:
            entrydict = {}
            th_cell = row.find("th")
            # add entry about years spent in club
            entrydict["Years"] = th_cell.text.strip()
            td_cells = row.find_all("td")
            # add entry about the club
            entrydict["Team"] = td_cells[0].text.strip()
            # add entry about apps for club
            entrydict["Apps"] = td_cells[1].text.strip()
            # add entry about goals for club
            entrydict["Goals"] = td_cells[2].text.strip()
            # append career list to player dict
            workinglist.append(entrydict)
        df = pd.DataFrame(workinglist)
        return df


    def get_position(self):
        for row in self.rows:
            thcell = row.find("th")
            if thcell:
                if thcell.text.strip() == "Position(s)":
                    position = row.find("td")
                    position = position.text.strip()
                    position = position.replace("\n", ", ")
                    position = re.sub(r"\[.*?\]", "", position)
                    return position

    def get_pob(self):
        if self.player.name == "George Weah":
            return "Monrovia, Liberia"
        if self.player.name == "Eric Cantona":
            return "Marseille, France"
        if self.player.name == "Dragan Stojković":
            return "Niš, SR Serbia, Yugoslavia"
        for row in self.rows:
            thcell = row.find("th")
            if thcell:
                if thcell.text.strip() == "Place of birth":
                    pob = row.find("td")
                    pob = pob.text.strip()
                    pob = pob.replace("\n", ", ")
                    pob = re.sub(r"\[.*?\]", "", pob)
                    return pob
