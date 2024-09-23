# %%
"""THIS FILE IS USED TO PARSE AUTHOR, TITLE, JOURNAL INFORMATION FROM XML FILES GENERATED USING GROBID XML EXPORTS"""

import os, re, copy, json, pprint, argparse, warnings
import pandas as pd
from stop_words import get_stop_words
import warnings 
from pprint import pprint
from pathlib import Path
import xmltojson
from collections import Counter
warnings.filterwarnings('ignore')



# %% [markdown]
# f'@article{c}'

# %%
def cited_titles(detailedFiles):
    """Extracts the cited titles, author from xml"""
    ddetailedFiles =detailedFiles
    detailedFiles= detailedFiles['TEI']['text']['back']['div']
    if isinstance(detailedFiles, list):
        for item in detailedFiles:
            try: 
                if 'listBibl' in list(item.keys()):
                    cited_works= item.get('listBibl').get('biblStruct')
                    cited_works=[i for i in cited_works]
                    jj = []
                    for sitem in cited_works:
                        c_work={}
                        try: 
                            sitem.pop('@xml:id')
                            sitem.pop('@coords')
                            cited_title= sitem.get('analytic').get('title').get('#text')
                            cited_journal = sitem.get('monogr').get('title').get('#text')
                            cited_year = sitem.get('monogr').get('imprint').get('date').get('#text')
                            c_work['cited_title']=cited_title
                            c_work['cited_journal']=cited_journal
                            c_work['cited_year']=cited_year
                            for stitle in sitem['analytic']['author']:
                                fname= stitle.get('persName').get('forename')
                                if  isinstance(fname, list):
                                    flname=[i['#text'] for i in fname]
                                    lname= stitle['persName'].get('surname')
                                    flname= flname + [lname]
                                    flname= ' '.join(flname)
                                    c_work['author']=flname
                                    jj.append(c_work)
                                else:
                                    fname= stitle.get('persName').get('forename').get('#text')
                                    lname= stitle['persName'].get('surname')
                                    flname= fname +' '+ lname
                                    c_work['author']=flname
                                    jj.append(c_work)
                        except Exception:
                            pass              
                    return jj
            except Exception:
                pass

        
    if isinstance(detailedFiles, dict):
        try: 
            cited_works= detailedFiles.get('listBibl').get('biblStruct')
            cited_works=[i for i in cited_works]
            jj = []
            for sitem in cited_works:
                c_work={}
                try: 
                    sitem.pop('@xml:id')
                    sitem.pop('@coords')
                    cited_title= sitem.get('analytic').get('title').get('#text')
                    cited_journal = sitem.get('monogr').get('title').get('#text')
                    cited_year = sitem.get('monogr').get('imprint').get('date').get('#text')
                    c_work['cited_title']=cited_title
                    c_work['cited_journal']=cited_journal
                    c_work['cited_year']=cited_year
                    for stitle in sitem['analytic']['author']:
                        fname= stitle.get('persName').get('forename')
                        if  isinstance(fname, list):
                            flname=[i['#text'] for i in fname]
                            lname= stitle['persName'].get('surname')
                            flname= flname + [lname]
                            flname= ' '.join(flname)
                            c_work['author']=flname
                            jj.append(c_work)
                        else:
                            fname= stitle.get('persName').get('forename').get('#text')
                            lname= stitle['persName'].get('surname')
                            flname= fname +' '+ lname
                            c_work['author']=flname
                            jj.append(c_work)
                except Exception:
                    pass              
                return jj
        except Exception:
            pass


# %%
def citing_title(detailFile):
    """Extracts the main author and title from xml"""
    main_pub_root= detailFile.get('TEI').get('teiHeader').get('fileDesc').get('sourceDesc').get('biblStruct')
    
    return main_pub_root

def remove_none_title(dicct):
    if not isinstance(dicct ,type(None)):
        return dicct.get('#text')
    
def extract_from_lsst(lsst):
    return lsst.get('#text')

    
def remove_none_author(dicct):
    if not isinstance(dicct ,type(None)):
        if not isinstance(dicct, list):
            if not isinstance(dicct.get('persName'), list):
                if isinstance(dicct.get('persName').get('forename'), str):
                    return dicct.get('persName').get('forename').get('#text')
                   
                else:
                    fname= dicct.get('persName').get('forename')
                    lname= dicct.get('persName').get('surname')
                    if  isinstance(fname, list):
                        fname=[i['#text'] for i in fname]
                    else:
                        fname= dicct.get('persName').get('forename')
                        if not isinstance(fname,type(None)):
                            try:
                                return ' '.join((fname.get('#text'), lname))
                            except  Exception:
                                pass
        else:
            try:
               
               f_lname=[(extract_from_lsst(item.get('persName').get('forename')), item.get('persName').get('surname'))  
                                                        for item in dicct if not isinstance(item.get('persName'),type(None)) ]
               return [' '.join((item[0], item[1])) for item in f_lname]
            except Exception:
                pass
    if isinstance(dicct, dict):
        fname= dicct.get('persName').get('forename')
        lname= dicct.get('persName').get('surname')
        if  isinstance(fname, list):
            fname=[i['#text'] for i in fname]
        else:
            fname= dicct.get('persName').get('forename')
            if not isinstance(fname,type(None)):
                try:

                    return ' '.join((fname.get('#text'), lname))
                except  Exception:
                    pass

