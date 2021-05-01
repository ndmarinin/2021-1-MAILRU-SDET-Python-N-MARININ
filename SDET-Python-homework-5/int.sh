#!/bin/bash

# variables
LOGFILE="access.log"
> res.txt


## actions

get_count(){
echo "Line count" >>  res.txt
wc -l $LOGFILE >>  res.txt
}

get_request_ips(){
echo ""
echo "Top 5 CODE 5XX IP's:" >>  res.txt
cat $LOGFILE | awk '$9 ~ /5[0-9][0-9]/' | awk '{print $1}' | sort | uniq -c | sort -rn | awk '{print $1, $2}' | head -5 >>  res.txt
echo ""
}

get_request_methods(){
echo "Top Request Methods:" >>  res.txt
cat $LOGFILE | awk '{print $6}' | cut -d'"' -f2 | sort | uniq -c | awk '{print $1, $2}' >>  res.txt
echo ""
}

get_request_pages_4xx(){
echo "Top 5: 4XX Page Responses:" >>  res.txt
cat $LOGFILE | awk '$9 ~ /4[0-9][0-9]/' | awk '{print $7, $9, $10, $1}'  | sort -k 3 -rn | head -5 | uniq >>  res.txt
echo ""
}

get_request_pages(){
echo "Top 10 Request Pages:" >>  res.txt
cat $LOGFILE | awk '{print $7}' | sort | uniq -c | sort -rn | awk '{print $1, $2}' | head -10 >>  res.txt
echo ""
}


# executing
get_count
get_request_methods
get_request_pages
get_request_ips
get_request_pages_4xx