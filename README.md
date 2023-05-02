# Trading Wizard

Ultimate Web Trading Platform for Success in Financial Markets

## Main Features

- Total portfolio holdings and performance across accounts
- Dividend visualizer to track dividends performance
- Position sizing calculator to manage your risk properly
- Custom watchlist to follow your favorite markets
- Alerts on markets so you'll never miss a price movement

## Data Sources

- [yfinance](https://pypi.org/project/yfinance/)
- [OANDA API](https://developer.oanda.com/)
- [Questrade API](https://www.questrade.com/api/documentation/getting-started)
- [Google Cloud Platform (GCP) Virtual Machine](https://cloud.google.com/)

## Data Analysis in Python

- [Pandas Basics](PANDAS.md)
- [SQL](SQL.md)

<!--
## Asset Allocation Strategies

- Traditonal 60% Equities + 40% Bonds Portfolio
- Four Seasons Portfolio
- All Weather Portfolio
- Permanent Portfolio
- [Dual Momentum](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2042750) by Gary Antonacci
- [Vigilant Asset Allocation (VAA)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3002624) by Wouter J. Keller
- [Defensive Asset Allocation (DAA)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3212862) by Wouter J. Keller
- [Lethargic Asset Allocation (LAA)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3498092) by Wouter J. Keller


## Usage

Run `python main.py`.

### Main Menu

<p align="center">
  <img width="500" height="300" src="https://user-images.githubusercontent.com/41933169/166627802-eae6970a-887d-4813-a732-46ee5b423488.png">
</p>

### Account Options

<p align="center">
  <img width="500" height="300" src="https://user-images.githubusercontent.com/41933169/166627895-3be04278-1b37-411f-8a14-592e7f298b85.png">
</p>

### Add New Account

New Questrade account can be added and will be saved in json file in the same location of `main.py`. Make sure new account number is correct! 

If you have two different Questrade IDs, unfortunately, multi-users feature is not supported yet. You have to get new access code from Questrade whenever you switch from one ID to another. :(

<p align="center">
  <img width="500" height="300" src="https://user-images.githubusercontent.com/41933169/166627975-518800ed-c439-4da0-b22d-65a0cb4634f9.png">
</p>

### Portfolio Summary

#### Balance Summary, Investment Summary and Performance Against BenchMark

BenchMark Portfolio is Traditional 60% Equities + 40% Bonds Portfolio. Performance comparison against BM computes CAGR and MDD.

<p align="center">
  <img width="700" height="500" src="https://user-images.githubusercontent.com/41933169/166628294-66ded221-02a2-4d5b-b2c1-1c70b0b9655e.png">
</p>

#### Historical Dividends

<p align="center">
  <img width="500" height="500" src="https://user-images.githubusercontent.com/41933169/166628418-2abfd386-3ff9-4d88-9015-f802346e922d.png">
</p>

<p align="center">
  <img width="500" height="500" src="https://user-images.githubusercontent.com/41933169/166628419-0f04464d-0b92-4811-a7d4-8d8a822b55f7.png">
</p>

### Allocation Rebalancing

Currently, PyQuant only offers rebalancing outputs for VAA and LAA based on historical momentums. More allocation strategies will be added!

<p align="center">
  <img width="500" height="300" src="https://user-images.githubusercontent.com/41933169/166628514-79c7e05a-3270-401c-b0fa-5abed9218256.png">
</p>

### Email Sharing

Automatic email sent out can be set up by providing your gmail address and gmail app password. Gmail app password must be set up from your Google account. Once gmail app password is generated, the overall portfolio summary can be sent out to other email addresses.

<p align="center">
  <img width="500" height="300" src="https://user-images.githubusercontent.com/41933169/166745729-7eb723e8-2dba-4094-88c6-1fa35d7fce41.png">
</p>

<p align="center">
  <img width="500" height="300" src="https://user-images.githubusercontent.com/41933169/166745730-2e73d573-efa1-4520-9ada-f5f28e256d27.png">
</p>

Below is the sample email.

<p align="center">
  <img width="700" height="500" src="https://user-images.githubusercontent.com/41933169/166746982-490a5849-9df5-42ef-9352-cfb566a21d7f.png">
</p>

## Futher Improvement Features

- Account verification when new account is added.
- Multi-users access without getting new access code (different yaml file paths for each Questrade ID)
- ~~Automatic email share of portfolio summary~~
- Improve performance comparison matrices
- Global Equities Momentum to determine when to buy equities
- Fixed Asset Allocations Rebalancing
-->
