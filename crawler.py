"""
A crawler is a program that starts with a url on the web 
(ex: http://python.org), fetches the web-page corresponding to that url,
and parses all the links on that page into a repository of links. Next,
it fetches the contents of any of the url from the repository just created,
parses the links from this new content into the repository and continues 
this process for all links in the repository until stopped or after a given
number of links are fetched. 
"""

from bs4 import BeautifulSoup # pip install BeautifulSoup4
from urlparse import urlparse
import urllib2, sys 
import pdb

total_collected_url = []
visited_url = []

class crawler:
	def __call__(self, url, count_of_crawler):
		"""
		Function which fetch the content from the given URL and collect all the
		URL in the content and pass the first url of the page to fetch the
		content.
		"""
		try:
			page = urllib2.urlopen(url)
			soup = BeautifulSoup(page.read())	

			links_on_page = map(lambda anchor: anchor.get('href'), 
						soup.find_all('a'))

			cleaned_url = map(lambda link: link if urlparse(link).scheme 
	 				and urlparse(url).netloc else (urlparse(url)
					.scheme+"://"+urlparse(url).netloc+link if 
					link[0] == "/" else url+link), links_on_page)
			visited_url.append(url)
			total_collected_url.append(cleaned_url)
			next_url_to_visit = [next_url for next_url in cleaned_url\
				 if not next_url in visited_url and not "#" in next_url][0]
		
			if count_of_crawler and next_url_to_visit:	
				count_of_crawler = crawler(next_url_to_visit, 
								count_of_crawler-1)
	
		except:
			print "It seems there is some issue in URL "+url
	
		return count_of_crawler


if __name__ == '__main__':
	crawl = crawler()
	#url = raw_input("Enter the url from which you want crawler to begin: ")
	try:
		#number_of_fetching = int(raw_input("Number to page crawler to "))
		count_of_crawler = crawl(sys.argv[1], int(sys.argv[2]))
		zipped = dict(zip(visited_url,total_collected_url))
		print "Number of Links that crawler visited "+ str(len(visited_url))
		print zipped	
    	
	except ValueError:
		print "You have to enter a whole digit number over there"
		
	except IndexError:
		print "Please the enter the arguements correctly first arguement \
should be the URL and Second should be the count of URL's you want to fetch"
	
	except:
		print "Oops !!! Duh ,It seems some big issue is there crawler is not working.\
you need to check it out" 
