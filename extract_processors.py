from bs4 import BeautifulSoup
from requests import Session

s = Session()

results = s.get(f"https://www.cpubenchmark.net/mid_range_cpus.html")
parsed = BeautifulSoup(results.content, "html.parser")
statu = parsed.find('ul', 'chartlist')
lista = [{'name': li.find('span', 'prdname').text.split('@')[0].strip(), 'count': li.find('span', 'count').text } for li in statu.find_all('li')]
print(lista)
with open('processors.py', 'w', newline='', encoding="UTF-8") as processorfile:
    processorfile.write(f'processors = {lista}')
    processorfile.close()
print("done")
