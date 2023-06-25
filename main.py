from crawler.golden_house import GoldenHouse
from models.htmlParser import HTMLParser


if __name__ == "__main__":
    # TODO: remove
    crawler = GoldenHouse("https://tw.hjwzw.com/Book/Chapter/1642")
    book = crawler.get_book(HTMLParser.LXML)
    chapters = crawler.get_content(
        "https://tw.hjwzw.com/Book/Read/1642,530186", HTMLParser.HTML5LIB
    )
