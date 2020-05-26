import os
import re
import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Tag

# Get list of every article html path
def get_articles(entries):    
    return [os.path.join(entries, fol, "index.html") 
            for fol in os.listdir(entries)]

def get_ai_articles():
    return ["plato-data/entries/reasoning-automated/index.html",
            "plato-data/entries/formal-belief/index.html",
            "plato-data/entries/chinese-room/index.html",
            "plato-data/entries/connectionism/index.html",
            "plato-data/entries/reasoning-defeasible/index.html",
            "plato-data/entries/ethics-ai/index.html",
            "plato-data/entries/frame-problem/index.html",
            "plato-data/entries/logic-ai/index.html",
            "plato-data/entries/turing-test/index.html"]

# Get the name of the topic for the given article
def get_topic(x):
    path, fil = os.path.split(x)
    _, fol = os.path.split(path)
    return fol 

# Open the HTML and return a soup object
def get_soup(filename):
    with open(filename, 'r') as f:
        return BeautifulSoup(f, 'html.parser')

# Pull the introduction from the soup object
def get_preamble(soup):
    return soup.find_all("div", id="preamble")

# Get the table of contents
def get_toc(soup):
    return soup.find_all("div", id="toc")

def remove_citations(text):
    return re.sub(r"\(.*[0-9]+\)", "", text)

def remove_tags(node):
    for r in node:
        if (r.string is None):
            r.string = ' '
    return node

def get_text(header):
    text = []
    nextNode = header
    while True:
        nextNode = nextNode.nextSibling
        if nextNode is None:
            break
        if isinstance(nextNode, NavigableString):
            text.append(nextNode.strip())
        if isinstance(nextNode, Tag):
            if (nextNode.name == "h2" or  
                nextNode.name == "h3" or 
                nextNode.name == "h4" or 
                nextNode.name == "h5" or 
                nextNode.name == "h6"):
                break
            nextNode = remove_tags(nextNode)
            text.append(nextNode.get_text().strip().replace("\n", " "))
    return " ".join(text).strip()

def get_body(soup):
    body = soup.find("div", id="main-text")
    indicies = []
    titles = []
    texts = []
    for header in body.find_all(re.compile('^h[1-6]$')):
        tokens = header.text.strip().split()
        indicies.append(tokens[0].split("."))
        titles.append(" ".join(tokens[1:]))
        texts.append(get_text(header))
    return texts
    build_dict(indices, titles, texts)

def build_dict(indices, titles, texts):
    for i in range(len(titles)):
        print(indices[i], titles[i], texts[i])

def get_bibliography(soup):
    bib = soup.find("div", id="bibliography")
    entries = []
    for node in bib.find_all("li"):
        node = remove_tags(node)
        entries.append(node.get_text().replace("\n", " "))
    return entries

def is_citation(bib, text, threshold=2):
    count = 0
    for word in text.split():
        if word in bib:
            count += 1
        if count >= threshold:
            return True

def get_related(soup):
    return soup.find("div", id="related-entries")


def get_some_text():
    articles = get_ai_articles()
    soup = [get_soup(a) for a in articles]
    texts = [get_body(s) for s in soup]
    return texts

def clean_data(entries):
    #df = pd.DataFrame({"filenames": get_articles(entries)})
    #df['topic'] = df['filenames'].apply(get_topic)
    soup = get_soup(get_ai_articles()[0])
    get_body(soup)
    #print(get_body(get_soup(df['filenames'][0])).keys())
    #print(get_body(get_soup(df['filenames'][0]))["Life"])


# Use bert to determine what passage 


if __name__ == "__main__":
    print(get_some_text())
