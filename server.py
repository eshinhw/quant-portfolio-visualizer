from flask import Flask
import pandas as pd

app = Flask(__name__)

# Members API Route


@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}


@app.route("/dataframe")
def dataframe():

    # initialize list elements
    data = [10, 20, 30, 40, 50, 60]

    # Create the pandas DataFrame with column name is provided explicitly
    df = pd.DataFrame(data, columns=['Numbers'])

    print(df.to_json())

    # print dataframe.
    return df.to_json(orient="records")


if __name__ == "__main__":
    app.run(debug=True)
