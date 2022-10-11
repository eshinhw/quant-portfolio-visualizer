// const yahooFinance = require('yahoo-finance2').default; // NOTE the .default
var yahooFinance = require('yahoo-finance');

yahooFinance.historical({
  symbol: 'AAPL',
  from: '2020-01-01',
  to: '2021-10-10'
}, function (err, quotes) {
  console.log(quotes)
});

// const apple = async function() {
//   const results = await yahooFinance.search('AAPL');
//   console.log(results)
// }

// apple()


const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
