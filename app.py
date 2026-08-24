from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search_vessel():
  data = request.json
  vessel_name = data.get('vessel_name', '').strip().upper()

  # 模擬對應你截圖中的詳細完整格式資料
  detailed_schedule = [
      {
          "status_type": "目前狀態",
          "port": "TOKYO",
          "arr_voyage": "N187",
          "arr_date": "2026/08/22",
          "arr_time": "21:50",
          "berth_date": "2026/08/22",
          "berth_time": "22:48",
          "dep_voyage": "S188",
          "dep_date": "2026/08/23",
          "dep_time": "19:16",
          "status": "ACTUAL",
      },
      {
          "status_type": "下個狀態",
          "port": "YOKOHAMA",
          "arr_voyage": "N187",
          "arr_date": "2026/08/23",
          "arr_time": "22:00",
          "berth_date": "2026/08/23",
          "berth_time": "22:00",
          "dep_voyage": "S188",
          "dep_date": "2026/08/24",
          "dep_time": "08:00",
          "status": "ESTIMATED",
      },
      {
          "status_type": "",
          "port": "NAGOYA",
          "arr_voyage": "N186",
          "arr_date": "2026/07/25",
          "arr_time": "11:00",
          "berth_date": "2026/07/25",
          "berth_time": "11:30",
          "dep_voyage": "S187",
          "dep_date": "2026/07/25",
          "dep_time": "23:25",
          "status": "ACTUAL",
      },
      {
          "status_type": "",
          "port": "HONG KONG",
          "arr_voyage": "S187",
          "arr_date": "2026/08/01",
          "arr_time": "00:00",
          "berth_date": "2026/08/01",
          "berth_time": "08:00",
          "dep_voyage": "S187",
          "dep_date": "2026/08/02",
          "dep_time": "02:10",
          "status": "ACTUAL",
      },
  ]

  return jsonify({
      "status": "success",
      "vessel": vessel_name if vessel_name else "ATHENS BRIDGE",
      "route": "JSM (JSM)",
      "schedule": detailed_schedule,
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
