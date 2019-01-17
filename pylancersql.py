import sqlite3
from math import ceil
from IPython import embed

class Pylancersql:
	def __init__(self):
		self.create_table()
		self.connection = sqlite3.connect('pylancer.db')
		self.c = self.connection.cursor()
		

	def create_table(self):
		self.c.execute("""
			CREATE TABLE IF NOT EXISTS pylancer (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT,
    		exp_level TEXT,
    		price TEXT,
    		currency TEXT,
    		payment_type TEXT,
    		time_posted DATETIME,
    		number_of_proposals TEXT,
    		description TEXT,
    		website TEXT,
    		link TEXT,
    		unique_job_id TEXT
    		)""")
		self.connection.commit()



	# SCRAPING METHODS


	def add_row(self, title, exp_level, price, currency, payment_type, time_posted, number_of_proposals, description, website, link, unique_job_id):
		self.connection
		self.c.execute("""INSERT INTO pylancer VALUES (:id, :title,
													 :exp_level, :price,
													  :currency, :payment_type, :time_posted,
													   :number_of_proposals,
													    :description, :website,
													     :link, :unique_job_id)""",
			{'id':None,'title':title,
			 'exp_level':exp_level,
			  'price':price, 'currency':currency,
			  	'payment_type':payment_type,
			   'time_posted':time_posted,
			    'number_of_proposals':number_of_proposals,
			     'description':description,
			      'website':website, 'link':link,
			       'unique_job_id':unique_job_id})
		self.connection.commit()

	# SITE METHODS
	
	# def search_site(self, search_term, page=1):
	# 	self.c.execute("SELECT * FROM pylancer WHERE title LIKE '%{}%' ORDER BY id LIMIT 10 OFFSET {}".format(search_term, (page-1)*10))
	# 	return self.c.fetchall()

	def search_site(self, search_term):
		self.c.execute("SELECT * FROM pylancer WHERE title LIKE '%{}%' ORDER BY id LIMIT 10 OFFSET {}".format(search_term))
		return self.c.fetchall()

	def get_page_posts(self, page=1):
		with sqlite3.connect('pylancer.db') as connection:
			c = connection.cursor()
			c.execute(("SELECT * FROM pylancer ORDER BY id LIMIT 10 OFFSET :offset"), {"offset": (page - 1) * 10})
			return c.fetchall()


	def delete_expired_posts(self):
		pass


	def sort_by_time(self, page=1):
		with sqlite3.connect('pylancer.db') as connection:
			c = connection.cursor()
			c.execute(("SELECT * FROM pylancer ORDER BY time_posted ASC LIMIT 10 OFFSET :offset"), {"offset": (page - 1) * 10})
			return c.fetchall()


	
	def number_of_pages(self):
		with self.connection:
			self.c.execute("SELECT COUNT() FROM pylancer")
			return ceil(self.c.fetchone()[0] / 10)


	# instantiate the connection here as it has to be formed in the thread
	def job_details(self, job_id):
		with sqlite3.connect('pylancer.db') as connection:
			c = connection.cursor()
			c.execute("SELECT * FROM pylancer WHERE id=:id", {"id": job_id})
			return c.fetchall()
