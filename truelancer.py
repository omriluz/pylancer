import requests
from bs4 import BeautifulSoup
from IPython import embed
import datetime
from time import sleep
import re
from pylancersql import Pylancersql

class TruelancerScraper:
	def __init__(self, page):
		self.page = page
		self.link_parser()
		self.sql = Pylancersql()


	def link_parser(self):

		""" parses the jobs links on the page  """

		r = requests.get(self.page)
		soup = BeautifulSoup(r.text, 'html.parser')
		div_list = soup.findAll('div', {'class': 'clearfix job_title'})
		self.links = [x.find('a')['href'] for x in div_list]



	def is_active(self, page):

		""" return True if a job listing is 
			still active else returns false"""
		
		r = requests.get(page)
		soup = BeautifulSoup(r.text, 'html.parser')
		status = soup.find('div',
			{'class':'text-center col-md-3 jobStatus'}).find('span').get_text()
		if status == 'Open':
			return True
		else:
			return False

	def time_parser(self, time):

		"""parses the time and format it into 
		a datetime format
		 supported by the 
		 database """
		
		if time.split()[1] == 'days' or time.split()[1] == 'day':
			time_to_format = datetime.datetime.now() - datetime.timedelta(days=int(time.split()[0]))
			return datetime.datetime.strftime(time_to_format, '%D')
		elif time.split()[1] == 'weeks' or time.split()[1] == 'week':
			time_to_format = datetime.datetime.now() - datetime.timedelta(days=int(time.split()[0])*7)
			return datetime.datetime.strftime(time_to_format, '%D')
		elif time.split()[1] == 'hours' or time.split()[1] == 'hour':
			return datetime.datetime.strftime(datetime.datetime.now(), '%D')
		elif time.split()[1] == 'month' or time.split()[1] == 'months':
			time_to_format = datetime.datetime.now() - datetime.timedelta(days=int(time.split()[0])*30)
			return datetime.datetime.strftime(time_to_format, '%D')

	def get_data(self):

		""" loops over the links given,
			gets the html, parses the required data
			and sends it to the database using the add_row() """

		for link in self.links:
			r = requests.get(link)
			soup = BeautifulSoup(r.text, 'html.parser')
			if soup.find('strong').get_text() != "Private Project!":					
				if soup.find('span', {'class':'value text-success'}).get_text() != 'Awarded':
					title = soup.find('h3', {'class': 'col-md-12'}).get_text().strip()
					if soup.find('span',{'class':'currency'}).find('div')['class'][1].split('-')[1] == 'inr':
						currency = '₹'
					elif soup.find('span',{'class':'currency'}).find('div')['class'][1].split('-')[1] == 'usd':
						currency = '$'
					if len(soup.find('span', {'class':'amount'}).get_text().strip().split()) > 1:
						price = soup.find('span', {'class':'amount'}).get_text().strip().split()[0]
						payment_type = 'Per Hour'
					else:
						price = soup.find('span', {'class':'amount'}).get_text().strip()
						payment_type = 'Fixed Price'
					description = soup.find('div',
						{'class':'job-description'}).get_text()
					exp_level = 'not mentioned'
					time_posted = self.time_parser(' '.join(soup.find('ul',{'class':'metainfo col-md-12 list-actions tl_gap_top_10'}).find('li').get_text().split()[3:]))
					proposals = soup.find('div',{'class':'text-center col-md-3 border-right border-left'}).find('span').get_text()
					print(link)
					print(title)
					sleep(3)
					print(currency)
					sleep(3)					
					print(price)
					sleep(3)
					print(payment_type)
					sleep(3)
					print(description)
					sleep(3)
					print('no exp level')
					sleep(2)
					print(time_posted)
					sleep(3)
					print(f'there are {proposals} proposals')
					sleep(3)
					unique_job_id = link.split('-')[-1]
					self.sql.add_row(title, exp_level, price, currency, payment_type, time_posted, proposals, description, 'Truelancer', link, unique_job_id)

r = requests.get('https://www.truelancer.com/freelance-python-jobs')
soup = BeautifulSoup(r.text, 'html.parser')
page_list = [x.get_text() for x in soup.find('ul',{'class':'pagination'}).findAll('li')[1:-1]]
for page in page_list:
	current_page = TruelancerScraper(f'https://www.truelancer.com/freelance-python-jobs?page={page}')
	current_page.get_data()