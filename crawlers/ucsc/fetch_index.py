import re
from urllib2 import urlopen
from bs4 import BeautifulSoup

def fetch_soup (url):
    response = urlopen(url)
    return BeautifulSoup(response.read(), 'html.parser')

def enforce (condition, msg, *args):
    if not condition:
        raise Exception(msg % args)

def parse_department_link (a):
    href = a['href'] #if 'href' in a else ''
    #title = a['title'] if 'title' in a else ''
    match = re.match(r'program.statements/([a-z]+\.html)', href)
    enforce(match, "Unexpected link url: '%s'", href)
    text = a.text
    if text:
        return text, href

def parse_department_links (links):
    for link in links:
        result = parse_department_link(link)
        if result:
            yield result

def fetch_department_urls (base_url = 'https://registrar.ucsc.edu/catalog/programs-courses'):
    index_url = '%s/index.html'%base_url
    soup = fetch_soup(index_url)
    dept_anchor = soup.find('a', id='departments')
    enforce(dept_anchor, "Could not find '%s/#departments'", index_url)
    header = dept_anchor.parent
    enforce(header.name == "h2", "Unexpected: is not a h2 tag (got '%s')", header.name)
    table = header.findNext('td')
    enforce(table.name == "td", "Expected element after heading to be table, not '%s'", table.name)
    return {k: '%s/%s'%(base_url, v) for k, v in parse_department_links(table.find_all('a'))}


if __name__ == '__main__':
    result = fetch_department_urls()
    print(result)
