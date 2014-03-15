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


# Really should be using smaller methods and testing what I'm
# actually using, but this'll do for now...
def test ():
    albert = describe_person( 'http://en.wikipedia.org/wiki/Einstein' )
    if albert[0] != 'Albert Einstein':
        print 'describe_person failed. Expected "Albert Einstein", got ' + str( albert[0] ) + '"'
    if type( albert[1] ) is not int:
        print 'describe_person failed. Expected an int, got ' + str( albert[1] )


def count_words ( soup ):
    words = soup.getText()
    return len( words.split() )


def describe_person ( url ):
    soup = BeautifulSoup( urlopen( url ) )
    page_content = soup.find( id = 'content' )
    name = page_content.find( 'h1', id = 'firstHeading' ).getText()
    words = count_words( page_content.find ( id = 'mw-content-text' ) )
    print [ name, words ]
    return [ name, words ]


def scrape_list ( url, results ):
    if url is False:
        return results

    soup = BeautifulSoup( urlopen( url ) )
    page_content = soup.find( 'div', id = 'mw-pages' )

    try:
        next_page = page_content.find( 'a', text = 'next 200' ).parent.get( 'href' )
    except AttributeError as e:
        next_page = False

    for column in page_content.findAll( 'td' ):
        for link in column.findAll( 'a' ):
            results.append( describe_person( wiki_base + link.get( 'href' ) ) )

    return scrape_list( next_page, results )


def organize():
    for year, people in important_people['births'].items():
        people.sort( key = lambda x: x[ 1 ] )


def run( first, last ):
    for year in range( first, last + 1 ):
        important_people['births'][year] = scrape_list( wiki_base + list_base + str( year ) + births, [] )
    organize()


# test()
run( 1900, 1980 )
