const yahooFinance = require("yahoo-finance");

yahooFinance.historical(
  {
    symbol: "AAPL",
    from: "2020-01-01",
    to: "2021-10-10",
  },
  function (err, quotes) {
    console.log(quotes);
  }
);