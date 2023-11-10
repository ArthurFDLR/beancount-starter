# Beancount Starter - A template to start your Beancount ledger <!-- omit in toc -->


This is a template to start your Beancount ledger. It includes a basic folder structure and some example files.

- [Getting started](#getting-started)
- [Ledger structure](#ledger-structure)
  - [`ledger/banking`](#ledgerbanking)
  - [`ledger/setup`](#ledgersetup)
    - [Assets](#assets)
    - [Liabilities](#liabilities)
    - [Expenses](#expenses)
    - [Income](#income)
    - [Commodities](#commodities)



## Getting started

1. Clone this repository:
```bash
git clone git@github.com:ArthurFDLR/beancount-starter.git
```

2. Build the Docker image:
```bash
docker build -t beancount-starter .
``` 

3. Run the Docker container:
```bash
docker run --rm -v $PWD:/ledger -e BEANCOUNT_FILE=/ledger/ledger-config.bean -p 5000:5000 beancount-starter
```

4. Open your browser at [http://localhost:5000](http://localhost:5000)


## Ledger structure

### [`ledger/banking`](/ledger/banking/)

This folder contains all operations related to your bankings accounts: checking, savings, credit cards, etc.
Create a file for each account and credit/debit card you have. Ideally, the name of the files should match the account names definned in your [`setup` folder](/ledger/setup/).

For example, if you have a Chase checking account (`Assets:US:Chase:Checking`) and the Freedom Unlimited credit card (`Liabilities:US:Chase:FreedomUnlimited`), you should have the following files:
```
banking
├── chase-checking.bean
└── chase-freedom-unlimited.bean
```

In case of large number of transactions, you can split the transactions history per year:
```
banking
├── 2022
│   └── chase-checking.bean
└── 2023
    ├── chase-checking.bean
    └── chase-freedom-unlimited.bean
```

### [`ledger/setup`](/ledger/setup/)

This folder contains all the files related to your setup. It is the first folder you should create when starting a new ledger. It defines all your bank accounts, credit cards, investment accounts, expenses categories, etc. A good setup is the key to a good ledger. It will make your life easier when you will start to enter transactions and generate reports.

A clear understanding of Double-Entry accounting is crucial to setting up your ledger. If you are not familiar with Double-Entry accounting, I recommend you to read [Beancount creator's article *The Double-Entry Counting Method*](https://beancount.github.io/docs/the_double_entry_counting_method.html) page.

#### Assets

> Asset accounts represent something the owner has. A canonical example is banking accounts. Another one is a “cash” account, which counts how much money is in your wallet. Investments are also assets (their units aren’t dollars in this case, but rather some number of shares of some mutual fund or stock). Finally, if you own a home, the home itself is considered an asset (and its market value fluctuates over time).
> *The Double-Entry Counting Method*, Martin Blais

Let's start by setting up a checking account with Chase which holds $1,000.00 when you start your ledger:

```beancount
2020-07-08 open Assets:US:Chase:Checking         USD
2020-07-08 pad Assets:US:Chase:Checking Equity:Opening-Balances
2020-07-20 balance Assets:US:Chase:Checking  10000.00 USD
```

Let's say that you have 100.00€ in cash remaining from your last trip to Europe:

```
2020-01-01 open Assets:Cash
2020-01-01 pad Assets:Cash Equity:Opening-Balances
2020-07-17 balance Assets:Cash                 100.00 EUR
```

Your investment must also be defined as assets. Their definitiion will evolve with the various financial objects you will buy and sell.

```beancount
2020-07-08 open Assets:US:Vanguard:401K       USD, VTI
2020-08-01 open Assets:HardWallet:Ledger      BTC, ETH
```

If someone owes you money, you can create a receivable entry for that person or entity:

```beancount
2000-01-01 open Assets:Receivables
2000-01-01 open Assets:Receivables:John
2000-01-01 open Assets:Receivables:SecurityDeposit
```

#### Liabilities

> A liability account represents something the owner owes. The most common example is a credit card. Again, the statement provided by your bank will show positive numbers, but from your own perspective, they are negative numbers. A loan is also a liability account. For example, if you take out a mortgage on a home, this is money you owe, and will be tracked by an account with a negative amount. As you pay off the mortgage every month the negative number goes up, that is, its absolute value gets smaller and smaller over time (e.g., -120,000 -> -117,345).
> *The Double-Entry Counting Method*, Martin Blais

Let's say that you have a Chase Freedom Unlimited credit card and a student loan:

```beancount
2021-11-16 open Liabilities:US:Chase:FreedomUnlimited      USD
2020-01-01 open Liabilities:StudentLoan                 USD
```

#### Expenses

> An expense account represents something you’ve received, perhaps by exchanging something else to purchase it. This type of account will seem pretty natural: food, drinks, clothing, rent, flights, hotels and most other categories of things you typically spend your disposable income on. However, taxes are also typically tracked by an expense account: when you receive some salary income, the amount of taxes withheld at the source is recorded immediately as an expense. Think of it as paying for government services you receive throughout the year.
> *The Double-Entry Counting Method*, Martin Blais

The expenses accounts are the most subjective part of your ledger. You can create as many as you want. The more you create, the more detailed your reports will be. However, you should not create too many accounts. It will make your ledger harder to maintain and your reports harder to read. Also, you should organize your expenses accounts in sub-accounts. For example, you can create a `Expenses:Food` account and then create sub-accounts for each type of food you buy: `Expenses:Food:Groceries`, `Expenses:Food:Restaurants`, `Expenses:Food:Coffee`, etc.


#### Income

> An income account is used to count something you’ve given away in order to receive something else (typically assets or expenses). For most people with jobs, that is the value of their time (a salary income). Specifically, here we’re talking about the gross income. For example, if you’re earning a salary of $120,000/year, that number is $120,000, not whatever amount remains after paying for taxes. Other types of income includes dividends received from investments, or interest paid from bonds held. There are also a number of oddball things received you might record as income, such the value of rewards received, e.g., cash back from a credit card, or monetary gifts from someone.
> *The Double-Entry Counting Method*, Martin Blais

Let's say that you get a salary from a 9 to 5 job with 401K matching. And you also get a side income from a rental property and a side hustle:

```beancount
2020-01-01 open Income:Work:Paycheck USD
2020-01-01 open Income:Work:401Kmatch USD
2020-01-01 open Income:RentalProperty USD
2020-01-01 open Income:SideHustle USD
```

#### Commodities

There is a “Commodity” directive that can be used to declare currencies, financial instruments, commodities (different names for the same thing in Beancount):
```
YYYY-MM-DD commodity Currency
```

This directive is entirely optional: you can use commodities without having to really declare them this way. The purpose of this directive is to attach commodity-specific metadata fields on it, so that it can be gathered by plugins later on. For example, you might want to provide automatically fetch prices for a given commodity. The [`beanprice`](https://github.com/beancount/beanprice) interpretes the `price` metadata field to fetch conversion prices from various sources.

Use [`/scripts/fetch_prices.py`](/scripts/fetch_prices.py) to fetch the prices of all your commodities. It will create a `prices.bean` file in your `ledger` folder.
