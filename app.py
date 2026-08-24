from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


# 1. 當打開網頁根目錄時，顯示 HTML 介面
@app.route('/')
def index():
    return render_template('index.html')


# 2. 接收網頁傳來的查詢請求
@app.route('/api/search', methods=['POST'])
def search_vessel():
  data = request.json
  vessel_name = data.get('vessel_name')

  # 這裡未來可以放入你的爬蟲邏輯 (目前先用測試資料回傳)
  mock_schedule = [
      {
          'port': '基隆 (KEELUNG)',
          'eta': '2026-08-28 08:00',
          'etd': '2026-08-29 18:00',
          'voyage': 'N032',
      },
      {
          'port': '高雄 (KAOHSIUNG)',
          'eta': '2026-08-30 10:00',
          'etd': '2026-08-31 22:00',
          'voyage': 'N032',
      },
  ]

  return jsonify({
      'status': 'success',
      'vessel': vessel_name,
      'schedule': mock_schedule,
  })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
