import re 
import spacy


nlp = spacy.load('es_core_news_sm')
nlp_de = spacy.load("de_core_news_sm")

def get_meta(meta, meta_de, titles, titles_de):

	""" 
	Cleans the metadata extracted from each article and saves it to txt file
	Args:
	    set_of_links: list. all the links to the Spanish articles		
	"""

	final_meta = {}

	# Process German metadata
	authors_de = {}
	original_lang_de = {}

	for key,values in meta_de.items():
	    for k,v in values.items():

	    	# German author
	        aut = re.search("Autor.*\n",v)
	        if aut != None:
	            v = v[aut.span()[1]:]
	        tokens = nlp_de(v)
	        if tokens.ents[0].label_ == "PER":
	            author = tokens.ents[0]
	        else:
	            author = "--"
	        authors_de[key] = author
	        
	        # German translator
	        tokes = v.split()
	        if "Übersetzung:" in tokes:
	            original_lang = "español"
	            translator = []
	            trans_loc = tokes.index("Übersetzung:")
	            while True:
	                for word in tokes[trans_loc+1:]:
	                    if word == "Copyright:":
	                        break
	                    else:
	                        translator.append(word)
	                break

	            translator = " ".join(translator)
	        else:
	            translator = "--"
	            original_lang = "alemán"

	        original_lang_de[key] = [original_lang,translator]

	# Process metadata from Spanish version
	for key,values in meta.items():
	    for k,v in values.items():

	        v2 = re.sub("^Autor[ea]?s?\n|^autor[ea]?s?\n|^Autor[ea]?s?","",v)
	        v2 = re.sub("Foto \(Detail\): privat|Photo \(détail\) : privée","",v2)
	        v2 = re.sub("Nací"," nací",v2)
	        v2 = re.sub("Tengo"," tengo",v2)
	        v2 = re.sub("Soy"," soy",v2)
	        v2 = re.sub("Sobre el autor","",v2)
	        v2 = re.sub("\(\w*\)","",v2)
	        tokes = v2.split()

	        # Spanish author ======================================================
	        author =[]
	        while True:
	            for word in tokes:
	                    if word[0].isupper():
	                        author.append(word)
	                    elif word == "y" or word == "von":
	                        author.append(word)
	                    elif len(word) > 1 and word[1] == ".":
	                            author.append(word)
	                    else:
	                        break
	            break
	        try:
	            if author[-1] == "y":
	                author.pop()
	        except:
	            pass

	        if len(author) <= 1:
	            author = "--"
	        else:
	            author = " ".join(author)
	        if author[-1] == ",":
	            author = author.strip(author[-1])

	        for art,aut in authors_de.items():
	            if art == key:
	                if author == "--":
	                    author = str(aut)

	        # Spanish translator ===================================================
	                
	        trans_de = original_lang_de[key]
	        translator_de = trans_de[1]

	        if "Traducción:" in tokes:
	            original_lang = "alemán"
	            translator = []
	            trad_loc = tokes.index("Traducción:")
	            while True:
	                for word in tokes[trad_loc+1:]:
	                    if word == "Copyright:":
	                        break
	                    else:
	                        translator.append(word)
	                break

	            translator = " ".join(translator)
	        else:
	            translator = "--"
	            original_lang = "español"


	        if original_lang != trans_de[0]:
	            original_lang = "--"

	        # time of publication ========================================
	        months = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre",
	                 "noviembre","diciembre"]

	        if tokes[-2] in months:
	            date = " ".join(tokes[-2:])
	        elif tokes[-1].isnumeric():
	            date = " ".join(tokes[-1])
	        else:
	            date = "--"

	        # titles ======================================================  
	        title_es = titles[key]
	        title_de = titles_de[key]
	        link_de = re.sub("es/kul","de/kul",k)

	        final_meta[key] = [k,link_de,original_lang,title_es,title_de,author,translator,translator_de,date]

	with open("metadata.txt", "w") as f:
	    for k,v in final_meta.items():
	        f.write("Artículo: "+k+"\n"+
	            "Enlace (es): "+v[0]+"\n"+
	            "Enlace (de): "+v[1]+"\n"+
	            "Lengua de origen: "+v[2]+"\n"+
	            "Título en español: "+v[3]+"\n"+
	            "Título en alemán: "+v[4] +"\n"+
	            "Autor/a: "+v[5]+"\n"+
	            "Traducción (es): "+v[6]+"\n"+
	            "Traducción (de): "+v[7]+"\n"+
	            "Fecha: "+v[8]+"\n\n")