from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# ---------------------------------------------------------
# COMMON FUNCTION FOR TASK 3 (SMA CALCULATION)
# ---------------------------------------------------------
def process_task3(dates, closes):
    try:
        # VALIDATION
        if not dates or not closes:
            return {"error": "Dates and Close prices are required!"}, 400

        if len(dates) != len(closes):
            return {"error": "Dates and Close prices must have same length!"}, 400

        # CREATE DATAFRAME
        df = pd.DataFrame({
            "Date": pd.to_datetime(dates),
            "Close": closes
        })

        # CALCULATE SMA-3
        sma_values = []
        for i in range(len(df)):
            if i < 2:
                sma_values.append(None)
            else:
                avg = (df.loc[i, "Close"] +
                       df.loc[i-1, "Close"] +
                       df.loc[i-2, "Close"]) / 3
                sma_values.append(avg)

        df["SMA_3"] = sma_values

        # CONVERT NON-JSON objects
        df["Date"] = df["Date"].astype(str)

        return {
            "status": "success",
            "rows": df.to_dict(orient="records")
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500


# ---------------------------------------------------------
# POST METHOD (JSON BODY)
# ---------------------------------------------------------
@app.route("/task03/sma", methods=["POST"])
def task03_post():
    data = request.get_json()

    dates = data.get("dates")
    closes = data.get("close_prices")

    return process_task3(dates, closes)


# ---------------------------------------------------------
# GET METHOD (URL PARAMS)
# ---------------------------------------------------------
@app.route("/task03/sma", methods=["GET"])
def task03_get():
    dates = request.args.getlist("dates")
    closes = request.args.getlist("close_prices", type=float)

    return process_task3(dates, closes)


# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5006)
