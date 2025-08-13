from bs4 import BeautifulSoup

class LocatorExtractor:
    def extract_locators(self, html_content: str):
        soup = BeautifulSoup(html_content, "html.parser")
        locators = []
        for tag in soup.find_all():
            if tag.has_attr("id"):
                locators.append(("id", tag["id"]))
            elif tag.has_attr("name"):
                locators.append(("name", tag["name"]))
        return locators
