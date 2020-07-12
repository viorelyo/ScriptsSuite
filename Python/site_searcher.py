import re
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from os.path import splitext, basename


ip_regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def validate_url(url):
    global ip_regex
    return re.match(ip_regex, url) is not None


def are_urls_related(root_url, new_url):
    return urlparse(new_url).netloc in root_url


def find_related_links(url):
    if not check_extension(url):
        return set()

    try:
        page = urlopen(url)
    except:
        return set()
    
    bsObj = BeautifulSoup(page, "html.parser")

    link_tags = bsObj.findAll('a')
    found_links = set()
    for x in link_tags:
        try:
            t = x['href']
            if validate_url(t) and are_urls_related(url, t) and check_extension(t):
                found_links.add(t)
        except KeyError:
            continue

    return found_links


def scrape_site(url, links_set, max_depth, content):
    if (0 == max_depth):
        return
    for l in find_related_links(url):
        if l not in links_set:
            links_set.add(l)
            if search_content(l, content):
                print("<=== Spotted =====>", l)
            scrape_site(l, links_set, max_depth - 1, content)


def search_content(url, content):
    page = urlopen(url)
    source = str(page.read())
    return source.find(content) != -1


def check_extension(url):
    disassembled = urlparse(url)
    filename, file_ext = splitext(basename(disassembled.path))
    return filename == "" and file_ext == ""


if __name__ == "__main__":
    URL = ""
    links_set = set()
    scrape_site(URL, links_set, 3, "")