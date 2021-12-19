import requests
from bs4 import BeautifulSoup
import datetime


class KlikBCAParser:
    def __init__(self, user_id, password):
        self.s = requests.Session()

        self.url = {
            "login_url": "https://ibank.klikbca.com/authentication.do",
            "logout_url": "https://ibank.klikbca.com/authentication.do?value(actions)=logout",
            "check_balance": "https://ibank.klikbca.com/balanceinquiry.do",
            "statement_acct" : "https://ibank.klikbca.com/accountstmt.do?value(actions)=acctstmtview"
        }
        self.user_id = user_id
        self.password = password
        self.ip_address = None
        self.login_status = False


        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://ibank.klikbca.com',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://ibank.klikbca.com/',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8'
        }

    def _get_ip_address(self):
        r = self.s.get('https://httpbin.org/ip')
        self.ip_address = r.json()['origin']

    def login(self):
        self._get_ip_address()
        payloads = {
            'value(user_id)': self.user_id,
            'value(pswd)': self.password,
            'value(Submit)': 'LOGIN',
            'value(actions)': 'login',
            'value(user_ip)': self.ip_address,
            'value(mobile)': 'false',
            'value(browser_info)': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        }

        self.s.post(url=self.url['login_url'], headers=self.headers, data=payloads)
        r = self.s.get('https://ibank.klikbca.com/authentication.do?value(actions)=welcome')
        
        try:
            soup = BeautifulSoup(r.content, 'html.parser')
            name = soup.find('font', {'face':'Verdana, Arial, Helvetica, sans-serif','size' : 3, 'color':'#000099'}).text

            if len(name):
                self.login_status = True

        except Exception as e:
            self.logout()
            raise SyntaxError('Login failed')

    def check_balance(self):
        if not self.login_status:
            raise SyntaxError('Please login first')

        r = self.s.post(url=self.url['check_balance'])
        try:
            soup = BeautifulSoup(r.content, 'html.parser')
            tables = soup.find_all('font', {'face':'Verdana', 'size': 2, 'color' : '#0000bb'})
            acct_list = []
            acct_content = []
            x = 1
            for table in tables:
                if table.text.strip() == '':
                    continue
                if x%4 == 0:
                    acct_content.append(table.text.strip())
                    acct_list.append(acct_content)
                    acct_content = []
                    x += 1
                else:
                    acct_content.append(table.text.strip())
                    x += 1

            return acct_list

        except Exception as e:
            self.logout()
            print(e)
            exit(1)
    
    def daily_statements(self, start_date=datetime.datetime.now().strftime('%d/%m/%Y'), end_date=datetime.datetime.now().strftime('%d/%m/%Y')):
        if not self.login_status:
            raise SyntaxError('Please login first')

        if self._check_date(start_date, end_date):
            
            start_date = start_date.split('/')
            end_date = end_date.split('/')
            payloads = {
                'value(D1)': 0,
                'value(r1)': 1,
                'value(startDt)': start_date[0],
                'value(startMt)': start_date[1],
                'value(startYr)': start_date[2],
                'value(endDt)': end_date[0],
                'value(endMt)': end_date[1],
                'value(endYr)': end_date[2],
                'value(fDt)' : '',
                'value(tDt)': '',
                'value(submit1)': 'View Account Statement'
            }

            r = self.s.post(url=self.url['statement_acct'], headers=self.headers, data=payloads)

            return self._get_statements_data(r.content)

    def monthly_statements(self, month_name):
        if not self.login_status:
            raise SyntaxError('Please login first')

        ok, fdt, tdt, x = self._check_month(month_name)
        if ok:
            payloads = {
                'value(D1)': 0,
                'value(r1)': 2,
                'value(x)': x,
                'value(fDt)' : fdt,
                'value(tDt)': tdt,
                'value(submit1)': 'View Account Statement'
            }

            r = self.s.post(url=self.url['statement_acct'], headers=self.headers, data=payloads)

            return self._get_statements_data(r.content)
    
    def _check_month(self, month_name):
        today = datetime.date.today()
        first_last_month = today.replace(day=1)
        last_month = first_last_month - datetime.timedelta(days=1)
        first_two_last_month = last_month.replace(day=1)
        last_two_month = first_two_last_month - datetime.timedelta(days=1)

        if month_name == last_month.strftime("%B"):
            return True, '01'+last_month.strftime("%m"),last_month.strftime("%d")+last_month.strftime("%m"), 1
        elif month_name == last_two_month.strftime("%B"):
            return True, '01'+last_two_month.strftime("%m"), last_two_month.strftime("%d")+last_two_month.strftime("%m"), 2 
        else:
            self.logout()
            raise SyntaxError('Month not exist, only the last two month allowed')
            
    def _check_date(self, start_date, end_date):
        try:
            start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y').date()
            end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y').date()
            date_now = datetime.datetime.now().date()
            max_start_date = date_now - datetime.timedelta(31)
            if start_date >= max_start_date and start_date <= date_now and end_date <= date_now and end_date >= start_date:
               return True
            else:
                return False
        except Exception as e:
            self.logout()
            print(e)
            exit(1)

    def _get_statements_data(self, respond_content):
        try:
            data = []
            col_name = []
            col_data = []
            soup = BeautifulSoup(respond_content, 'html.parser')
            # Top content
            top = []
            
            table = soup.find('table', {'border':"0", 'width':"90%", 'cellpadding': "0", 'cellspacing': "0", 'bordercolor':'#f0f0f0'})
            rows = table.find_all('tr')
            for row in rows:
                if row.text.strip() == '':
                    continue
                cols = row.find_all('td')
                x = 1
                
                for ele in cols:
                    if x==1:
                        col_name.append(ele.text.strip())
                        x+=1
                    elif x==3:
                        col_data.append(ele.text.strip())
                    else:
                        x+=1
            top.append(col_name)
            top.append(col_data)
            col_name = []
            col_data = []
            # Mid content
            mid = []
            table = soup.find('table', {'border':"1", 'width':"100%", 'cellpadding': "0", 'cellspacing': "0", 'bordercolor':'#ffffff'})
            rows = table.find_all('tr')
            first = True
            for row in rows:
                
                if row.text.strip() == '':
                    continue
                cols = row.find_all('td')
                if first:
                    col_name = [ele.text.strip() for ele in cols]
                    first = False
                else:
                    col_data.append([ele.text.strip() for ele in cols])
                
            mid.append(col_name)
            mid.append(col_data)
            col_name = []
            col_data = []
            # Bottom content
            bot = []
            table = soup.find('table', {'border':"0", 'width':"70%", 'cellpadding': "0", 'cellspacing': "0", 'bordercolor':'#ffffff'})
            rows = table.find_all('tr')
            for row in rows:
                if row.text.strip() == '':
                    continue
                cols = row.find_all('td')
                x = 1
                
                for ele in cols:
                    if x==1:
                        col_name.append(ele.text.strip())
                        x+=1
                    elif x==3:
                        col_data.append(ele.text.strip())
                    else:
                        x+=1
            bot.append(col_name)
            bot.append(col_data)
            data.append(top)
            data.append(mid)
            data.append(bot)
            return data


        except Exception as e:
            self.logout()
            print(e)
            exit(1)

    def logout(self):
        self.s.post(self.url['logout_url'])

