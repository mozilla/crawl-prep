from __future__ import absolute_import

import json
import os

import depth_n_link_following_crawl.upstream.domain_utils as du

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

jsonfile = open(os.path.join(DATA_DIR, 'internal_links.json'))
jsonstr = jsonfile.read()
jsondata = json.loads(jsonstr)

finaltld = {}


def parse(string):
    return string.split("/")[2]

    # for other understanding of TLD+1, use the below return function
    # return "".join([str.split("/")[2], "/", str.split("/")[3]])
result = {}
frequency_dict = {}
for i in range(len(jsondata)):
    for j in jsondata[i][1]:
        if j.startswith("http") and "://" in j:
            tld = du.get_ps_plus_1(j)
            if tld in result:
                result[tld] += 1
            else:
                result[tld] = 1
for key in result:
    if result[key] in frequency_dict:
        frequency_dict[result[key]] += 1
    else:
        frequency_dict[result[key]] = 1
print(result)
print(len(result))
