class HEADERS:


    def headers_auth(self):
        return {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Origin': 'https://target.my.com',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://target.my.com/'}

    def headers_create_campagin(self):
        return {'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': self.csrf_token,
                'X-Campaign-Create-Action': 'new',
                'Origin': 'https://target.my.com',
                'Accept-Language': 'ru',
                'Referer': 'https://target.my.com/campaign/new'}

    def headers_delete_campagin(self):
        return {'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Accept': '*/*',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': self.csrf_token,
                'Origin': 'https://target.my.com',
                'Accept-Language': 'ru',
                'Referer': 'https://target.my.com/dashboard',
                }

    def headers_create_segment(self):
        return {'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': self.csrf_token,
                'Origin': 'https://target.my.com',
                'Accept-Language': 'ru',
                'Referer': 'https://target.my.com/segments/segments_list/new',
                }

    def headers_delete_segment(self):
        return {'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Accept': '*/*',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': self.csrf_token,
                'Origin': 'https://target.my.com',
                'Accept-Language': 'ru',
                'Referer': 'https://target.my.com/segments/segments_list',
                }
