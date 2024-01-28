import requests
import re
import json

from utils import *
from bs4 import BeautifulSoup as bs 

def goethe_scraper(set_of_links):

    """
    Cleans the text extracted from each article
    Args:
        set_of_links: list. all the links to the Spanish articles
    Returns:
        alltexts: dictionary containing all articles (article number : text)
        meta: dictionary containing all metadata (article number : full, unclean metadata)
        titles: dictionary containing all titles (article number : title)
        discard: dictionary containing articles to discard article number : article to discard)
    """

    alltexts = {}
    meta = {}
    titles = {}
    discard = {}

    replacements = [
        ("\t",""),
        ("\n\n*","\n"),
        ("  +"," "),
        ("©.*\n",""),
        ("Foto:.*",""),
        ("\n \n \n \n \n \n \n|\n \n \n|\n \n","\n"),
        ("\n\xa0\n","\n"),
        ("\xa0",""),
        ("\n ","\n")
    ]

    markers = [ 
        "\nReferencias bibliográficas",
        "\nBibliografía\n",
        "\nLiteratur\n",
        "\nLiteraturhinweise",
        "\nLiteratura\n",
        "$(function() {",
        "Información de protección de datos",
        "Informationen zum Datenschutz",
        "Artikel drucken",
        "Imprimir artículo"
    ]


    meta_markers = ["Información de protección de datos",
                    "Informationen zum Datenschutz",
                    "Artikel drucken",
                    "Imprimir artículo"]

    article_id = 1
    for link in set_of_links:

        doc = bs(requests.get(link).text, "html5lib")
        fulltext = doc.get_text()

        #get language
        lang = get_language(doc,link)
        if lang == None:
            discard[article_id] = link
            meta[article_id], alltexts[article_id], titles[article_id]  = {link : "discard"},"discard", "discard"
            article_id+=1
            continue

        # beginning of text
        start_class = doc.find_all('span', class_ = re.compile("spitz.*"))
        title = doc.find("span", class_ = re.compile("hdl.*")).text

        try:
            headline = [item for item in start_class[0]]
            if headline[0] == "Alemania":
                headline = title
                start = fulltext.find(headline + "\n")
            else:
                start = fulltext.find(headline[0] + "\n")
        except:
            headline = title
            start = check_title(headline,fulltext)

        # end of text
        try:
            finish = doc.find("div",class_ = re.compile("box author")).find("a", href = re.compile("mailto:"))
            finish = re.search(re.escape(finish.text),fulltext).span()[0]
        except AttributeError:
            finish = fulltext.find("  Top")

        final = fulltext[start:finish]
        final = re.sub("\|.*\n",'',final)

        # get metadata ======================
        # beginning:
        if "\tAutor" in final:
            metadata = final[final.find("\tAutor"):]
        elif "\nAutor" in final:
            metadata = final[final.find("\nAutor"):]
        elif doc.find("h3", class_ = "box-hdl-h3 autor") != None:
            author = doc.find("h3", class_ = "box-hdl-h3 autor")
            metadata = final[final.find(author.text):]
        else:
            metadata = final

        # end:
        try:
            try:
                end = re.search("Copyright.* \d\d\d\d",metadata).span()[1]+1
                metadata = metadata[:end]
            except AttributeError:
                try:
                    end = re.search("Copyright.*\n",metadata).span()[1]+1
                    metadata = metadata[:end]
                except:  
                    end = doc.find("div",class_ = re.compile("box author")).find("a", href = re.compile("mailto:"))
                    end = re.search(re.escape(end.text),metadata).span()[0]
                    metadata = metadata[:end]
        except AttributeError:
            pass

        for marker in meta_markers:
            if marker in metadata:
                metadata = metadata[:metadata.find(marker)]

        for old, new in replacements:
            final = re.sub(old,new,final)
            metadata = re.sub(old,new,metadata)
        for old, new in replacements:
            final = re.sub(old,new,final)
            metadata = re.sub(old,new,metadata)

        comentarios = re.search(" \n\d* Comentarios \n", metadata)
        if comentarios != None:
            comentarios = comentarios.span()[0]
            metadata = metadata[:comentarios]


        # drop metadata from text
        loc = final.find(metadata)
        if loc > 0:
            final = final[:loc]

        for mark in markers:
            if mark in final:
                final=final[:final.find(mark)]

        comentarios = re.search("\n\d* Comentarios \n", final)
        if comentarios != None:
            comentarios = comentarios.span()[0]
            final=final[:comentarios]

        if final[-1] == "\n":
            final = final.rstrip(final[-1])

        if "window.GenPopupCaption = function() {" in final or "frageblock" in final or "CaptionImageGallery" in final:
            final = remove_leftovers(final)

        if "</div>" in final:
            discard[article_id] = link
            meta[article_id], alltexts[article_id], titles[article_id]  = {link : "discard"},"discard", "discard"
            article_id+=1
            print("Article",article_id,"discarded. Unable to extract only clean text.")
            continue

        meta[article_id], alltexts[article_id], titles[article_id]  = {link : metadata}, final, title
        article_id+=1

    print("Language:", lang,
          "\ntotal texts:",len(alltexts),
          "\ntotal metadata:",len(meta),
          "\ntotal titles:", len(titles))
    print("\n**********************************\n\nlinks discarded:",len(discard))
    print("Discarding", discard,"\n")

    return alltexts, meta, titles, discard