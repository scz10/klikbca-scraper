# klikbca-scraper
python class for scraping klikbca

## How to install
**package used : requests, beautifulsoup4, lxml <br>**

Install require package :  
>   `pip install -r requirements.txt `
---
## How to use
### ***Login***
Use username and password your klikbca account

    obj = BCAParses('USERNAME','PASSWORD')
    obj.login()
---
### ***Get balance***
Use this function to get
1. Account Number
2. Account Currency
3. Account Balance 

Note : before call ***getSaldo*** function, make sure to login first

    acct = obj.getSaldo() 

Output array will be like this

    [
        [
            "741065XXXX",   # account number
            "IDR",          # currency
            "680,xxx.xx"    # remaining balance
        ]
    ]

To access your ***first*** account number you can access the array like this

    acct[0][0]

---
### ***Logout***
This function to logout your account from the session.<br>
you need to ***logout*** everytime you want to exit the code<br>
or it will make you cant login for 10 minutes

    obj.logout()

---
## Next update
- Get account mutation
- Check incoming transfer by transfer value / notes