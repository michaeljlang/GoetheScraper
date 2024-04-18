import re
import requests
from bs4 import BeautifulSoup as bs


def remove_leftovers(article_text):

    """
    Removes leftover html code.
    Args:
        article_text: a string containing the text from the article.
    Returns:
        final_text: the string with the remaining html removed.
    """
    replace = [("xyx321window\. ?GenPopupCaption.*?;xyx321}",""),("frageblock.*]]>",""),
               ("function CaptionImage.*;xyx321}","")]
    text = re.sub("\n","xyx321",article_text)
    for old, new in replace:
        text = re.sub(old,new,text)
    final_text = re.sub("xyx321","\n",text)
    return final_text

def check_title(headline,fulltext):

    """
    Check for multiple instances of the headline and select the final option to avoid unwanted banner text.
    Args:
        headline: a string contained in fulltext
        fulltext: a string containing the text (extracted via bs4)
    Returns:
        locations[-1]: the final instance of the headline
    """
    locations = []
    real_headline = "\t"+headline+"\n"
    for hl in re.finditer(re.escape(real_headline),fulltext):
        locations.append(hl.start())
    return locations[-1]


def get_language(soup,url):
    try:
        language = soup.find("span", class_ = "meta-navigation-level-0-button-text current-lang")
        if "de" in language.text.lower():
            lang = "de"
        else:
            lang = "es"
    except AttributeError:
        all_text = soup.get_text()
        if "The page you have selected could not be found" in all_text:
            print("PAGE DOES N0T EXIST:",url)
            lang = None
        else:
            if "/es/es/" in url:
                lang = "es"
            else:
                lang = "de"
    return lang


def reorder(dictionary):
    counter = 1
    final_order = {}
    for k,v in dictionary.items():
        final_id = f"<{str(counter).rjust(3, '0')}>"
        final_order[final_id] = v
        counter += 1
    return final_order
