from selenium import webdriver
from bs4 import BeautifulSoup as bs, SoupStrainer
from time import sleep # this should go at the top of the file
import pandas as pd

browser = webdriver.ChromiumEdge()
_inline_class = SoupStrainer(attrs={'class': 'texttitle-blue'})
path_to_nci.csv = ""
nci = pd.read_csv('path/to/nci.csv', dtype=str).set_index("NCI_CODE")
nci['NAME'] = ''
ncodes = nci.index
print(ncodes)
for code in ncodes:
    browser.get(f"https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code={code}")
    sleep(0.01)
    innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = bs(innerHTML, 'html.parser', parse_only=_inline_class)
    nci.loc[code]['NAME'] = soup.text
    # print(nci)
    # if code == 'C3512': break

nci.to_csv('path/to/nci_and_name.csv')