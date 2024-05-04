#!/usr/bin/env python3

import sqlite3
import sys
from hashing import *
'''
take each line in the data file, tokenize it and index it in a database
'''

db = sqlite3.connect("data.db")
gcursor = db.cursor()
gcursor.execute("CREATE TABLE IF NOT EXISTS hash (hash INTEGER, value TEXT, PRIMARY KEY (hash,value)) ")

if len(sys.argv) < 2:
	print("usage: %s <text file to index>"%sys.argv[0])
	exit(1)

datfile = sys.argv[1]

with open(datfile,'r') as f:
	for line in f:
		line = line.strip()
		cursor = db.cursor()
		hashvals = get_hashes(line)
		for i in hashvals:
			cursor.execute("INSERT OR IGNORE INTO hash VALUES (?,?)", (int(i), line))
		db.commit()