def date_formatting(subitem_dict):
    if not isinstance(subitem_dict.get('monogr'),type(None)):
        try:
            return subitem_dict.get('monogr').get('imprint').get('date').get('@when')
        except Exception:
            return "UNAVAILBLE_PUBLICATION_DATE"
        
def title_formattting(subitem_dict):
    if not isinstance(subitem_dict.get('monogr').get('title'), list):
        if not isinstance(subitem_dict.get('monogr'), type(None)):
            return subitem_dict.get('monogr').get('title').get('#text')
    


def cited_titles(detailedFiles):
    """Extracts the cited titles, author from xml"""
    backmaterial= detailedFiles.get('TEI').get('text').get('back').get('div')
    if isinstance(backmaterial, list):
        bblstruct= [item.get('listBibl').get('biblStruct') for item in backmaterial if not isinstance(item.get('listBibl'),type(None))
                                                    and item.get('@type') == 'references' ]
        bblstruct=[(remove_none_title(subitem.get('analytic').get('title')), 
                                                       remove_none_author(subitem.get('analytic').get('author')),
                                                       title_formattting(subitem),
                                                       date_formatting(subitem)
                                                      ) 
                                                    for item in bblstruct for subitem in item 
                                                    if not isinstance(subitem.get('analytic') ,type(None)) ]
                                                  
        return bblstruct
    

    else:
        try: 
            cited_works= detailedFiles.get('listBibl').get('biblStruct')
            cited_works=[i for i in cited_works]
            jj = []
            for sitem in cited_works:
                c_work={}
                try: 
                    sitem.pop('@xml:id')
                    sitem.pop('@coords')
                    cited_title= sitem.get('analytic').get('title').get('#text')
                    cited_journal = sitem.get('monogr').get('title').get('#text')
                    cited_year = sitem.get('monogr').get('imprint').get('date').get('#text')
                    c_work['cited_title']=cited_title
                    c_work['cited_journal']=cited_journal
                    c_work['cited_year']=cited_year
                    for stitle in sitem['analytic']['author']:
                        fname= stitle.get('persName').get('forename')
                        if  isinstance(fname, list):
                            flname=[i['#text'] for i in fname]
                            lname= stitle['persName'].get('surname')
                            flname= flname + [lname]
                            flname= ' '.join(flname)
                            c_work['author']=flname
                            jj.append(c_work)
                        else:
                            fname= stitle.get('persName').get('forename').get('#text')
                            lname= stitle['persName'].get('surname')
                            flname= fname +' '+ lname
                            c_work['author']=flname
                            jj.append(c_work)
                except Exception:
                    pass              
                return jj
        except Exception:
            pass  

# %%


counter = 0

all_citations=[]
file_dir='' ##REPLACE THE FILE DIRECTOR WITH XML 
for item in os.listdir(Path(file_dir)):
    counter +=1
    # if counter ==15:
    #     break
    if 'xml' in str(item).split('.'):
        item = Path(f'{file_dir}/{item}')
        with open(item, 'r') as f:
            my_xml = f.read()
            dd= json.loads(xmltojson.parse(my_xml))
            f.close()
            citing_titles=citing_title(dd)
            citedd_titles= cited_titles(dd)

            citing_title_publish_journal= dd.get('TEI').get('teiHeader').get('fileDesc').get('titleStmt')
           
     
            if not isinstance(dd.get('TEI').get('teiHeader').get('fileDesc').get('sourceDesc').get('biblStruct').get('monogr').get('imprint'), type(None)):
                try: 
                    citing_title_pub_year= dd.get('TEI').get('teiHeader').get('fileDesc').get('sourceDesc').get('biblStruct').get('monogr').get('imprint').get('date').get('@when')
                except Exception:
                    pass 

            main_article={}
            #print(citing_title_pub_year)
            main_article['main_publish_date']=citing_title_pub_year
            main_article['cited_titles']=citedd_titles
            if not isinstance(citing_titles.get('analytic'), type(None)):
               
                if not isinstance(citing_titles.get('analytic').get('title'), type(None)):
                    if not isinstance(citing_titles.get('analytic').get('author'), type(None)):
                        main_article_authors=[]
                        for main_authors in citing_titles.get('analytic').get('author'):
                            if not isinstance(main_authors, str):
                                if not isinstance(main_authors.get('persName'),type(None)):
                                    principal_title= citing_titles.get('analytic').get('title').get('#text')

                                    authors_fname= main_authors.get('persName').get('forename')
                                    authors_lname= main_authors.get('persName').get('surname')
                                    if isinstance(authors_fname, list):
                                        flname=' '.join([i['#text'] for i in authors_fname])
                                        authors_fname=flname
                                    else:
                                        if not isinstance(authors_fname, type(None)):
                                            authors_fname=authors_fname.get('#text')
                                    principal_title, principal_author_fname, principal_author_lname = principal_title, authors_fname, authors_lname 
                                    
                                    main_article_authors.append((principal_author_fname, principal_author_lname))
                                    main_article['main_title']=principal_title
                        main_article['main_authors']=main_article_authors
            all_citations.append(main_article)
