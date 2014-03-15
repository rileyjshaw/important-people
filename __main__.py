from BeautifulSoup import BeautifulSoup
import urllib2
wiki_base = 'http://en.wikipedia.org'
list_base = '/w/index.php?title=Category:'
births = '_births'
deaths = '_deaths'
list_page = urllib2.urlopen( wiki_base + list_base + '1900' + deaths )
soup = BeautifulSoup( list_page )

page_content = soup.find( 'div', { 'id': 'mw-pages'} )
next_page = page_content.find( 'a', text = 'next 200' ).parent.get( 'href' )

links = []

for column in page_content.findAll( 'td' ):
    for link in column.findAll( 'a' ):
        links.append( link.get( 'href' ) )

person_page = urllib2.urlopen( 'http://en.wikipedia.org' + links[ 0 ] )
soup = BeautifulSoup( person_page )

print links
print soup.prettify()
print next_page


'''

Follow every link in .mw-content-ltr

Enter article

Record name as #firstHeading > span
Record word count in #mw-content-text

analyze = function ( article ) {

}

demo = function ( list ) {
  analyze( list .mw-content-ltr a );
}

demo( 'http://en.wikipedia.org/w/index.php?title=Category:1900_deaths' );

important_births = {
  '1900': [
      [ 'Albert Einstein', 8000 ],
      [ 'Blbert Einstein', 4000 ],
      [ 'Clbert Einstein', 2000 ]
    ],
  '1901': #etc...
}

for year in important_births:
  contents.sort( key = lambda x: x[ 1 ] )

births = {
 '1900': [
  ['Alpha', 8000],
  ['Beta', 4000],
  ['Delta', 2000]
 ],
 '1901': [
  ['Air Bud', 1000],
  ['Air Bud 2', 0]
 ]
}

for year, people in births.items():
  people.sort( key = lambda x: x[ 1 ] )

print births

'''

