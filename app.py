from flask import Flask, jsonify
import datetime
import pandas as pd
from google_play_scraper import search

app = Flask(__name__)

# 🔹 Configuration
APP_PACKAGE = "com.whatsapp"  # Replace with your app's package name
KEYWORDS = ["messenger", "chat app", "video call"]
COUNTRY = "us"
NUM_RESULTS = 50
EXCEL_FILE = "playstore_rankings.xlsx"

# 🔹 Function to Fetch Rankings
def get_rank(keyword):
    results = search(keyword, country=COUNTRY)  # Remove 'n' parameter
    results = results[:NUM_RESULTS]  # Manually limit the results
    for rank, app in enumerate(results, start=1):
        if app['appId'] == APP_PACKAGE:
            return rank
    return "Not Found"

@app.route("/")
def fetch_rankings():
    date = datetime.date.today().strftime("%Y-%m-%d")
    rankings = []

    for keyword in KEYWORDS:
        rank = get_rank(keyword)
        rankings.append({"date": date, "keyword": keyword, "rank": rank})

    # Save to Excel
    try:
        df_existing = pd.read_excel(EXCEL_FILE)
        df_new = pd.DataFrame(rankings)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    except FileNotFoundError:
        df_combined = pd.DataFrame(rankings)

    df_combined.to_excel(EXCEL_FILE, index=False)

    return jsonify({"message": "✅ Rankings updated!", "data": rankings})

if __name__ == "__main__":
    app.run(debug=True)
