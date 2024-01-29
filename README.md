# GoetheScraper

GoetheScraper is designed to retrieve all bilingual text articles from the German-Spanish Kultur magazine, an online publication by the Goethe Institut.

The tool was developed by Michael Lang through the PaCorEs research group at the University of Santiago de Compostela in Galicia, Spain.

GoetheScraper primarily replies on Selenium WebDriver to automatically retrieve the links and BeautifulSoup to process the text.

NOTE: The code requires Google Chrome to carry out the webscraping process, although Selenium also supports other browsers, such as Edge and Firefox, among others. The code must be altered in order to use a browser other than Chrome. 

To run the code, execute the scrape.py file. This can be done from the command line. This will create a new directory, "Goethe", where all files will be saved. 

# Output

GoetheScraper will generate six files:

1) articles_es.txt: A clean text file containing all articles in Spanish with their corresponding id number.
2) articles_es.json:  A dictionary containing  all articles in Spanish, structured as { <article_id> : text }.
3) articles_de.txt: A clean text file containing all articles in German with their corresponding id number.
4) articles_de.json:  A dictionary containing  all articles in German, structured as { <article_id> : text }.
5) metadata.txt: A text file with all available metadata structured as follows:

    Enlace (es): 
    Enlace (de):
    Lengua de origen: 
    Título en español: 
    Título en alemán:
    Autor/a:
    Traducción (es):
    Traducción (de): 
    Fecha: 
  
6) links.txt: A text file containing all the links to the articles in Spanish. The links to the German articles are generated within the code by altering the Spanish url.

The articles_{language}.json files allow for the articles to be easily loaded in Python, while the articles_{language}.txt files are intended to be aligned as is.

At the time of writing, the code will extract approximately 515 links to articles (pages dedicated to videos/interviews are discarded outright), of which around 510 articles will be correctly processed. Issues that may cause an article to be discarded include: the lack of bilingual version, the inability to adequately remove all HTML code, and inconsistencies in HTML structure and labeling. 
