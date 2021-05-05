import re
from collections import Counter

class Make_data:
    urls = []
    error = []
    error_5xx = []
    line_count = 0
    get_count = 0
    post_count = 0
    head_count = 0
    put_count = 0
    top5 = []
    top10 = []


    def print_5xx(self):
        result = []
        for i in range(5):
            result.append([str(self.top_5[i][0]), int(self.top_5[i][1])])
            print(str(self.top_5[i][0]), int(self.top_5[i][1]))
        return result

    def print_4xx(self):
        result = []
        for i in range(5):
            result.append([str(self.error[i][0]), int(self.error[i][1]), int(self.error[i][2]), str(self.error[i][3])])
        return result

    def print_top10(self):
        result = []
        for i in range(10):
            result.append([str(self.top_10[i][0]), int(self.top_10[i][1])])
        return result

    def print_method(self):
        result = []
        result.append(["GET", int(self.get_count)])
        result.append(["POST", int(self.post_count)])
        result.append(["HEAD", int(self.head_count)])
        result.append(["PUT", int(self.put_count)])
        return result

    def print_count(self):
        result = self.line_count
        return result

    def analyze(self):
        lineformat = re.compile(
            r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST|HEAD|PUT) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""",
            re.IGNORECASE)
        logfile = open("access.log")
        out_file = open("result.txt", "w")

        for l in logfile.readlines():
            data = re.search(lineformat, l)
            if data:
                self.line_count += 1
                datadict = data.groupdict()
                ip = datadict["ipaddress"]
                datetimestring = datadict["dateandtime"]
                url = datadict["url"]
                self.urls.append(url)
                bytessent = datadict["bytessent"]
                referrer = datadict["refferer"]
                useragent = datadict["useragent"]
                status = datadict["statuscode"]
                method = data.group(6)
                find = re.findall(r"[4][0-9][0-9]", status)
                find_5xx = re.findall(r"[5][0-9][0-9]", status)
                if len(find) > 0:
                    self.error.append([str(url), int(status), int(bytessent), str(ip)])
                if len(find_5xx) > 0:
                    self.error_5xx.append(ip)
                if (method.__contains__('GET')):
                    self.get_count += 1
                elif (method.__contains__("POST")):
                    self.post_count += 1
                elif (method.__contains__("HEAD")):
                    self.head_count += 1
                elif (method.__contains__("PUT")):
                    self.put_count += 1
                # print( ip,datetimestring,url,bytessent,referrer,useragent,status,method)
        logfile.close()

        self.top_10 = (Counter(self.urls).most_common(10))
        self.error.sort(key=lambda x: x[2], reverse=True)
        self.top_5 = (Counter(self.error_5xx).most_common(5))






