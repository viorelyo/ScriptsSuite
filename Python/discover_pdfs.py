import os
import requests
import shutil
from tqdm import tqdm
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def check_disk(disk, limit):
    total, used, free = shutil.disk_usage(disk)

    free = free // (2**20)
    if free <= limit:
        return False
    return True


def download_xakep_pdfs(download_path, start_nr, stop_nr):
    url = "https://xakep.ru/pdf/xa/"

    for i in range(start_nr, stop_nr + 1):
        if not check_disk(download_path[:3], 200):
            print("Out of memory!")
            break

        u = urljoin(url, str(i))
        filename = os.path.join(download_path, str(i)) + ".pdf"
        download_file(u, filename)


def scrape_pdfs(url, download_path):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    s = soup.select('a[href*="pdf"]')
    for link in s:
        print("> ", link)
        filename = os.path.join(download_path, link['href'].split('/')[-1])
        print("> ", filename)
        download_file(urljoin(url, link['href']), filename)
        print()


def read_content_length(response):
        meta_data = dict(response.headers.items())
        return int(meta_data.get('Content-Length')) or int(meta_data.get(
            'content-length'))


def download_file(url, filename):
    print("> ", url)
    r = requests.get(url, stream=True)
    # file_size = int(r.headers['Content-Length'])
    file_size = read_content_length(r)
    
    block_size = 1024
    t = tqdm(total=file_size, unit='iB', unit_scale=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(block_size):
            t.update(len(chunk))
            f.write(chunk)
    t.close()


download_xakep_pdfs("e:\\folder", 190, 196)
