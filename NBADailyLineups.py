import urllib.request
from bs4 import BeautifulSoup

class NBADailyLineups:

    data = []

    def __init__(self, url):
        self.url = url
        self.soup = self._getSoup()

    def __str__(self):
        result = ""
        for index, matchup in enumerate(self.data):
            result += "\n\nMatchup {}\n".format(index + 1)
            for team in matchup:
                result += "\n\n{} team: {}\n{}\n".format(team, matchup[team]["team"], '-' * len("team: " + team + matchup[team]["team"]))
                result += "\nConfirmed Playing\n{}\n".format('-' * len("Confirmed Playing"))
                for player in matchup[team]["confirmed"]:
                    result += player + "\n"
                result += "\nGame Time Decision\n{}\n".format('-' * len("Game Time Decision"))
                for player in matchup[team]["gtd"]:
                    result += player + "\n"
                result += "\nConfirmed Out\n{}\n".format('-' * len("Confirmed Out"))
                for player in matchup[team]["out"]:
                    result += player + "\n"
        return result

    def _getSoup(self):
        fp = urllib.request.urlopen(self.url)
        mybytes = fp.read()
        fp.close()
        return BeautifulSoup(mybytes.decode("utf8"), "html.parser")

    def getDict(self):
        self.data = []
        for matchup in self.soup.find_all("div", {"class": "lineup is-nba"}):
            self.data.append({
                "away": {
                    "team": matchup.find("a", {"class": "lineup__mteam is-visit white"}).text.split(None, 1)[0],
                    "confirmed": set(item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-visit"}).find_all("li", {"title": "Very Likely To Play"})),
                    "gtd": set(item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-visit"}).find_all("li", {"title": ["Toss Up To Play", "Likely To Play"]})),
                    "out": set(item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-visit"}).find_all("li", {"title": "Very Unlikely To Play"})), 
                },
                "home": {
                    "team": matchup.find("a", {"class": "lineup__mteam is-home white"}).text.split(None, 1)[0],
                    "confirmed": set(item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-home"}).find_all("li", {"title": ["Very Likely To Play", "Likely To Play"]})),
                    "gtd": set(item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-home"}).find_all("li", {"title": "Toss Up To Play"})),
                    "out": set(item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-home"}).find_all("li", {"title": "Very Unlikely To Play"})), 
                }
            })

if __name__ == "__main__":
    NBADailyLineups = NBADailyLineups("https://www.rotowire.com/basketball/nba-lineups.php")
    NBADailyLineups.getDict()
    print(NBADailyLineups)
