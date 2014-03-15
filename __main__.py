from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
wiki_base = 'http://en.wikipedia.org'
list_base = '/w/index.php?title=Category:'
births = '_births'
deaths = '_deaths'
important_people = {
    'births': {},
#    'deaths': {},
}


def count_words ( soup ):
    # soup.get_text()
    print 'count_words is not ready yet :('
    return 404


def describe_person ( year, url ):
    soup = BeautifulSoup( urlopen( url ) )
    page_content = soup.find( id = 'content' )
    name = page_content.find( id = 'firstHeading' ).get_text()
    words = count_words( page_content.find ( id = 'mw-content-text' )
    return [ name, words ]


def scrape_list ( url, results ):
    if url is False:
        return results

    soup = BeautifulSoup( urlopen( url ) )
    page_content = soup.find( 'div', { 'id': 'mw-pages'} )

    try:
        next_page = page_content.find( 'a', text = 'next 200' ).parent.get( 'href' )
    except AttributeError as e:
        next_page = False

    for column in page_content.findAll( 'td' ):
        for link in column.findAll( 'a' ):
            results.append( describe_person( wiki_base + link.get( 'href' ) ) )

    return scrape_list( next_page, results )


for year in range( 1900, 1981 ):
    important_people['births'][year] = scrape_list( wiki_base + list_base + str( year ) + births, [] )

for year, people in important_people['births'].items():
    people.sort( key = lambda x: x[ 1 ] )

print important_people
