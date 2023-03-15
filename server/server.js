const express = require("express");
const { historicalPriceData } = require("./FinancialData");
const app = express();
const port = 3000;

let quotes = historicalPriceData("AAPL");


app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
