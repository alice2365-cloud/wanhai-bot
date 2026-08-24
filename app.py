from flask import Flask, jsonify, render_template, request
import json
import os

app = Flask(__name__)

DATA_FILE = "vessels_data.json"


def load_vessel_data():
  """讀取本地 JSON 快取資料"""
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return {}


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def search_vessel():
  data = request.json
  vessel_name = data.get("vessel_name", "").strip().upper()

  if not vessel_name:
    return jsonify({"status": "error", "message": "請輸入船名"})

  db = load_vessel_data()

  # 支援部分關鍵字或完整船名比對
  found_schedule = []
  for key in db:
    if vessel_name in key:
      found_schedule = db[key]
      break

  if not found_schedule:
    return jsonify({
        "status": "error",
        "message": (
            f"找不到船名為 '{vessel_name}' 的排班資料，請確認名稱是否正確。"
        ),
    })

  return jsonify({
      "status": "success",
      "vessel": vessel_name,
      "route": "Hybrid JSON Cache",
      "schedule": found_schedule,
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
