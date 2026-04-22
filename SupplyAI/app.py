from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def detect_disruption():
    df = pd.read_csv("data.csv")
    df["risk"] = df["delay_minutes"].apply(lambda x: "HIGH" if x > 30 else "LOW")
    return df

def suggest_route(location):
    routes = {
        "Delhi": "Use NH48 alternative",
        "Mumbai": "Divert via Pune route",
        "Chennai": "Use coastal bypass",
        "Lucknow": "Use outer ring road"
    }
    return routes.get(location, "No suggestion")

@app.route("/")
def home():
    data = detect_disruption()
    alerts = []

    for _, row in data.iterrows():
        if row["risk"] == "HIGH":
            alerts.append({
                "location": row["location"],
                "delay": row["delay_minutes"],
                "solution": suggest_route(row["location"])
            })

    return render_template("index.html", alerts=alerts)


if __name__ == "__main__":
    print("🚀 Starting server...")
    app.run(debug=True)