from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "kisan-connect-demo-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "kisan_connect.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS crop_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            crop TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            location TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id INTEGER NOT NULL,
            buyer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            message TEXT,
            FOREIGN KEY(listing_id) REFERENCES crop_listings(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transport_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            from_location TEXT NOT NULL,
            to_location TEXT NOT NULL,
            quantity REAL NOT NULL,
            vehicle TEXT NOT NULL,
            estimated_cost REAL NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            verified INTEGER DEFAULT 1
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            link TEXT
        )
    """)

    count = cur.execute("SELECT COUNT(*) FROM inputs").fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO inputs (name, category, price, verified) VALUES (?, ?, ?, ?)",
            [
                ("Certified Wheat Seeds", "Seeds", 850, 1),
                ("Hybrid Maize Seeds", "Seeds", 720, 1),
                ("NPK 10:26:26 Fertilizer", "Fertilizer", 1450, 1),
                ("Urea 45 kg", "Fertilizer", 310, 1),
                ("Mustard Certified Seeds", "Seeds", 690, 1),
            ],
        )

    count = cur.execute("SELECT COUNT(*) FROM schemes").fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO schemes (name, description, link) VALUES (?, ?, ?)",
            [
                ("PM-KISAN", "Eligible farmer families can receive income support through the scheme.", "https://pmkisan.gov.in/"),
                ("Pradhan Mantri Fasal Bima Yojana", "Crop insurance support against eligible crop losses and risks.", "https://pmfby.gov.in/"),
                ("Kisan Credit Card", "Credit facility for agricultural and allied activities through eligible banks.", "https://www.myscheme.gov.in/"),
                ("Soil Health Card", "Helps farmers understand soil nutrients and recommended inputs.", "https://soilhealth.dac.gov.in/"),
            ],
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    stats = {
        "crops": conn.execute("SELECT COUNT(*) FROM crop_listings").fetchone()[0],
        "inputs": conn.execute("SELECT COUNT(*) FROM inputs").fetchone()[0],
        "schemes": conn.execute("SELECT COUNT(*) FROM schemes").fetchone()[0],
        "transport": conn.execute("SELECT COUNT(*) FROM transport_requests").fetchone()[0],
    }
    latest = conn.execute(
        "SELECT * FROM crop_listings ORDER BY id DESC LIMIT 6"
    ).fetchall()
    conn.close()
    return render_template("index.html", stats=stats, latest=latest)


@app.route("/crop-advisory", methods=["GET", "POST"])
def crop_advisory():
    result = None
    if request.method == "POST":
        soil = request.form.get("soil", "")
        water = request.form.get("water", "")
        season = request.form.get("season", "")
        area = request.form.get("area", "")

        if soil == "Black":
            crops = ["Soybean", "Wheat", "Gram"]
        elif soil == "Alluvial":
            crops = ["Wheat", "Rice", "Mustard"]
        elif soil == "Red":
            crops = ["Groundnut", "Millet", "Maize"]
        else:
            crops = ["Millet", "Maize", "Pulses"]

        if water == "Low":
            crops = [c for c in crops if c in ["Gram", "Mustard", "Millet", "Groundnut", "Pulses"]] or ["Millet", "Gram"]
        elif water == "High" and season == "Kharif":
            if "Rice" not in crops:
                crops.insert(0, "Rice")

        result = {
            "crops": crops[:3],
            "soil": soil,
            "water": water,
            "season": season,
            "area": area,
        }

    return render_template("crop.html", result=result)


@app.route("/inputs")
def inputs():
    conn = get_db()
    items = conn.execute("SELECT * FROM inputs ORDER BY category, name").fetchall()
    conn.close()
    return render_template("inputs.html", items=items)


@app.route("/schemes")
def schemes():
    conn = get_db()
    items = conn.execute("SELECT * FROM schemes ORDER BY id").fetchall()
    conn.close()
    return render_template("schemes.html", schemes=items)


@app.route("/transport", methods=["GET", "POST"])
def transport():
    estimate = None
    if request.method == "POST":
        farmer = request.form.get("farmer_name", "").strip()
        from_location = request.form.get("from_location", "").strip()
        to_location = request.form.get("to_location", "").strip()

        try:
            quantity = float(request.form.get("quantity", 0))
        except ValueError:
            quantity = 0

        if quantity <= 0:
            flash("Please enter a valid quantity.", "error")
            return redirect(url_for("transport"))

        if quantity <= 500:
            vehicle = "Mini Truck"
            base_cost = 900
        elif quantity <= 1500:
            vehicle = "Pickup / Small Truck"
            base_cost = 1400
        else:
            vehicle = "Large Truck"
            base_cost = 2200

        estimated_cost = base_cost + max(0, quantity - 500) * 0.35

        conn = get_db()
        conn.execute(
            """INSERT INTO transport_requests
               (farmer_name, from_location, to_location, quantity, vehicle, estimated_cost)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (farmer, from_location, to_location, quantity, vehicle, estimated_cost),
        )
        conn.commit()
        conn.close()

        estimate = {
            "vehicle": vehicle,
            "cost": round(estimated_cost),
            "quantity": quantity,
            "from_location": from_location,
            "to_location": to_location,
        }

    return render_template("transport.html", estimate=estimate)


@app.route("/market", methods=["GET", "POST"])
def market():
    if request.method == "POST":
        farmer = request.form.get("farmer_name", "").strip()
        crop = request.form.get("crop", "").strip()
        location = request.form.get("location", "").strip()

        try:
            quantity = float(request.form.get("quantity", 0))
            price = float(request.form.get("price", 0))
        except ValueError:
            quantity, price = 0, 0

        if not farmer or not crop or not location or quantity <= 0 or price <= 0:
            flash("Please fill all crop listing details correctly.", "error")
            return redirect(url_for("market"))

        conn = get_db()
        conn.execute(
            """INSERT INTO crop_listings
               (farmer_name, crop, quantity, price, location)
               VALUES (?, ?, ?, ?, ?)""",
            (farmer, crop, quantity, price, location),
        )
        conn.commit()
        conn.close()

        flash("Crop listed successfully. Buyers can now see your listing.", "success")
        return redirect(url_for("market"))

    conn = get_db()
    listings = conn.execute(
        "SELECT * FROM crop_listings ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("market.html", listings=listings)


@app.route("/enquire/<int:listing_id>", methods=["POST"])
def enquire(listing_id):
    buyer = request.form.get("buyer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()

    if not buyer or not phone:
        flash("Buyer name and phone are required.", "error")
        return redirect(url_for("market"))

    conn = get_db()
    exists = conn.execute(
        "SELECT id FROM crop_listings WHERE id = ?", (listing_id,)
    ).fetchone()

    if not exists:
        conn.close()
        flash("Listing not found.", "error")
        return redirect(url_for("market"))

    conn.execute(
        "INSERT INTO enquiries (listing_id, buyer_name, phone, message) VALUES (?, ?, ?, ?)",
        (listing_id, buyer, phone, message),
    )
    conn.commit()
    conn.close()

    flash("Enquiry sent to the farmer (demo).", "success")
    return redirect(url_for("market"))


@app.route("/delete-listing/<int:listing_id>", methods=["POST"])
def delete_listing(listing_id):
    conn = get_db()
    conn.execute("DELETE FROM crop_listings WHERE id = ?", (listing_id,))
    conn.execute("DELETE FROM enquiries WHERE listing_id = ?", (listing_id,))
    conn.commit()
    conn.close()
    flash("Listing removed.", "success")
    return redirect(url_for("market"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
