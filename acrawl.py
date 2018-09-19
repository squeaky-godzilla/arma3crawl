from bs4 import BeautifulSoup as bs
import requests

TARGET_WEBPAGES = {
"https://forums.bohemia.net/forums/forum/156-arma-3-addons-mods-complete/":"page"
}

def load_page(url):
    page = requests.get(url)
    return page.text

def crawl_forum(page_text):
    soup = bs(page_text)
    result_list = []
    try:
        for link in soup.find_all("a"):
            title = str(link.get('title'))
            href = str(link.get('href'))
            if "topic" in href \
            and not title.startswith("Go to") \
            and not title.endswith("page") \
            and not title == "None":
                # print [title, href]
                result_list.append({"title":title, "href":href, "score":0})
    except:
        pass

    return result_list


for url,pgvar in TARGET_WEBPAGES.items():
    for n in range(5):
        page_text = load_page(url + "?" + pgvar + "=" + str(n))
        crawl_forum(page_text)

def crawl_mods(mod_list):
    for title, href, score in mod_list.items():
        score = page_analytics(topic_url)
