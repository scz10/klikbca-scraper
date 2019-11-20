import requests
from bs4 import BeautifulSoup, Tag

class BCAParses:
    username = None
    password = None
    url = {
        "loginUrl": "https://m.klikbca.com/login.jsp",
        "loginAction": "https://m.klikbca.com/authentication.do",
        "logoutAction": "https://m.klikbca.com/authentication.do?value(actions)=logout",
        "cekSaldoUrl": "https://m.klikbca.com/balanceinquiry.do"
    }
    ipAddress = None
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://m.klikbca.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Referer': 'https://m.klikbca.com/login.jsp',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    }

    data = {
        'value(user_id)': username,
        'value(pswd)': password,
        'value(Submit)': 'LOGIN',
        'value(actions)': 'login',
        'value(user_ip)': ipAddress,
        'user_ip': ipAddress,
        'value(mobile)': 'true',
        'value(browser_info)': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'mobile': 'true'
    }

    # parameterized constructor

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.ipAddress = BeautifulSoup(requests.get(
            'http://myip.dnsomatic.com/').text, "html.parser").text

    def login(self):
        self.data['value(user_id)'] = self.username
        self.data['value(pswd)'] = self.password
        self.data['value(user_ip)'] = self.ipAddress
        self.data['user_ip'] = self.ipAddress
        self.s = requests.Session()
        self.s.post(url=self.url["loginAction"],
                    headers=self.headers, data=self.data)

    def getSaldo(self):
        self.s.headers.update({'Referer': self.url["loginAction"]})
        self.s.post('https://m.klikbca.com/accountstmt.do?value(actions)=menu')
        self.s.headers.update(
            {'Referer': 'https://m.klikbca.com/accountstmt.do?value(actions)=menu'})
        r = self.s.post(self.url["cekSaldoUrl"])
        soup = BeautifulSoup(r.text, "html.parser")
        rekList = []
        rek = []
        for i in range(2, len(soup.find_all('table')[0].find_all('table')[1].find_all('font')), 3):
            for x in range(3):
                rek.append((soup.find_all('table')[0].find_all('table')[
                           1].find_all('font')[i + x].text).strip())
                if x == 2:
                    rekList.append(rek)
                    rek = []
        return rekList

    def logout(self):
        self.s.get(
            'https://m.klikbca.com/authentication.do?value(actions)=logout')
