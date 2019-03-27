import sqlite3
from math import ceil
from IPython import embed

class Pylancersql:
	def __init__(self):
		self.connection = sqlite3.connect('pylancer.db')
		self.c = self.connection.cursor()
		self.create_table()
		

	def create_table(self):

		""" creates the main table if it does not exist """
		
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

		""" adds a row to the database """

		self.connection

		# gets every unique job id in a list
		unique_job_ids = [x[0] for x in self.c.execute("SELECT unique_job_id FROM pylancer").fetchall()]

		if unique_job_id in unique_job_ids:
			pass
			# make an if statement to see if post needs to be deleted or updated(should a post be updated?)

		else:
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
	

	def search_site(self, search_term, page=1):
		
		""" search function to read data from
		 the database per a user's request """

		with sqlite3.connect('pylancer.db') as connection:
			c = connection.cursor()
			c.execute("SELECT * FROM pylancer WHERE title LIKE '%{}%' ORDER BY id LIMIT 10 OFFSET {}".format(search_term, page))
			return c.fetchall()


	def get_page_posts(self, page=1):

		""" handles pagination for the website """

		with sqlite3.connect('pylancer.db') as connection:
			c = connection.cursor()
			c.execute(("SELECT * FROM pylancer ORDER BY id LIMIT 9 OFFSET :offset"), {"offset": (page - 1) * 9})
			return c.fetchall()


	def delete_expired_posts(self):
		pass


	def sort_by_time(self, page=1):

		""" sorts database rows by time  """

		with sqlite3.connect('pylancer.db') as connection:
			c = connection.cursor()
			c.execute(("SELECT * FROM pylancer ORDER BY time_posted ASC LIMIT 10 OFFSET :offset"), {"offset": (page - 1) * 10})
			return c.fetchall()


	
	def number_of_pages(self):
		""" return the number of pages the site has rounded up with ceil """
		with self.connection:
			self.c.execute("SELECT COUNT() FROM pylancer")
			return ceil(self.c.fetchone()[0] / 10)


	
	def job_details(self, job_id): # instantiate the connection here as it has to be formed in the thread
		
		""" return the job details for the  """

		with sqlite3.connect('pylancer.db') as connection:
			c = connection.cursor()
			c.execute("SELECT * FROM pylancer WHERE id=:id", {"id": job_id})
			return c.fetchall()


