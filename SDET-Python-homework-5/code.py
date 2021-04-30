import gzip
import json
import os
import sys
import re
from collections import Counter
import argparse



lineformat = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST|HEAD|PUT) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)
urls = []
error = []
error_5xx = []
logfile = open("access.log")
out_file = open("result.txt", "w")
line_count = 0
get_count = 0
post_count = 0
head_count = 0
put_count = 0
for l in logfile.readlines():
    data = re.search(lineformat, l)
    if data:
        line_count += 1
        datadict = data.groupdict()
        ip = datadict["ipaddress"]
        datetimestring = datadict["dateandtime"]
        url = datadict["url"]
        urls.append(url)
        bytessent = datadict["bytessent"]
        referrer = datadict["refferer"]
        useragent = datadict["useragent"]
        status = datadict["statuscode"]
        method = data.group(6)
        find = re.findall(r"[4][0-9][0-9]", status)
        find_5xx = re.findall(r"[5][0-9][0-9]", status)
        if len(find) > 0:
            error.append([url, status, int(bytessent), ip])
        if len(find_5xx) > 0:
            error_5xx.append(ip)
        if (method.__contains__('GET')):
            get_count += 1
        elif (method.__contains__("POST")):
            post_count += 1
        elif (method.__contains__("HEAD")):
            head_count += 1
        elif (method.__contains__("PUT")):
            put_count += 1
        #print( ip,datetimestring,url,bytessent,referrer,useragent,status,method)
logfile.close()
out_file.write("String count\n")
out_file.write(str(line_count) + "\n")
out_file.write("GET count\n")
out_file.write(str(get_count) + "\n")
out_file.write("POST count\n")
out_file.write(str(post_count) + "\n")
out_file.write("HEAD count\n")
out_file.write(str(head_count) + "\n")
out_file.write("PUT count\n")
out_file.write(str(put_count) + "\n")
top_10 = (Counter(urls).most_common(10))
out_file.write("TOP 10 URLS\n")
for i in range(10):
    out_file.write(str(i+1) + " position\n")
    out_file.write("URL = " + str(top_10[i][0]) + "\n")
    out_file.write("COUNT = " + str(top_10[i][1]) + "\n")
error.sort(key = lambda x: x[2], reverse=True)
out_file.write("TOP 5 4XX\n")
for i in range(5):
    out_file.write(str(i+1) + " position\n")
    out_file.write("URL = " + str(error[i][0]) + "\n")
    out_file.write("CODE = " + str(error[i][1]) + "\n")
    out_file.write("SIZE = " + str(error[i][2]) + "\n")
    out_file.write("IP = " + str(error[i][3]) + "\n")
out_file.write("TOP 5 5XX\n")
top_5 = (Counter(error_5xx).most_common(5))
for i in range(5):
    out_file.write(str(i+1) + " position\n")
    out_file.write("IP = " + str(top_5[i][0]) + "\n")
    out_file.write("COUNT = " + str(top_5[i][1]) + "\n")
out_file.close()




parser = argparse.ArgumentParser(description="--json on")
parser.add_argument('--json', default=False, required=False)
args = parser.parse_args()

if args.json:
    data_json = {}
    data_json['count'] = []
    data_json['count'].append({
        'all': line_count,
        'post': post_count,
        'get': get_count,
        'put': put_count,
        'head': head_count,
    })
    data_json['top10url'] = []
    for i in range(10):
        data_json['top10url'].append({
         top_10[i][0] : top_10[i][1]
     })
    data_json['5top4xx'] = []
    for i in range(5):
        data_json['5top4xx'].append({
        'url' : error[i][0],
        'code' : error[i][1],
        'size' : error[i][2],
        'ip' : error[i][3]
        })
    data_json['5top5xx'] = []
    for i in range(5):
        data_json['5top4xx'].append({
            'ip': top_5[i][0],
            'count': top_5[i][1]
        })

    with open('result.json', 'w') as json_file:
        json.dump(data_json, json_file)