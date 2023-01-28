const yahooFinance = require("yahoo-finance");

async function historicalPriceData(symbol) {
  yahooFinance.historical(
    {
      symbol: "AAPL",
      from: "2020-01-01",
      to: "2021-10-10",
    },
    function (err, quotes) {
      // console.log(quotes);
      return quotes;
    }
  );
}

module.exports = { historicalPriceData };
