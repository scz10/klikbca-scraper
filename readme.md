# klikbca-scraper
python class for scraping klikbca

## How to install
**package used : requests, beautifulsoup4, lxml <br>**

Install require package :  

    pip install -r requirements.txt 

---
## How to use
### ***Login***
Use username and password your klikbca account

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
### ***Get account mutation***
Use this function to get list transaction based on period of time
with specification
1. Account statement information is only available for the past 31 days

2. Account statement information Period statement can be selected within 7 days.

`getMutasiRek(startDt, endDt, indexRek="0")`

Note : before call ***getMutasiRek*** function, make sure to ***login*** first.

Example : 

Let say you want get account mutation 

from ***13 November 2019*** to ***16 November 2019***

then you can call this function like this

    mutasi = obj.getMutasiRek("13/11/2019","16/11/2019") 

Output array will be like this

    [
        "7410XXXXXX",                   # your account number
        "13/11/2019 - 18/11/2019",      # statement period
        "IDR",                          # currency
        [
            [
                "13/11",                # transaction date
                "TRSF E-BANKING DB ",   # transfer method  
                "1311/FTFVA/XXXXXXX",   
                "70001/GO-PAY CUSTO",   # VA / bank 
                "-                 ",
                "-                 ",
                "081288XXXXXX",         # account number
                "0000",                 # branch code (?)
                "51,000.00",            # nominal
                "DB"                    # flow
            ],
            [
                "13/11",
                "TRSF E-BANKING DB ",
                "1311/FTFVA/XXXXXXX",
                "12208/SHOPEEPAY   ",
                "-                 ",
                "-                 ",
                "1288XXXXXX",
                "0000",
                "10,000.00",
                "DB"
            ],
            [
                "15/11",
                "BIAYA ADM         ",    #adm fee from bank
                "0000",
                "17,000.00",
                "DB"
            ],
            [
                "18/11",
                "TRSF E-BANKING DB ",
                "1711/FTFVA/XXXXXX",
                "39358/OVO         ",
                "-                 ",
                "-                 ",
                "08XXXXXXXX",
                "0000",
                "200,000.00",
                "DB"
            ]
        ],
        "1,126,XXX.XX",    # starting balance period based
        "0.00",            # total credit statement
        "278,000.00",      # total debit statement
        "848,XXX.XX"       # final balance period based
    ]
    
To access the output you can access the array like this

    mutasi[0]       # to get account number
    mutasi[3][0]    # to get first transaction data
---
### ***Logout***
This function to logout your account from the session.<br>
you need to ***logout*** everytime you want to exit the code<br>
or it will make you cant login for 10 minutes

    obj.logout()

---
## Next update
- Check incoming transfer by transfer value / notes