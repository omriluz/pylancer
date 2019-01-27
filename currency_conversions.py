import requests
import json
import sqlite3
from datetime import datetime, timedelta
from IPython import embed

class Currency():

	def __init__(self):
		self.connection = sqlite3.connect('currency_conversions.db')
		self.c = self.connection.cursor()
		self.create_currency_table()
		self.initialize_null_values()


	def create_currency_table(self):
		self.c.execute("""
			CREATE TABLE IF NOT EXISTS currency_conversions (
			CONSTANT_ID INTEGER PRIMARY KEY,
			EUR_USD REAL,
    		GBP_USD REAL,
    		INR_USD REAL,
    		last_updated DATETIME 
    		)""")
		self.connection.commit()

	def initialize_null_values(self):
		try:
			self.c.execute("""INSERT INTO currency_conversions VALUES (:id, :eur, :inr,
														 :gbp, :last_updated)""",
				{'id':1,'eur':348,'inr':4,'gbp':3,'last_updated':'12/12/12 12:20'})
			self.connection.commit()
		except sqlite3.IntegrityError:
			pass




	def get_currency(self, currency):
		with sqlite3.connect('currency_conversions.db') as connection:
			c = connection.cursor()
			currency = currency.upper()
			# if over a period of time update and then extract
			last_updated = datetime.strptime(c.execute('SELECT last_updated FROM currency_conversions').fetchone()[0], '%m/%d/%y %H:%M')
			if (datetime.now() - last_updated).seconds > 3600:
				# self.update_currency()
				time = datetime.now()
				update_time = time.strftime('%D %H:%M')
				eur = requests.get('http://www.floatrates.com/daily/usd.json')
				eur = json.loads(eur.text)['eur']['rate']
				inr = requests.get('http://www.floatrates.com/daily/usd.json')
				inr = json.loads(inr.text)['inr']['rate']
				gbp = requests.get('http://www.floatrates.com/daily/usd.json')
				gbp = json.loads(gbp.text)['gbp']['rate']
				c.execute("UPDATE currency_conversions SET EUR_USD = :eur, GBP_USD = :gbp, INR_USD = :inr, last_updated = :update_time", {'eur':eur,'gbp':gbp,'inr':inr,'update_time':update_time})
				connection.commit()
			c.execute(f"SELECT {currency}_USD FROM currency_conversions")
			return c.fetchone()[0]
