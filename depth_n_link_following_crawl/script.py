import json
import os
import pickle

import matplotlib.pyplot as plt

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

jsonfile = open(os.path.join(DATA_DIR, 'internal_links.json'))
jsonstr = jsonfile.read()
jsondata = json.loads(jsonstr)

finaltld = {}


def parse(string):
    return string.split("/")[2]
    # for other understanding of TLD+1, use the below return function
    # return "".join([str.split("/")[2], "/", str.split("/")[3]])


for i in range(len(jsondata)):
    for j in jsondata[i][1]:
        if j.startswith("http") and "://" in j:
            tld = parse(j)
            finaltld[tld] = finaltld.get(tld, 0) + 1

sort = sorted(finaltld.items())
x, y = list(zip(*sort))

xvals = list(range(len(x)))

plt.figure(figsize=(20, 10))
plt.xticks(xvals, x, rotation="vertical")
plt.plot(xvals, y)
# plt.show()
plt.savefig('data/plot.png')

savefile = open("data/dict.pkl", "wb")
pickle.dump(finaltld, savefile)
savefile.close()
