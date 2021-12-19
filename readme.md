# klikbca-scraper
Python class for scraping klikbca

## How to install


Install require package :  
```shell
pip install -r requirements.txt 
```
---
## How to use
### ***Login***
Use username and password your klikbca account
```python
from klikbca.parser import KlikBCAParser

parser = KlikBCAParser("username", "pin")
parser.login()
```
### ***Get balance***
Use this function to get
1. Account Number
2. Account Type
3. Account Currency
4. Account Balance 


Note : before call ***check_balance*** function, make sure to ***login*** first
```python
from klikbca.parser import KlikBCAParser

parser = KlikBCAParser("username", "pin")
parser.login()

balance = parser.check_balance()


```

Output variable balance will be like this
```json
[
  [
    "Account No.",
    "Account Type",
    "Currency",
    "Available Balance"
  ],
  [
    "XXXXXX",
    "Tabungan",
    "IDR",
    "XXX,XXX,XXX.18"
  ]
]
```

### ***Get account statement***
Use this function to get list transaction based on period of time
with specification

1. Account statement information is only available for the past 31 days
2. For monthly statements, you can access the last 2 months


<br>

    start_date (str), Start statement date "%d/%m/%Y". e.g: "17/12/2021"

    end_date (str), End statement date "%d/%m/%Y". e.g: "21/12/2021"

    by default daily statement was Today date, for monthyl statement you need to specify the Month name. 


---
***Example :*** 

Let say you want get account statement 

from ***17 Desember 2021*** to ***20 Desember 2021***

then you can call this function like this

```python
from klikbca.parser import KlikBCAParser
import json

parser = KlikBCAParser("username", "pin")
parser.login()

statements = parser.daily_statements("17/12/2021", "20/12/2021")

```

Statement output will be like this

```json
[
    [
        [
            "Account Number",
            "Name",
            "Period",
            "Currency"
        ],
        [
            "XXXXXXX",
            "XXXXXXX",
            "17/12/2021 - 20/12/2021",
            "IDR"
        ]
    ],
    [
        [
            "Date",
            "Description",
            "Branch",
            "Amount",
            "Balance"
        ],
        [
            [
                "15/12", // DATE
                "XXXXX", // DETAIL TRANSFER
                "0XXXX", // BRANCH CODE
                "10,000,000.00", // AMOUNT
                "CR",           // FLOW
                "12,843,128.18" // ENDING BALANCE AFTER TRANSACTION
            ],
            [
                ......
            ]
        ]
    ],
    [
        [
            "Starting Balance",
            "Total Credits",
            "Total Debits",
            "Ending Balance"
        ],
        [
            "XXXXX",
            "XXXX",
            "XXXX",
            "XXXX"
        ]
    ]
]
```


***Example 2 :*** 

let say you want to get monthly statement for November 2021 ( Last month in this case)

```python
from klikbca.parser import KlikBCAParser
import json

parser = KlikBCAParser("username", "pin")
parser.login()

statements = parser.monthly_statements("November")
```

and then the output will be the same as example 1


### ***Logout***
This function to logout your account from the session.<br>
you need to ***logout*** everytime you want to exit the code<br>
or it will make you cant login for 5 minutes

```python
from klikbca.parser import KlikBCAParser
import json

parser = KlikBCAParser("username", "pin")
parser.login()

statements = parser.daily_statements("17/12/2021", "20/12/2021")

parser.logout()
```
