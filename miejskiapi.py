import requests
from bs4 import BeautifulSoup


def parse_styling(element):
    for index, item in enumerate(element):
        if item.name == "strong":
            element[index] = f"**{item.string}**"
        elif item.name == "a":
            element[index] = f"__{item.string}__"
        elif item.name == "br":
            element[index] = ""
        else:
            element[index] = item.string

    return "".join(element).strip()


def parse_article(article: BeautifulSoup):
    word = f"**{article.header.string}**"
    try:
        definition = parse_styling(list(article.p.children))
    except:
        definition = None
    try:
        quote = f"*{parse_styling(list(article.blockquote.children))}*"
    except:
        quote = None

    return {"word": word, "definition": definition, "quote": quote}


def get_miejski(query: str):
    if query != "losuj":
        query = "slowo-" + query

    r = requests.get(f"https://www.miejski.pl/{query}")
    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup("article")
    parsed = [parse_article(article) for article in articles]
    return parsed


if __name__ == "__main__":
    from time import sleep

    for i in range(100):
        sleep(1)
        print(get_miejski("losuj"))
