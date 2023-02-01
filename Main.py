import urllib.request
from bs4 import BeautifulSoup

class Main:

    def __init__(self, url):
        self.url = url
        self.soup = self._getSoup()

    def _getSoup(self):
        fp = urllib.request.urlopen(self.url)
        mybytes = fp.read()
        fp.close()
        return BeautifulSoup(mybytes.decode("utf8"), "html.parser")

    def run(self):
        result = []
        matchups = self.soup.find_all("div", {"class": "lineup is-nba"})
        for index, matchup in enumerate(matchups):
            awayTeam = matchup.find("a", {"class": "lineup__mteam is-visit white"})
            homeTeam = matchup.find("a", {"class": "lineup__mteam is-home white"})
            result.append({
                "away": {
                    "team": awayTeam.text.split(None, 1)[0],
                    "likely": [item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-visit"}).find_all("li", {"class": "lineup__player is-pct-play-100"})],
                    "unlikely": [item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-visit"}).find_all("li", {"class": "lineup__player is-pct-play-0 has-injury-status"})], 
                },
                "home": {
                    "team": homeTeam.text.split(None, 1)[0],
                    "likely": [item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-home"}).find_all("li", {"class": "lineup__player is-pct-play-100"})],
                    "unlikely": [item.a['title'] for item in matchup.find("ul", {"class": "lineup__list is-home"}).find_all("li", {"class": "lineup__player is-pct-play-0 has-injury-status"})], 
                }
            })

        for row in result:
            print(row)

        return


if __name__ == "__main__":
    Main("https://www.rotowire.com/basketball/nba-lineups.php").run()
