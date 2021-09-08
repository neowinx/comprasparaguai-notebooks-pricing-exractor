import os

from bs4 import BeautifulSoup
from requests import Session
import xlsxwriter
import re

host = 'www.comprasparaguai.com.br'
base_url = f'https://{host}'

print('processing...')

try:
    s = Session()
    s.headers['Host'] = host
    # s.headers['Connection'] = 'keep-alive'
    # s.headers['Content-Length'] = '41'
    # s.headers['Cache-Control'] = 'max-age=0'
    # s.headers['Upgrade-Insecure-Requests'] = '1'
    # s.headers['Origin'] = 'https://www.smb.com.py:8181'
    # s.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.2 Chrome/87.0.4280.144 Safari/537.36'
    s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    # s.headers['DNT'] = '1'
    s.headers['Accept-Language'] = 'en-US,en;q=0.9'
    # s.headers['Sec-Fetch-Site'] = 'same-origin'
    # s.headers['Sec-Fetch-Mode'] = 'navigate'
    # s.headers['Sec-Fetch-User'] = '?1'
    # s.headers['Sec-Fetch-Dest'] = 'document'
    # s.headers['Referer'] = 'https://www.smb.com.py:8181/smbonline/'
    s.headers['Accept-Encoding'] = 'gzip, deflate, br'
    # s.headers['Cookie'] = 'JSESSIONID=8c6a2063ed3bae567fb71a20c329'

    workbook = xlsxwriter.Workbook('notebooks_comprasparaguai.xlsx')
    worksheet = workbook.add_worksheet()

    current_row = 1
    width = 10

    for current_page in range(17,30):
        print(f"  page {current_page}... ")

        results = s.get(f"{base_url}/notebook/?page={current_page}&ordem=menor-preco")
        parsed = BeautifulSoup(results.content, "html.parser")

        p = re.compile('U\$[^0-9]+([0-9,]+)')

        for row in parsed.find_all('div', 'promocao-produtos-item-text'):
            for a in row.find_all('a', 'truncate'):
                text = str.strip(a.getText())
                if width < len(text):
                    width = len(text) 
                worksheet.write_url(f'A{current_row}', f"{base_url}{a['href']}", string=text)
            for a in row.find_all('div', 'promocao-item-preco-oferta'):
                text = str.strip(a.getText())
                result = p.search(text)
                worksheet.write(f'B{current_row}', result.group(1) if result else None)
            current_row = current_row + 1

    worksheet.set_column(0, 0, width)

    workbook.close()

except Exception as ex:
    print(ex)

