from bs4 import BeautifulSoup


def extract_articles(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    articles = []

    for article in soup.select("article"):

        title_node = (
            article.find(["h1", "h2", "h3"])
        )

        link_node = article.find("a")

        content = article.get_text(
            " ",
            strip=True
        )

        articles.append(
            {
                "title":
                    title_node.get_text(strip=True)
                    if title_node
                    else None,

                "content":
                    content,

                "url":
                    link_node.get("href")
                    if link_node
                    else None,
            }
        )

    return articles