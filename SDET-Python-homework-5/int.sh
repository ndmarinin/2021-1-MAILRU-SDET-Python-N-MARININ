#!/bin/bash

# variables
LOGFILE="access.log"
> res.txt


# functions
filters_5xx(){
awk '$9 ~ /5[0-9][0-9]/'
}


request_ips(){
awk '{print $1}'
}

request_method(){
awk '{print $6}' \
| cut -d'"' -f2
}

request_pages(){
awk '{print $7}'
}

wordcount(){
sort \
| uniq -c
}


sort_desc(){
sort -rn
}

return_kv(){
awk '{print $1, $2}'
}

request_pages(){
awk '{print $7}'
}

return_top_ten(){
head -10
}

return_top_five(){
head -5
}


## actions

get_count(){
echo "Line count" >>  res.txt
wc -l $LOGFILE >>  res.txt
}

get_request_ips(){
echo ""
echo "Top 5 CODE 5XX IP's:" >>  res.txt

cat $LOGFILE \
| filters_5xx \
| request_ips \
| wordcount \
| sort_desc \
| return_kv \
| return_top_ten >>  res.txt
echo ""
}

get_request_methods(){
echo "Top Request Methods:" >>  res.txt
cat $LOGFILE \
| request_method \
| wordcount \
| return_kv >>  res.txt
echo ""
}

get_request_pages_4xx(){
echo "Top 5: 4XX Page Responses:" >>  res.txt
cat $LOGFILE | awk '$9 ~ /4[0-9][0-9]/' | awk '{print $7, $9, $10, $1}'  | sort -k 3 -rn | head -5 | uniq >>  res.txt
echo ""
}

get_request_pages(){
echo "Top 10 Request Pages:" >>  res.txt
cat $LOGFILE \
| request_pages \
| wordcount \
| sort_desc \
| return_kv \
| return_top_ten >>  res.txt
echo ""
}


# executing
get_count
get_request_methods
get_request_pages
get_request_ips
get_request_pages_4xx