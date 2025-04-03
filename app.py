from flask import Flask, request, render_template
from google_play_scraper import search

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}

    if request.method == "POST":
        app_packages = request.form["app_packages"].split(",")  # Multiple apps
        keywords = request.form["keywords"].split(",")  # Multiple keywords

        for app_package in app_packages:
            app_package = app_package.strip()
            results[app_package] = {}

            for keyword in keywords:
                keyword = keyword.strip()
                search_results = search(keyword, country="us")[:50]  # Get top 50 results
                rank = next((i+1 for i, app in enumerate(search_results) if app['appId'] == app_package), "Not Found")
                results[app_package][keyword] = rank

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
