import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/get_schedule', methods=['POST'])
def get_schedule():
  data = request.json
  vessel_name = data.get('vessel_name')

  # 模擬去萬海抓資料（帶上完整的瀏覽器 Headers 繞過 403）
  headers = {
      'User-Agent': (
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
          ' (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
      ),
      'Referer': 'https://tw.wanhai.com/views/quick/skd_by_vessel.xhtml',
  }

  # 這裡先用測試資料回傳，確認前後端串接成功
  mock_data = [
      {
          'port': '基隆 (KEELUNG)',
          'eta': '2026-08-28 08:00',
          'etd': '2026-08-29 18:00',
      },
      {
          'port': '高雄 (KAOHSIUNG)',
          'eta': '2026-08-30 10:00',
          'etd': '2026-08-31 22:00',
      },
  ]

  return jsonify({'status': 'success', 'schedule': mock_data})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
