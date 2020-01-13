import requests
import datetime
from bs4 import BeautifulSoup
from time import sleep
from pylancersql import Pylancersql
import re
from IPython import embed

# make a scraper object
class PphScraper:

	# initialize with a page to scrape
	def __init__(self, page):
		self.page = page
		self.sql = Pylancersql()
		self.link_parser()

	def price_parser(self, soup):

		""" parses prices from a given soup 
			object and returns the price,
		 	currency and payment type in a form of a list """
		

		price = soup.find('div', {'class': 'value price-tag'}).find('span').get_text().replace('k', '00').replace('.','')

		currency = soup.find('div', {'class': 'value price-tag'}).get_text()[0]
		payment_type = soup.find('div', 
			{'class': 'col-xs-6 budget no-padding-left no-padding-right'}).find('label', 
			{'class': 'discreet'}).get_text()
		if re.search('[0-9]', price) is None:
			return ['price not mentioned', currency, payment_type]
		return [price, currency, payment_type] 


	def time_parser(self, time):

		"""parses the time and formats it into 
		a datetime format
		 supported by the 
		 database """

		if time.split()[1] == 'days' or time.split()[1] == 'day':
			time_to_format =  datetime.datetime.now() - datetime.timedelta(days=int(time.split()[0]))
			return datetime.datetime.strftime(time_to_format, '%D')
		elif time.split()[1] == 'weeks' or time.split()[1] == 'week':
			time_to_format = datetime.datetime.now() - datetime.timedelta(days=int(time.split()[0])*7)
			return datetime.datetime.strftime(time_to_format, '%D')
		elif time.split()[1] == 'hours' or time.split()[1] == 'hour':
			return datetime.datetime.strftime(datetime.datetime.now(), '%D')


	# get the links from the page 
	def link_parser(self):

		""" parses the jobs links on the page  """


		r = requests.get(self.page)
		soup = BeautifulSoup(r.text, 'html.parser')
		h6 = soup.findAll('h6')
		self.links = [x.find('a')['href'] for x in h6[1:]]

	# get the required data from the links and insert it into the database
	def get_data(self):

		""" loops over the links given,
			gets the html, parses the required data
			and sends it to the database using the add_row() """



		for link in self.links:
			request = requests.get(link)
			soup = BeautifulSoup(request.text, 'html.parser')
			title = soup.find('h1').get_text()	
			print(title)
			sleep(5)
			exp_level = soup.find('div', {'class': 'description-experience-level'}).get_text().replace('\n','').strip().replace('Experience Level: ', '')
			print(exp_level)
			sleep(3)
			price, currency, payment_type = self.price_parser(soup)
			sleep(5)
			print(price)
			sleep(3)
			print(payment_type)
			sleep(5)
			print('the currency used is ' + currency)
			time_posted = self.time_parser(soup.find('time').get_text())
			sleep(5)
			print(time_posted)
			number_of_proposals = soup.find('span', {'class': 'info-value'}).get_text().strip()
			sleep(1)
			print(number_of_proposals)
			description = soup.find('div', {'class': 'project-description gutter-top'}).get_text().strip()
			print(description)
			sleep(5)
			unique_job_id = link.split('-')[-1]
			self.sql.add_row(title, exp_level, price, currency, payment_type, time_posted, number_of_proposals, description, 'People Per Hour', link, unique_job_id)





if __name__ == "__main__":
	r = requests.get('https://www.peopleperhour.com/freelance-python-jobs')
	soup = BeautifulSoup(r.text, 'html.parser')
	pages_list = sorted(list({x['data-page'] for x in soup.find('div',
				 {'class':'pagination clearfix'}).find('ul').findAll('a')}))

	for page in pages_list:
		current_page = PphScraper(f'https://www.peopleperhour.com/freelance-python-jobs?page={page}')
		current_page.get_data()