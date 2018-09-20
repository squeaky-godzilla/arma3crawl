from bs4 import BeautifulSoup as bs
import requests

TARGET_WEBPAGES = {
"https://forums.bohemia.net/forums/forum/156-arma-3-addons-mods-complete/":"page"
}

def load_page(url):
    page = requests.get(url)
    return page.text

def score_mod_title(mod_title, keywords):
    score = 0
    for word in str(mod_name).split(' '):
        if word in keywords:
            score += 1
            return score

def crawl_forum(page_text):
    soup = bs(page_text, features="lxml")
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
                score = score_mod_title(title)

    except:
        pass

    return result_list




# def crawl_mod(mod_url):
#     score = page_analytics(topic_url)
#     return score



for url,pgvar in TARGET_WEBPAGES.items():
    for n in range(5):
        page_text = load_page(url + "?" + pgvar + "=" + str(n))
        crawl_forum(page_text)
