from collections import defaultdict

def loadBigrams():
	d = defaultdict(list)
	with open('data/count_2w.txt', 'r') as f:
		for line in f:
			split = line.split()
			d[split[0]].append((split[1], split[2]))

	print d["12th"];
	return d;
	