Welcome to SimpleWallet! This application provides a robust set of features for managing bank accounts, transactions, and interest calculations. 

# Total Work Hours: 12


## Technical Details

- **Poetry:** The project is managed using Poetry for streamlined dependency management and project configuration.

- **Dockerized Container:** The application is containerized using Docker, making it easy to deploy and run consistently across different environments.

- **Celery Integration:** Celery is integrated into the system to handle scheduled tasks, contributing to the automation of background processes.

## Note

Please be aware that due to time constraints, the user interface (UI) and unit testing have not received extensive attention. The focus has been on delivering core functionality within the specified timeframe. Your understanding and feedback are highly appreciated as we work towards further enhancing and refining this Bank Management System.

Thank you for your time and consideration. If you have any questions or feedback, feel free to reach out!


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
