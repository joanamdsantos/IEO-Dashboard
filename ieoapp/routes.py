from ieoapp import app

import json, plotly
from flask import render_template, request, Response, jsonify
from collections import OrderedDict
from scripts.macro import return_figures


@app.route('/', methods=['POST', 'GET'])

@app.route('/index/', methods=['POST', 'GET'])
def index():
	return render_template('index.html')


@app.route('/macro/', methods=['POST', 'GET'])
def macro():

	# List of countries for filter
	country_codes = OrderedDict([('Non-OECD - Africa', 'AFR'),('Non-OECD - Middle East', 'MID'), 
                               ('Non-OECD Americas - Brazil', 'BRZ'), ('Non-OECD Americas - Other', 'CSA'), 
                               ('Non-OECD Americas', 'NAM'), ('Non-OECD Asia - China', 'CHI'), 
                               ('Non-OECD Asia - India', 'IND'),   ('Non-OECD Asia - Other', 'OAS'), 
                               ('Non-OECD Asia', 'NAA'), ('Non-OECD Europe and Eurasia - Russia', 'RUS'), 
                               ('Non-OECD Europe and Eurasia - Other', 'URA'), ('Non-OECD Europe and Eurasia', 'NUR'), 
                               ('Total Non-OECD', 'NNN'),('OECD Americas - Canada', 'CAN'), 
                               ('OECD Americas - Mexico and Chile', 'MXC'), ('OECD Americas - United States', 'USA'), 
                               ('OECD Americas', 'OAM'), ('OECD Asia - Australia and New Zealand', 'ANZ'), 
                               ('OECD Asia - Japan', 'JPN'), ('OECD Asia - South Korea', 'SKO'), 
                               ('OECD Europe', 'EUR'), ('Total OECD', 'OOO'), ('Total World', 'WOR')])

	# default lists of economic growth and oil price scenarios
	scenario_codes = OrderedDict([('High economic growth', 'HIGHMACRO'),('Reference', 'REFERENCE'), 
                               ('Low economic growth', 'LOWMACRO'), ('High oil price', 'HIGHOILPRICE'), 
                               ('Low oil price', 'LOWOILPRICE')])

	# Parse the POST request countries list
	if (request.method == 'POST') and request.form:
		figures = return_figures(request.form)
		countries_selected = []

		for country in request.form.lists():
			countries_selected.append(country[1][0])

	# GET request returns all countries for initial page load
	else:
		figures = return_figures()
		countries_selected = []
		for country in country_codes:
			countries_selected.append(country[1])

	# plot ids for the html id tag
	ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

	# Convert the plotly figures to JSON for javascript in html template
	figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

	return render_template('/macro.html', ids=ids,
		figuresJSON=figuresJSON,
		all_countries=country_codes,
		countries_selected=countries_selected)

@app.route('/power/')
def power():
    return render_template('power.html')

@app.route('/energy/')
def energy():
    return render_template('energy.html')

@app.route('/carbon/')
def carbon():
    return render_template('carbon.html')

@app.route('/references/')
def references():
    return render_template('references.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")
# TODO: Add another route. You can use any names you want


# Then go into the templates folder and add an html file that matches the file name you put in the render_template method. You can create a new file by going to the + sign at the top of the workspace and clicking on Create New File. Make sure to place the new html file in the templates folder.

if __name__=="__main__":
    app.run(debug = True)