from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search_vessel():
  data = request.json
  vessel_name = data.get('vessel_name', '').strip().upper()

  if not vessel_name:
    return jsonify({'status': 'error', 'message': '請輸入船名'})

  try:
    # 1. 設定萬海船期查詢的目標網址或 API 端點
    # （實務上會對應萬海公開查詢系統的請求網址）
    target_url = 'https://tw.wanhai.com/views/quick/skd_by_vessel.xhtml'

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/122.0.0.0 Safari/537.36'
        ),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # 2. 模擬使用者送出查詢表單（帶入使用者輸入的船名）
    # payload = { 'vesselName': vessel_name, ... }
    # response = requests.post(target_url, data=payload, headers=headers)

    # 3. 使用 BeautifulSoup 解析回傳的 HTML 頁面結構
    # soup = BeautifulSoup(response.text, 'html.parser')
    # schedule_rows = []
    
    # 4. 動態尋找表格中的每一個 tr（列），把所有欄位（td）抓出來
    # for tr in soup.find_all('tr', class_='schedule-row'):
    #     cols = [td.text.strip() for td in tr.find_all('td')]
    #     if cols:
    #         schedule_rows.append({
    #             "status_type": cols[0],
    #             "port": cols[1],
    #             "arr_voyage": cols[2],
    #             "arr_date": cols[3],
    #             "arr_time": cols[4],
    #             "berth_date": cols[5],
    #             "berth_time": cols[6],
    #             "dep_voyage": cols[7],
    #             "dep_date": cols[8],
    #             "dep_time": cols[9],
    #             "status": cols[10]
    #         })

    # ---------------------------------------------------------
    # ⚠️ 注意：
    # 為了讓你的專案真的能動態運作，我們需要配合萬海網站目前的
    # 表單欄位名稱（form parameters）與 DOM 結點來寫解析邏輯。
    # ---------------------------------------------------------

    # 這裡先回傳一個結構，讓你知道後端會轉為接收真實爬蟲結果
    return jsonify({
        'status': 'success',
        'vessel': vessel_name,
        'route': 'DYNAMIC_LIVE_QUERY',
        'schedule': [],  # 這邊會填入從網站即時解析出來的清單
    })

  except Exception as e:
    return jsonify({'status': 'error', 'message': f'抓取失敗: {str(e)}'})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
