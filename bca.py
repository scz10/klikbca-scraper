import sys
import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime,timedelta


class BCAScrape:
    username = None
    password = None
    ipAddress = None
    statusLogin = False
    url = {
        "loginUrl": "https://m.klikbca.com/login.jsp",
        "loginAction": "https://m.klikbca.com/authentication.do",
        "logoutAction": "https://m.klikbca.com/authentication.do?value(actions)=logout",
        "cekSaldoUrl": "https://m.klikbca.com/balanceinquiry.do"
    }
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
        self.s.post(url=self.url["loginAction"], headers=self.headers, data=self.data)
        self.statusLogin = True

    def getSaldo(self):
        self.s.headers.update({'Referer': self.url["loginAction"]})
        self.s.post('https://m.klikbca.com/accountstmt.do?value(actions)=menu')
        self.s.headers.update(
            {'Referer': 'https://m.klikbca.com/accountstmt.do?value(actions)=menu'})
        r = self.s.post(self.url["cekSaldoUrl"])
        if r.status_code == 302:
            self.logout()
            print("Please login first, or check your username or password \n SystemExit(1)")
            sys.exit(1)
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

    def getMutasiRek(self, startDt, endDt, flow=None, mode=None , indexRek="0"):
        try:
            date_format = "%d/%m/%Y"
            a = datetime.strptime(startDt, date_format)
            b = datetime.strptime(endDt, date_format)
            if ((a > b) or ((b - a).days > 7) or ((datetime.today() - a).days > 31)):
                print("ERROR!! Please check your input, and make sure \n\nStart date cant be greater than End date \nStatement information is only available for max the past 31 days. \nPeriod statement can be selected within 7 days.")
                self.logout()
                sys.exit(1)
            if (int(mode) != 1 and mode != None):
                print("Please input Mode option with 1 for Simple Mode, or leave it blank(None) for full mode")
                self.logout()
                sys.exit(1)
            if (str(flow).upper() != "CR" and str(flow).upper() != "DB" and flow != None):
                print("Please input Flow option with 'CR', 'DB' or leave it blank(None) to get both flow")
                self.logout()
                sys.exit(1)
            startDt = startDt.split("/")
            endDt = endDt.split("/")
            self.s.headers.update(
                {'Referer': 'https://m.klikbca.com/accountstmt.do?value(actions)=menu'})
            self.s.post(
                'https://m.klikbca.com/accountstmt.do?value(actions)=acct_stmt')
            self.s.headers.update(
                {'Referer': 'https://m.klikbca.com/accountstmt.do?value(actions)=acct_stmt'})
            data = {
                'r1': '1',
                'value(D1)': str(indexRek),  # index rekening default 0
                'value(startDt)': startDt[0],
                'value(startMt)': startDt[1],
                'value(startYr)': startDt[2],
                'value(endDt)': endDt[0],
                'value(endMt)': endDt[1],
                'value(endYr)': endDt[2]
            }
            r = self.s.post(
                'https://m.klikbca.com/accountstmt.do?value(actions)=acctstmtview', data=data)
            if r.status_code == 302:
                self.logout()
                print("Please login first, or check your username or password \n SystemExit(1)")
                sys.exit(1)
            # parse and scrape data
            soup = BeautifulSoup(r.text, "lxml")
            mutasiData = []
            listTransaksi = []
            mutasiTbl: Tag = soup.find_all('table')[0].find_all(
                'table')[1].find_all('table')[1].find_all('tr')

            for i in range(1, 5):
                if i == 2:
                    continue
                mutasiData.append(soup.find_all('table')[0].find_all('table')[1].find_all(
                'table')[0].find_all('tr')[i].find_all('td')[2].text)

            for i in range(1,(len(mutasiTbl))):
                trx = soup.find_all('table')[0].find_all('table')[1].find_all('table')[1].find_all('tr')[i].get_text(separator="||").split("||")
                if i == (len(mutasiTbl)-1):
                    del trx[-2:]
                else:
                    del trx[-1]
                if mode == 1:
                    for i in range(1,len(trx)-3):
                        del trx[2]     
                if flow:
                    if trx[-1] == str(flow.upper()):
                        listTransaksi.append(trx)
                else:
                    listTransaksi.append(trx)
            mutasiData.append(listTransaksi)

            for i in range(3, 13, 3):
                mutasiData.append(soup.find_all('table')[0].find_all('table')[
                              1].find_all('table')[2].find_all('td')[i].text)

            if mode == 1:
                return listTransaksi
            else:
                return mutasiData

        except ValueError as exc:
            print(exc)
            self.logout()
            sys.exit(1)
    
    def isTransactionExist(self,nominal,startDt=None, endDt=None):
        try:
            nominal = '{:20,.2f}'.format(int(nominal))
            if (startDt == None and endDt == None):
                startDt = datetime.strftime(datetime.now() - timedelta(1), "%d/%m/%Y")
                endDt = datetime.strftime(datetime.now(), "%d/%m/%Y")

            isExist = self.getMutasiRek(startDt,endDt,flow="CR",mode=1)

            for i in range(len(isExist)):
                if (isExist[i][2].strip() == nominal.strip()) and (isExist[i][1].strip() == "SWITCHING CR" or isExist[i][1].strip() == "TRSF E-BANKING CR"):
                    return True

            return False

        except ValueError as exc:
            print(exc)
            self.logout()
            sys.exit(1)
        except TypeError as exc:
            print(exc)
            self.logout()
            sys.exit(1)

    def logout(self):
        self.s.get(
            'https://m.klikbca.com/authentication.do?value(actions)=logout')
        self.statusLogin = False