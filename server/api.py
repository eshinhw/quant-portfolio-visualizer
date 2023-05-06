from polygon import RESTClient

client = RESTClient("pvHqKQ85khKruMFAns0Zpj36AzZNCP8O")
ticker = "AAPL"

# List Aggregates (Bars)
bars = client.get_aggs(ticker=ticker, multiplier=1,
                       timespan="day", from_="2023-01-01", to="2023-01-10")

for bar in bars:
    print(bar)

