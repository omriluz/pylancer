''' 
to make my code production ready by saturday i need to:
handle scheduling for the scrapers either by sleep or a cron-job or any other method
start working with a vcs!
	go through files to see what you need and what you dont need 
	create a private repo on github
	upload project files
document my code
	learn how to document code
	do it
learn how to update and delete sql queries and do it
rename files to make sense
decide what to do with the footer for now

work on at least one more scraper (this should be the last part you work on)
'''

# start working with vcs
# if twago on job page refer to sign up with affiliate
# pph banner in green bold with post a job css referring to pph affiliate
# upload site to the web
# use cloudflare on the site
# use google analytics
# UPDATE and DELETE sql queries accordingly
# work on the rest of the scrapers
# design main page...get rid of unnecessary spaces
# email alerts for a certain search
# smtp server with python for sending email alerts?
# rename files to make sense
# make a login/signup # database for login credentials needed
# set cookies
# make a pylancer gmail account
# active search bar
# try arrow module for time manipulation instead or in tandem with datetime module

from flask import (Flask, render_template, url_for,
				 redirect, request, make_response)
from flask_obscure import Obscure
import sqlite3
from pylancersql import Pylancersql
from currency_conversions import Currency
import json


sql = Pylancersql()
converter = Currency()
app = Flask(__name__)
app.config['OBSCURE_SALT'] = 4049
obscure = Obscure(app)

def logofinder(site):
	if site == "People Per Hour":
		return 'static/assets/img/peopleperhour-logo2.png'
	elif site == 'Twago':
		return 'static/assets/img/twago logo.png'
	elif site == 'Truelancer':
		return 'static/assets/img/favicon/truelancerlogo.png'
	else:
		return 'what am i gonna doooo'


def currency_converter(price, currency):
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
	return int(int(price) / divider)


number_of_pages = sql.number_of_pages()


# @app.route('/save')
# def set_cookie():
# 	resp = make_response(redirect(url_for('kaka')))
# 	resp.set_cookie('cookie', 'shlomo')
# 	return resp

# @app.route('/kaka')
# def kaka():
# 	return request.cookies.get('cookie')


@app.route("/")
def index():
	
	data = sql.get_page_posts()
	nums = range(len(data))
	return render_template('htmlattempts.html', search=search, currency_converter=currency_converter,
												int=int, str=str,
												job_page=job_page, data=data,
												nums=nums, logofinder=logofinder,
												number_of_pages=number_of_pages)


@app.route("/page=<int:page>")
def pagination(page=1):
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
	job_details = sql.job_details(job_id)
	return render_template("job-page.html", job_details=job_details, logofinder=logofinder, currency_converter=currency_converter)


@app.route('/search', methods=['GET', 'POST'])
def search():
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