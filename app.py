import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "jewelry_data.json"

# --- Load/Save Helpers ---
def load_data():x
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "prices": {
            "goldWithoutGST": 0,
            "goldWithGST": 0,
            "silverWithoutGST": 0,
            "silverWithGST": 0,
        },
        "wages": [{"id": "default", "srNo": 1, "material": "Default", "rate": 1000}],
        "history": [],
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- Initialize Session ---
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# --- Sidebar Tabs ---
tab = st.sidebar.radio("Navigation", ["Calculator", "Wages", "Prices", "History"])

# --- Prices Tab ---
if tab == "Prices":
    st.header("Daily Prices")
    for key, label in [
        ("goldWithoutGST", "Gold (No GST)"),
        ("goldWithGST", "Gold (With GST)"),
        ("silverWithoutGST", "Silver (No GST)"),
        ("silverWithGST", "Silver (With GST)"),
    ]:
        data["prices"][key] = st.number_input(label, value=float(data["prices"].get(key, 0)))

    if st.button("Save Prices"):
        save_data(data)
        st.success("Prices updated!")

# --- Wages Tab ---
elif tab == "Wages":
    st.header("Making Charges")
    for wage in data["wages"]:
        col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
        col1.write(wage["srNo"])
        wage["material"] = col2.text_input("Material", value=wage["material"], key=f"mat_{wage['id']}")
        wage["rate"] = col3.number_input("Rate", value=wage["rate"], key=f"rate_{wage['id']}")
        if col4.button("🗑️", key=f"del_{wage['id']}") and len(data["wages"]) > 1:
            data["wages"] = [w for w in data["wages"] if w["id"] != wage["id"]]
            for i, w in enumerate(data["wages"], start=1):
                w["srNo"] = i
            save_data(data)
            st.experimental_rerun()

    if st.button("➕ Add Wage"):
        new_entry = {
            "id": str(datetime.now().timestamp()),
            "srNo": len(data["wages"]) + 1,
            "material": f"Item {len(data['wages']) + 1}",
            "rate": 1000,
        }
        data["wages"].append(new_entry)
        save_data(data)
        st.experimental_rerun()

# --- Calculator Tab ---
elif tab == "Calculator":
    st.header("Jewelry Calculator")

    material = st.radio("Material", ["gold", "silver"], horizontal=True)
    include_gst = st.toggle("Include GST", value=True)
    wage = st.selectbox("Select Wage", data["wages"], format_func=lambda w: f"{w['material']} (x{w['rate']})")

    weight = st.number_input("Weight (grams)", min_value=0.0, step=0.1)

    if st.button("Calculate"):
        price_per_gram = data["prices"]["goldWithGST"] if (material == "gold" and include_gst) else \
                         data["prices"]["goldWithoutGST"] if material == "gold" else \
                         data["prices"]["silverWithGST"] if include_gst else \
                         data["prices"]["silverWithoutGST"]

        total = weight * price_per_gram * wage["rate"]
        st.session_state.result = {
            "weight": weight,
            "material": material,
            "pricePerGram": price_per_gram,
            "wage": wage["rate"],
            "total": total,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    if "result" in st.session_state:
        r = st.session_state.result
        st.success(f"💰 Total Price: ₹{r['total']:,}")
        if st.button("Save to History"):
            entry = {**r, "id": str(datetime.now().timestamp())}
            data["history"].insert(0, entry)
            save_data(data)
            st.success("Saved to history!")

# --- History Tab ---
elif tab == "History":
    st.header("Calculation History")

    if st.button("🗑️ Clear History"):
        data["history"] = []
        save_data(data)
        st.success("History cleared!")

    if not data["history"]:
        st.info("No history yet.")
    else:
        for h in data["history"]:
            st.write(f"**{h['material'].upper()} {h['weight']}g** → ₹{h['total']:,}")
            st.caption(h["timestamp"])
