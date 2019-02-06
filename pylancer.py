# -*- coding: utf-8 -*-

from flask import (Flask, render_template, url_for,
				 redirect, request, make_response)
from flask_obscure import Obscure
import sqlite3
from pylancersql import Pylancersql
from currency_conversion import Currency
import json


sql = Pylancersql()
converter = Currency()
app = Flask(__name__)
app.config['OBSCURE_SALT'] = 4049
obscure = Obscure(app)

def logofinder(site):

	"returns the logo for the site given"
	
	if site == "People Per Hour":
		return 'static/assets/img/peopleperhour-logo2.png'
	elif site == 'Twago':
		return 'static/assets/img/twago logo.png'
	elif site == 'Truelancer':
		return 'static/assets/img/favicon/truelancerlogo.png'
	else:
		return 'what am i gonna doooo'


def currency_converter(price, currency):

	"converts every currency given to its price in usd"

	if price == 'price not mentioned':
		return 'price not mentioned'
	if ',' in price:
		price = price.replace(',','') 
	if currency == '₹':
		divider = converter.get_currency('inr')
	elif currency == '£':
		divider = converter.get_currency('gbp')
	elif currency == '€':
		divider = converter.get_currency('eur')
	elif currency == '$':
		divider = 1
	else:
		divider = 1
	return int(int(price) / divider)


number_of_pages = sql.number_of_pages()

@app.route("/")
def index():
	
	"home page route"
	
	data = sql.get_page_posts()
	nums = range(len(data))
	return render_template('htmlattempts.html', search=search, currency_converter=currency_converter,
												int=int, str=str,
												job_page=job_page, data=data,
												nums=nums, logofinder=logofinder,
												number_of_pages=number_of_pages)


@app.route("/page=<int:page>")
def pagination(page=1):

	"handles pagination"
	
	if page == 1:
		return redirect(url_for('index'))
	data = sql.sort_by_time(page)
	nums = range(len(data))
	return render_template('htmlattempts.html', search=search, currency_converter=currency_converter,
												int=int, str=str,
												job_page=job_page, data=data,
												nums=nums, logofinder=logofinder,
												number_of_pages=number_of_pages)


@app.route('/<tame:job_id>', methods=['GET'])
def job_page(job_id):
	
	"""a route that gets the job page 
	with the details of each individual job"""

	job_details = sql.job_details(job_id)
	return render_template("job-page.html", job_details=job_details, logofinder=logofinder, currency_converter=currency_converter)


@app.route('/search', methods=['GET', 'POST'])
def search():

	"search function for the search bar on the site"
	
	search_term = request.form['text'] 
	data = sql.search_site(search_term)
	nums = range(len(data))
	return render_template('htmlattempts.html', currency_converter=currency_converter,
												int=int, str=str,
												job_page=job_page, data=data,
												nums=nums, logofinder=logofinder,
												number_of_pages=number_of_pages)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)