#!/usr/bin/env python3

from flask import Flask, request, jsonify
import sqlite3
from hashing import *

'''
fuzzy string search api using minhash
'''

app = Flask(__name__)
db = sqlite3.connect("data.db", check_same_thread=False)

# optimized threshold, but adjustable per request
DEFAULT_THRESHOLD = 0.25

def get_values_from_db(h):
	# get values from hash
	cursor = db.cursor()
	cursor.execute("SELECT value FROM hash WHERE hash = ?", (h,))
	return [x[0] for x in cursor.fetchall()]

@app.route('/search', methods=["GET","POST"])
def search():
	params = request.args
	if request.method == "POST":
		params = request.form

	query = params.get('q')
	if query == None:
		return "no query", 400

	threshold = params.get('threshold') # adjustable, 0-1
	
	if threshold != None and threshold != '':
		threshold = float(threshold)
		if threshold > 1 or threshold < 0:
			return "bad threshold, should be between 0 and 1 (e.g. 0.2)", 400
	else:
		threshold = DEFAULT_THRESHOLD

	hashvals = get_hashes(query)
	# print('hashvals:', hashvals)
	matches = []
	# for each value, find all similar value in the db (each function would be O(64) for 64 hash lookups)
	hashcounts = {}
	for h in hashvals:
		results = get_values_from_db(h)
		# print(f'h: {h}, results: {results}')
		for r in results:
			if r not in hashcounts:
				hashcounts[r] = 0
			hashcounts[r] += 1

	for match in hashcounts:
		score = hashcounts[match] / MINHASH_PERMS
		print(f"score: {score}, match: {match}")
		if score >= threshold:
			matches.append(match)

	return jsonify(matches)




@app.route("/")
def index():
	return '''
	<form action=search>
	query: <input name=q>
	<br>
	thresohold (optional): <input name=threshold placeholder=0.7 value=0.7>
	<input type=submit>
	</form>
	'''


if __name__ == '__main__':
	app.run()