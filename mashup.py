from flask import Flask, render_template, session, jsonify, request, redirect, url_for, abort
import requests, settings

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mashup')
def mashup():
	congress_number = request.args.get('congress_number')
	chamber = request.args.get('chamber')
	state = request.args.get('state')
	api_key = settings.CONGRESS_API_KEY
	uri = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/{0}/{1}/members.json".format(congress_number, chamber)
	results = requests.get(uri, params={'state': state, 'api-key': api_key})
	members = results.json()['results'][0]['members']

	return render_template('mashup.html', members=members)

@app.route('/bills/<member_id>')
def bills(member_id):
	api_key = settings.CONGRESS_API_KEY
	uri = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/members/{0}/bills/cosponsored.json".format(member_id)
	results = requests.get(uri, params={'api-key': api_key})
	return jsonify(results.json())

if __name__ == '__main__':
    app.run(debug=True, port=8000)