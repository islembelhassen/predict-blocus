from bs4 import BeautifulSoup


def extract_messages(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    messages = []

    blocks = soup.select(
        ".tgme_widget_message_wrap"
    )

    for block in blocks:

        text_node = block.select_one(
            ".tgme_widget_message_text"
        )

        if not text_node:
            continue

        date_node = block.select_one(
            "time"
        )

        link_node = block.select_one(
            ".tgme_widget_message_date"
        )

        messages.append(
            {
                "content": text_node.get_text(
                    " ",
                    strip=True
                ),
                "published_at":
                    date_node["datetime"]
                    if date_node and "datetime" in date_node.attrs
                    else None,
                "url":
                    link_node["href"]
                    if link_node
                    else None,
            }
        )

    return messages