import io, json
from datetime import datetime
from bs4 import BeautifulSoup
from urllib2 import urlopen

sentinel = object()
startTime = datetime.now()

wiki_base = 'http://en.wikipedia.org'
list_base = '/w/index.php?title=Category:'
births = '_births'
deaths = '_deaths'
important_people = {
    'births': {},
#    'deaths': {},
}


# Really should be using smaller methods and testing what I'm
# actually using, but this'll do for now...
def test():
    albert = describe_person('http://en.wikipedia.org/wiki/Einstein')
    if albert[0] != 'Albert Einstein':
        print 'describe_person failed. Expected "Albert Einstein", got "' + unicode(albert[0]) + '"'
    if type(albert[1]) is not int:
        print 'describe_person failed. Expected an int, got ' + unicode(albert[1])


def count_words(soup):
    words = soup.get_text()
    return len(words.split())


def describe_person(url):
    soup = BeautifulSoup(urlopen(url))
    page_content = soup.find(id = 'content')
    name = page_content.find('h1', id = 'firstHeading').get_text()
    words = count_words(page_content.find(id = 'mw-content-text'))
    #name = name.encode('utf-8')
    print 'Done ' + name
    return [name, words]


def scrape_list(url, results):
    soup = BeautifulSoup(urlopen(url))
    page_content = soup.find('div', id = 'mw-pages')

    try:
        next_page = page_content.find('a', text = 'next 200').get('href')
    except AttributeError as e:
        next_page = False

    for column in page_content.find_all('td'):
        for link in column.find_all('a'):
            results.append(describe_person(wiki_base + link.get('href')))

    if next_page:
        return scrape_list(wiki_base + next_page, results)
    else:
        return results


def organize():
    for year, people in important_people['births'].items():
        people.sort(key = lambda x: x[1], reverse = True)


def run(first, last = sentinel):
    if last is sentinel:
        last = first

    for year in range(first, last + 1):
        important_people['births'][year] = scrape_list(wiki_base + list_base + unicode(year) + births, [])

    organize()

    with io.open(unicode(first) + '-' + unicode(last) + '-births.json', 'w', encoding='utf-8') as f:
      f.write(unicode(json.dumps(important_people, ensure_ascii = False)))


run(1987)

print 'Completed in ' + unicode(datetime.now() - startTime)
