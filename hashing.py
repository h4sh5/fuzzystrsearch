from datasketch import MinHash, LeanMinHash

# rolling window length
# e.g.
#  >>> chunkstring('hello world',4)
# ['hell', 'o wo', 'rld']
W = 4
MINHASH_PERMS = 64 # the bigger this is, the more hashes are generated per string, too big values no longer improve accuracy

def chunkstring(string, length):
	string = string.lower()
	return list((string[0+i:length+i] for i in range(0, len(string), length)))


def tokenize(string):
	# tokenize a string and return chunks
	return chunkstring(string,W)

def get_hashes(string):
	tokens = tokenize(string)
	m = MinHash(num_perm=MINHASH_PERMS)
	for t in tokens:
		m.update(t.encode('utf8'))

	lm = LeanMinHash(m)
	hashvals = [int(x) for x in lm.hashvalues]

	return hashvals
