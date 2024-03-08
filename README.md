<div align="center">

  ![logo](https://github.com/eshinhw/quant-portfolio-visualizer/assets/41933169/5e05f0a5-384d-421c-8a56-aa8b2265b93c)

</div>

<div align="center">

  ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/eshinhw/quant-portfolio-visualizer)
  ![GitHub issues](https://img.shields.io/github/issues/eshinhw/quant-portfolio-visualizer)
  ![GitHub pull requests](https://img.shields.io/github/issues-pr/eshinhw/quant-portfolio-visualizer)
  
</div>

## Objectives

- Develop an interactive dash app in Python with financial data.
- Display the historical performances of quantitative factors in Quant Investing from Fama-French Data Library.
- Introduce various types of portfolio asset allocation strategies and analyze the historical performances and statistics.

## Fama-French Quantitative Factors

- Size (SMB): Small firms outperform Big firms in the long run.
- Value (HML): Return of value firms minus Return of growth firms. FF found that value firms outperform growth firms in the long run.
- Market Beta

- Momentum

## Portfolio Asset Allocation Strategies

- Classic 60% Equities + 40% Bonds Portfolio
- Four Seasons Portfolio
- All Weather Portfolio
- Permanent Portfolio
- [Dual Momentum](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2042750) by Gary Antonacci
- [Vigilant Asset Allocation (VAA)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3002624) by Wouter J. Keller
- [Defensive Asset Allocation (DAA)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3212862) by Wouter J. Keller
- [Lethargic Asset Allocation (LAA)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3498092) by Wouter J. Keller

## How to Install and Run

1. Clone the repo
2. Run virtual environment by `source venv/bin/activate`
3. Run `python src/app.py`
4. Wait until you see `Dash is running on http://127.0.0.1:8050/` on the console.

## Data Source

- [Kenneth R. French - Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)

## Demo Screenshot

<div align="center">

  <img width="1200" height="600" alt="" src="https://github.com/eshinhw/quant-portfolio-visualizer/assets/41933169/f62c82a0-d2f1-4289-ae30-864aae4364b1">

</div>
