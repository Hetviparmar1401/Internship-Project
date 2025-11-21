from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/task01/symbol-token-map", methods=["GET", "POST"])
def symbol_token_map_api():

    # -------------------------
    # POST method (JSON body)
    # -------------------------
    if request.method == "POST":
        data = request.get_json()
        file_path = data.get("file_path")

    # -------------------------
    # GET method (Query params)
    # -------------------------
    else:  # GET request
        file_path = request.args.get("file_path")

    # Validate input
    if not file_path:
        return jsonify({"error": "file_path is required"}), 400

    symbol_token_map = {}

    try:
        # Open CSV file
        with open(file_path, "r", encoding="utf-8") as file:
            rows = file.readlines()

        # Skip header row
        for row in rows[1:]:
            row = row.strip()
            if row == "":
                continue  # skip empty lines

            columns = row.split(",")

            # Validate column length
            if len(columns) < 12:
                continue

            instrument_token = columns[0].strip()
            trading_symbol   = columns[2].strip()
            instrument_type  = columns[9].strip()
            exchange         = columns[11].strip()

            # Only NSE Equity instruments
            if exchange == "NSE" and instrument_type == "EQ":
                symbol_token_map[trading_symbol] = int(instrument_token)

        return jsonify({
            "status": "success",
            "count": len(symbol_token_map),
            "symbol_token_map": symbol_token_map
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run app
if __name__ == "__main__":
    app.run(debug=True,port=5004)



