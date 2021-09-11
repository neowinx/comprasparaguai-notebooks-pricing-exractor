import os
from functools import reduce

from bs4 import BeautifulSoup
from requests import Session
import xlsxwriter
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from processors import processors

descriptions = [
    'Notebook Acr A315-56-31HU i3 1.2/4G/1TB 15.6',
    'Notebook Lenovo Ideapad 3 15ITL05 i3-1115G4 3.0GHZ/ 4GB/ 128GB SSD/ 15.6"FHD/ W10/ Ingles Abyss Azul',
    'Notebook Dell 3000-3511 Intel i3 de 11/ 4GB/ 128GB SSD/ 15.6" FHD/ W10',
    'Notebook Acr A315-54K-39UO i3 4/1TB/15.6 PR',
    'Notebook Lenovo Ideapad Flex 5 14ARE05 - Ryzen 3 4300U 2.7 GHZ - 4/128GB - 14" - Cinza',
    'Notebook Acer A515-56-36UT Intel Core i3 3.0GHz / Memória 4GB / SSD 128GB / 15.6" / Windows 10',
    'Notebook Acer A315-23-R4PF AMD Athlon 3050U/ 12GB/ 1TBGB HDD/ 15.6" HD/ W10',
    'HP AMD Ryzen 3-3250U 15-EF1041, 4GB Memoria, 256GB SSD, 15" Touchscreen',
    'Notebook Acer Intel Core i3-1115G4/ 128GB SSD/ 4GB Ram/ Tela 15.6" / Windows 10 - Prata',
    'Notebook HP 15-DA2018LA Intel Core i3 2.1GHz / Memória 4GB / HD 1TB / 15.6" / Windows 10',
    'Notebook Gateway GWTN156-4PR AMD Ryzen 5 3450U/ 8GB/ 256GB SSD/ 15.6" FHD/ W10',
    'Notebook HP 15-DA0286NIA Intel Core i3 2.2GHz / Memória 4GB / HD 1TB / 15.6" / FreeDOS',
    'Notebook Dell Inspiron 15 3505 15.6" AMD Athlon Silver 3050U HDD 1 TB - Prata',
    'Notebook Dell Inspiron 15 3505 15.6" AMD Athlon Silver 3050U SSD 256 GB - Prata',
    'Notebook Dell Inspiron 15-3505 RYZEN3-2.6/ 4GB/ 128SSD/ 15.6"/ W10 White',
    'HP, Intel Pentium, 15-DA0018, 8GB Memoria, 256GB SSD, 15" Pantalla Tactil, Silver',
    'HP Intel Pentium, 15-DA0019, 8GB Memoria, 256GB SSD, 15" Pantalla Tactil Gold',
    'HP Intel Pentium, 15-DA0020, 8GB Memoria, 256GB SSD, 15" Pantalla Tactil, Rose',
    'Notebook Lenovo IdeaPad 3 15IML05 81WR000FUS Intel Core i3 2.1GHz / Memória 8GB / SSD 256GB / 15.6" / Windows 10',
    'Notebook Evoo EVC141-12SL AMD Ryzen 5 2.1GHz / Memória 8GB / SSD 256GB / 14.1" / Windows 10',
    'Notebook Dell Inspiron I3493-3464 14" Intel Core i3-1005G1 - Prata',
    'Notebook Lenovo Ideapad 3 Intel Core i3 / 256GB SSD / 8GB Ram / TELA15.6" Touch / Windows 10 - Azul',
    'Notebook HP Chromebook X360 14-CA0013DX - Celeron N4000 1.1 GHZ - 4/32GB - 14" - Touchscreen - Prata',
    'Notebook Dell Inspiron 14 3493 Intel i3 de 10/ 4GB/ 128GB SSD/ 14.0" HD/ W10',
    'Notebook Evoo Ultra Thin EVC141-12BK 14.1" AMD Ryzen 5 3500U - Preto',
    'Notebook Evoo EVC141-12BK AMD Ryzen 5 3500U/ 8GB/ 256GB SSD/ 14.1" FHD/ W10',
    'Notebook HP 15-DW0023CL i3 8 2.1/ 4GB/ 128SSD/ 15.6"/ W10/ Silver/ REFURB3',
    'Notebook HP 15-DY1042NR - Ryzen 3 3250U 2.6 GHZ - 4/256GB - Touchscreen - 15.6" - Prata - Recondicionado',
    'Notebook Lenovo 3 15IML05 i3 10110U/8G/256SSD/15" Blue.',
    'Notebook Lenovo Ideapad 3 15IML05 Intel i3 de 10/ 8GB/ 256GB SSD/ 15.6" HD/ W10',
    'Notebook Asus VivoBook Flip TP412FA-OS31T Intel Core i3 2.1GHz / Memória 4GB / SSD 128GB / 14" / Windows 10',
    'Notebook Lenovo Idea 3 15IILO5 i3 1.2/8GB/256 15.6',
    'Dell NB 14-3493-1005G1 i3/4GB/1TB/14"',
    'Notebook Dell 7350 Tab 2 In 1 M5Y70-1.2GHZ/ 8GB/ 256SSD/ 13.3" Ips F.HD Touchscreen/ W10 Black',
    'NTB HP Probook 640 G1 i5-4300M 2.6GHZ/8GB/1TB/W10PRO 14"Ref',
    'Notebook HP i3-1005G1 15-DW2047LA 4GB-Ram/1TB-HDD/W10H/15"',
    'Notebook Lenovo Ideapad 3 15IML05 Intel Core i3-10110U de 2.1GHZ Tela HD Touch Screen 15.6" / 8GB de Ram / 256GB SSD - Abyss Azul',
    'Notebook HP Split X2 13-R100 i3/ 4GB/ 500GB/ 13P/ Touch/ W8 Recond.',
    'Notebook Asus Vivobook Flip TP412F TP412F-OS31T Intel Core i3-8145U 14" W10 4/128GB SSD - Star Grey',
    'Notebook HP 15-DY1025NR i3-1005G1 15.6" W10H 4/256GB SSD - Silver (Refurbished)'
]

