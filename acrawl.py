from bs4 import BeautifulSoup as bs
import requests
from htmlslacker import HTMLSlacker as htmlslacker

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
    forum = bs(page_text, features="lxml")
    print ("Crawling, found %i links" % len(forum.find_all("a")))
    result = {}
    try:
        for link in forum.find_all("a"):
            is_modlink = True
            title = str(link.get('title'))
            href = str(link.get('href'))
            # print(href)
            # print(id)
            for string in START_BLACKLIST:
                if title.startswith(string):
                    is_modlink = False
                else:
                    pass
            if is_modlink:
                id = href.split("/topic/")[1].split("-")[0]
                score = score_mod_title(title, KEYWORDS_LIST)
                # result[title] = {'href':href, 'score':score}
                result[id] = {'title':title, 'href':href, 'score':score}
                print(result)



    except:
        pass
    return result




def crawl_mod(mod_url):

    # '''data-quotedata='{"userid":929465,"username":"AxiosODST","timestamp":1496759058,"contentapp":"forums","contenttype":"forums","contentid":205551,"contentclass":"forums_Topic","contentcommentid":3198756}''''

    page_text = load_page(mod_url)
    comments = bs(page_text, features="lxml")
    topic = comments.find_all('div',{"data-commentapp":"forums"})[0]

    return topic


for url, pgvar in TARGET_WEBPAGES.items():
    output = {}
    for n in range(5):
        if n == 0:
            page_text = load_page(url)
        else:
            page_text = load_page(url + "?" + pgvar + "=" + str(n))
        # print len(page_text)
        # print(crawl_forum(page_text, START_BLACKLIST))
        output.update(crawl_forum(page_text, START_BLACKLIST))

print(output)

for id, mod in output.items():
    if int(mod['score']) > 0:
        print(id, mod)
        topic_lines = crawl_mod(mod["href"]).find_all("p")
        out_md = open(id + ".md", "w")
        for line in topic_lines:
            out_md.writelines(htmlslacker(str(line)).get_output()+'\n')
