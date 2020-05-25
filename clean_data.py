import os
import re
import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Tag

def get_articles(entries):    
    return [os.path.join(entries, fol, "index.html") 
            for fol in os.listdir(entries)]

def get_topic(x):
    path, fil = os.path.split(x)
    _, fol = os.path.split(path)
    return fol 

def get_soup(filename):
    with open(filename, 'r') as f:
        return BeautifulSoup(f, 'html.parser')

def get_preamble(soup):
    return soup.find_all("div", id="preamble")

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
            if nextNode.name == "h2":
                break
            nextNode = remove_tags(nextNode)
            text.append(nextNode.get_text().strip().replace("\n", " "))
    return remove_citations(" ".join(text).strip())

def get_body(soup):
    body = soup.find("div", id="main-text")
    sections = {}
    for header in body.find_all('h2'):
        title = header.text.split(".")[-1].strip()
        sections[title] = get_text(header)
    return sections

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

def dump_text(filename):
    articles = get_articles(filename)

def clean_data(entries):
    df = pd.DataFrame({"filenames": get_articles(entries)})
    df['topic'] = df['filenames'].apply(get_topic)
    print(get_body(get_soup(df['filenames'][0]))["Logic"])
    #print(get_body(get_soup(df['filenames'][0]))["Life"])



if __name__ == "__main__":
    clean_data("plato-data/entries")