parsers = list(map(lambda x: re.compile(x), [
    'NTB HP (.+) I\d',
    'NOTEBOOK (.+) I\d',
    'NOTEBOOK (.+) RYZEN',
    'NOTEBOOK (.+) INTEL CORE',
    'NOTEBOOK (.+) INTEL',
    'NOTEBOOK ([ A-Z0-9-."]+) AMD',
    #'DELL NB (.+) I\d',
    '^NOTEBOOK HP ([A-Z0-9-].+)\dGB',
    'HP,? INTEL PENTIUM, ([ A-Z0-9-]+), ',
    'HP,? ([ A-Z0-9-]+), ',
    'NOTEBOOK ([ A-Z0-9-.]+)/',
    '([ A-Z0-9-]+) - ',
    '([ A-Z0-9-]+)/',
    '([ A-Z0-9-]+), ',
]))

options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)

def parse_desc(desc):
    sp = desc.upper().split('/')[0]
    sp1 = ''
    for word in sp.split(' '):
        if ('GB' in word 
                or 'PRETO' in word
                or 'PRATA' in word
                or 'TELA' in word):
            break
        sp1 += ' ' + word.replace('ACR', 'ACER').replace('NOTEBOOK', '')
    sp2 = ''
    for word in sp1.strip().split(' '):
        if 'I3' in word:
            break
        sp2 += ' ' + word
    return sp2.strip()


def return_info(search_term):
    print(f'search_term: {search_term}')
    
    search_url = f'https://www.google.com/search?q={"+".join(search_term.strip().split(" "))}+characteristics+processor&ie=utf-8&oe=utf-8'
    print('  ' + search_url)
    browser.get(search_url)
    
    try:
        elem = browser.find_element_by_class_name('xpdopen') 
        infos = [info.text for info in elem.find_elements_by_tag_name('li')]
        if len(infos) == 0:
            infos = [info.text for info in elem.find_elements_by_tag_name('tr')]
        filters = ['PROCESSOR MODEL', 'PROCESSOR', 'RYZEN', 'I7', 'I5', 'I3', 'ATLHON'] 
        for filt in filters:
            filtered = list(filter(lambda x: filt in x.upper(), infos))
            if len(filtered) > 0:
                return filtered[0]
    except Exception as ex:
        print(f'  xpdopen not found for {search_term}')
    
    return None


def match_processor_in_description(descs):
    l = []
    for d in descs:
        n = {'description': d}
        for p in processors:
            if p in d['name']:
                n['name'] = p['name']
                n['count'] = p['count']
                break
        l.append(n)
    return l

for description in descriptions:
    print("==========================")
    print(description)
    l = match_processor_in_description(processors)
    pardes = parse_desc(description)
    #print(pardes)
    #info = return_info(pardes)
    #print(f'  info: {info}')


