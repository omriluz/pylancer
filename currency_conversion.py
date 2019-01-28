import requests
import json
import sqlite3
from datetime import datetime, timedelta
from IPython import embed

class Currency():

	def __init__(self):
		self.update_currency()

	def get_currency(self, currency):
		# if over a period of time update and then extract
		
		if (datetime.now() - self.last_updated).seconds > 3600:
			self.update_currency()
		return self.rates[currency]

	def update_currency(self):
		self.last_updated = datetime.now()
		eur = requests.get('http://www.floatrates.com/daily/usd.json')
		eur = json.loads(eur.text)['eur']['rate']
		inr = requests.get('http://www.floatrates.com/daily/usd.json')
		inr = json.loads(inr.text)['inr']['rate']
		gbp = requests.get('http://www.floatrates.com/daily/usd.json')
		gbp = json.loads(gbp.text)['gbp']['rate']
		self.rates = {'gbp':gbp,'inr':inr,'eur':eur,'last_updated':self.last_updated}


