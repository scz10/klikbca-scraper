# klikbca-scraper
Python class for scraping klikbca (mobile version)

## How to install
**package used : requests, beautifulsoup4, lxml <br>**

Install require package :  

    pip install -r requirements.txt 

---
## How to use
### ***Login***
Use username and password your klikbca account

    from bca import BCAScrape

    obj = BCAScrape('USERNAME','PASSWORD')
    obj.login()
---
### ***Get balance***
Use this function to get
1. Account Number
2. Account Currency
3. Account Balance 

Note : before call ***getSaldo*** function, make sure to ***login*** first

    acct = obj.getSaldo() 

Output array will be like this

    [
        [
            "741065XXXX",   # account number
            "IDR",          # currency
            "680,xxx.xx"    # balance
        ]
    ]

To access your ***first*** account number you can access the array like this

    acct[0][0]

---
### ***Get account statement***
Use this function to get list transaction based on period of time
with specification
1. Account statement information is only available for the past 31 days

2. Account statement information Period statement can be selected within 7 days.

<br>

`getMutasiRek(startDt, endDt, flow=None, mode=None, indexRek="0")`


<br>

    startDt (str), Start statement date "%d/%m/%Y". e.g: "18/10/2019"

    endDt (str), End statement date "%d/%m/%Y". e.g: "18/10/2019"

    flow (str), To filter transaction data result by cash flow. e.g: Filter by credit use "CR" or debit use "DB", all use None the default is None

    mode (int), To change format result data, e.g: Use 1 to get result data only for transaction , or None to get all data including starting balance and final balance, the default is None

    indexRek (str), To select another account number in your account, if you have only 1 account number, please dont change this 

Note : before call ***getMutasiRek*** function, make sure to ***login*** first.

---
***Example :*** 

Let say you want get account statement 

from ***18 November 2019*** to ***21 November 2019***

then you can call this function like this

    statement = obj.getMutasiRek("18/11/2019","21/11/2019") 

Statement output will be like this

    [
        "7410XXXXXX",                   # account number
        "18/11/2019 - 21/11/2019",      # statement period
        "IDR",                          # currency
        [
            [
                "18/11",                # transaction date
                "SWITCHING CR      ",   # transaction type from other bank using "SWTICHING"
                "TRANSFER   DR 013 ",   # from bank code 013
                "XXXX NAME",            # sender name
                "XXX LOCATION",         # transfer location 
                "0998",                 # branch code (?)
                "106,819.00",           # nominal transaction
                "CR"                    # cash flow
            ],
            [
                "18/11",
                "SWITCHING DB      ",
                "TRANSFER   KE 009 ",
                "XXXX NAME",
                "XXX LOCATION",
                "0998",
                "358,819.00",
                "DB"
            ],
            [
                "18/11",
                "BIAYA ADM         ", # admin fee from bank
                "0000",
                "17,000.00",
                "DB"
            ],
            [
                "21/11",
                "TRSF E-BANKING DB ",   # "TRSF E-BANKING" mean it come from same bank transaction
                "2110/FTFVA/WS95031",   # description
                "12208/SHOPEEPAY   ",   # destination account
                "-                 ",
                "-                 ",
                "128XXXXXXX",           
                "0000",
                "26,000.00",
                "DB"
            ],
            [
                "21/11",
                "TRSF E-BANKING CR ",
                "21/10 95031",
                "XXX NAME SENDER",
                "0998",
                "72,115.00",
                "CR"
            ]
        ],
        "764,952.00",   # starting balance period based
        "178.934.00",   # total credit statement
        "375,819.00",   # total debit statement
        "568,067.00"    # final balance period based
    ]


To access the output you can access the array like this

    mutasi[0]       # to get account number
    mutasi[3][0]    # to get first transaction data

---

***Example 2 :*** 

you can also filter the transaction data by cash flow and format it with only transaction data to result by using option ***flow*** and ***mode***

    statement = obj.getMutasiRek("18/11/2019","21/11/2019",flow="CR",mode=1)

And the output will be like this

    [
        [
            "18/11",
            "SWITCHING CR      ",
            "XXXX NAME SENDER",
            "106,819.00",
            "CR"
        ],
        [
            "21/11",
            "TRSF E-BANKING CR ",
            "XXX NAME SENDER"
            "72,115.00",
            "CR"
        ]
    ]

---

### ***Check if transaction exist based on transfer amount***

`isTransactionExist(nominal,startDt=None, endDt=None)`

<br>
Use this function to check are the transaction exist based on transfer amount,  it will check only for transaction type

***"TRSF E-BANKING CR"*** or ***"SWITCHING CR"***

That mean it will check incoming transfer between account (same bank) or between bank only

    nominal (int), transfer nominal to be check. e.g: 102132 // 102.132

    startDt (optional) (str), Start date based check transfer using format "%d/%m/%Y". e.g: "18/11/2019" // 18 November 2019

    endDt (optional) (str), End date based check transfer using format "%d/%m/%Y". e.g: "20/11/2019" // 20 November 2019

    by default if you dont fill the startDt and endDt
    the startDt and endDt will be today

***Example :***

Lets say you want to check is there any transaction with transfer amount ***72.115 Rupiah*** from today transaction

    exist,data = obj.isTransactionExist(72115)

Or if you want specify the date from **18 Oct 2019** to **20 Oct 2019**

    exist,data = obj.isTransactionExist(72115,"18/10/2019","21/10/2019")

It will return tuple

From example above the ***exist*** will return **True** if transaction data exist 
or **False** if transaction data not exist

And ***data*** will return as list fill with transaction data if the transaction exist

data:

    [
        [
            "21/10",
            "TRSF E-BANKING CR ",
            "XXX NAME SENDER"
            "72,115.00",
            "CR"
        ]
    ]

---
### ***Logout***
This function to logout your account from the session.<br>
you need to ***logout*** everytime you want to exit the code<br>
or it will make you cant login for 10 minutes

    obj.logout()
