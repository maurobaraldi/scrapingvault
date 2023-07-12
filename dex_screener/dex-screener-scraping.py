#!/usr/bin/env python3

# ToDo List
# - Format data as currency, percent and datetime
# - Pack the app in a scheduled container Cron Docker https://gitlab.com/maurobaraldi/toys/-/tree/main/cron_docker
# - Add multiple pages support - Done
# - Add by blockchain support
# - Fix files path to absolute path so it can run as a service

from csv import DictWriter
from datetime import datetime
from gzip import GzipFile
from io import BytesIO
from os.path import exists
from urllib.request import Request, urlopen

from lxml import html

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Cookie': '_ga=GA1.1.763411189.1689118519; _ga_532KFVB4WT=GS1.1.1689118518.1.1.1689120935.59.0.0; chakra-ui-color-mode=dark; __cf_bm=NYe7DVpIjsfoHbdd43bRa7e1463INHj40va1P4GPrhg-1689120556-0-AedqScRhsDbuVmhFrFv4FjZTxc9yUcZOPeJfNzO10ssa0ujUDpWnEB1609AV8Uyu/CqUTquyAjoPkQi/EYTXM99MulDQZ5YQoRft2XorpEbI; _ga_RD6VMQDXZ6=GS1.1.1689119309.1.1.1689119436.0.0.0; amp_fef1e8=22336dba-c437-4f47-bd2b-8b2b4a7ce357R...1h53lmgsp.1h53lqa97.9.1.a; __cuid=5799a3bfda664cc7ba9deeebcda5b869; cf_clearance=6oWSbcWqzTbdBIiGMCwOPKiuBUIFBKl3MNhfSvMyfnc-1689118515-0-160',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
}

def request(url, headers):
    request = Request(url, headers=headers)
    with urlopen(request) as r:
        with GzipFile(fileobj=BytesIO(r.read())) as zipf:
            return zipf.read()

def scraping(page):
    page = request(f"https://dexscreener.com/page-{page}", headers)
    tree = html.fromstring(page)
    rows = tree.xpath('//*[@id="root"]/div/main/div/div[3]/a')
    result = []

    for i, _ in enumerate(rows, 1):
        row = tree.xpath(f'//*[@id="root"]/div/main/div/div[3]/a[{i}]/div')
        r = {
            'token_symbol':row[0].xpath('./span[contains(@class, "ds-dex-table-row-base-token-symbol")]')[0].text,
            'token_quote_symbol':row[0].xpath('./span[contains(@class, "ds-dex-table-row-quote-token-symbol")]')[0].text,
            'token_name':row[0].xpath('./span[contains(@class, "ds-dex-table-row-base-token-name")]')[0].text,
            'price':row[1].text_content(),
            'txns':row[2].text_content(),
            'makers':row[3].text_content(),
            'volume':row[4].text_content(),
            'five_min':row[5].text_content(),
            'one_hour':row[6].text_content(),
            'six_hour':row[7].text_content(),
            'twenty_four_hour':row[8].text_content(),
            'liquidity':row[9].text_content(),
            'fdv':row[10].text_content(),
            'datetime': str(datetime.now())
        }
        result.append(r)

    write_header = True

    if exists('./dexscreener.csv'):
        with open('./dexscreener.csv', 'r') as _:
            if _.read().startswith('token_'):
                write_header = False

    with open('./dexscreener.csv', 'a', newline='') as csvfile:
        writer = DictWriter(csvfile, result[0].keys())
        if write_header:
            writer.writeheader()
        writer.writerows(result)

for i in range(1,6):
    scraping(i)
    print('Done page', i)
