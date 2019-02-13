import requests
import json
import sqlite3
from datetime import datetime, timedelta
from IPython import embed

class Currency():

	def __init__(self):
		self.update_currency()

	def get_currency(self, currency):

		"""gets the current rate for the currency compared to usd
		   for the given currency caches it in a dictionary,
		   if the function is used after an hour from the previous usage
		   it calls the api again"""
		
		if (datetime.now() - self.last_updated).seconds > 3600:
			self.update_currency()
		return self.rates[currency]

	def update_currency(self):

		"""updates currency and 
		caches result inside the
		 rates dictionary"""

		self.last_updated = datetime.now()
		eur = requests.get('http://www.floatrates.com/daily/usd.json')
		eur = json.loads(eur.text)['eur']['rate']
		inr = requests.get('http://www.floatrates.com/daily/usd.json')
		inr = json.loads(inr.text)['inr']['rate']
		gbp = requests.get('http://www.floatrates.com/daily/usd.json')
		gbp = json.loads(gbp.text)['gbp']['rate']
		self.rates = {'gbp':gbp,'inr':inr,'eur':eur,'last_updated':self.last_updated}



