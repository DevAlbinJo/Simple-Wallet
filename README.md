## Features

* Create Bank Account.
* Deposit & Withdraw and Transfer Money
* Bank Account Type Support (e.g. Current Account, Savings Account)
* Interest calculation depending on the Bank Account type
* Transaction report with a date range filter 
* See balance after every transaction in the Transaction Report
* Calculate Monthly Interest Using Celery Scheduled tasks
* More efficient and accurate interest calculation and balance update
* Ability to add Minimum and Maximum Transaction amount restriction

## Requirements

+ celery==4.4.2
+ Django==5.0
+ django-celery-beat==2.1.0
+ python-dateutil==2.8.1
+ redis==3.5.3

## Project Installation

Clone GitHub Project,
```bash
git clone https://github.com/DevAlbinJo/Simple-Wallet.git

cd Simple-Wallet
```

Install development dependencies,
```bash
poetry init
poetry install
poetry shell
```

Migrate Database,
```bash
python manage.py migrate
```

Run the web application locally,
```bash
python manage.py runserver # 127.0.0.1:8000
```

Create Superuser,
```bash
python manage.py createsuperuser
```

Run Celery
(Different Terminal Window with Virtual Environment Activated)
```bash
celery -A banking_system worker -l info

celery -A banking_system beat -l info
```
