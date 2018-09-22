from bs4 import BeautifulSoup as bs
import requests
# import hashtools as ht
import hashlib

TARGET_WEBPAGES = {
"https://forums.bohemia.net/forums/forum/156-arma-3-addons-mods-complete/":"page"
}

KEYWORDS_LIST = [

    "ai",
    "immersion",
    "command"

]

START_BLACKLIST = [

    'Next page',
    'Last page',
    'Find other',
    'Go to',
    'All Content',
    'None',
    'Go to the sign in page',
    'See who follows this',
    'Previous page',
    'First page',
    'Home',
    'Addon & Mod Compilation List'

]

END_BLACKLIST = [

]


def load_page(url):
    page = requests.get(url)
    return page.text

def score_mod_title(mod_title, keywords):
    score = 0
    mod_title = mod_title.lower()
    for word in str(mod_title).split(' '):
        if word in keywords:
            score += 1
    return score


def crawl_forum(page_text, BLACKLIST):
    soup = bs(page_text, features="lxml")
    result = {}
    try:
        for link in soup.find_all("a"):
            is_modlink = True
            title = str(link.get('title'))
            href = str(link.get('href'))
            for string in START_BLACKLIST:
                if title.startswith(string):
                    is_modlink = False
                else:
                    pass
            if is_modlink:
                score = score_mod_title(title, KEYWORDS_LIST)
                # print {"title":title, "href":href, "score":score}
                # result_dict.update({"title":title, "href":href, "score":score})
                result[title] = {'href':href, 'score':score}


    except:
        pass
    return result




# def crawl_mod(mod_url):
#     score = page_analytics(topic_url)
#     return score



for url, pgvar in TARGET_WEBPAGES.items():
    output = {}
    for n in range(5):
        page_text = load_page(url + "?" + pgvar + "=" + str(n))
        # print len(page_text)
        print(crawl_forum(page_text, START_BLACKLIST))
        output.update(crawl_forum(page_text, START_BLACKLIST))

print(output)

for mod, attrs in output.items():
    if int(attrs['score']) > 0:
        print(mod, attrs)


import pdb; pdb.set_trace()
