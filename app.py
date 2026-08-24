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

  schedule_rows = []

  try:
    # 萬海船期查詢的主網址或對應的頁面端點
    # 實務上我們可直接帶入查詢參數或目標 xhtml 頁面
    target_url = 'https://tw.wanhai.com/views/skd/SkdByVsl.xhtml'

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/122.0.0.0 Safari/537.36'
        ),
        'Referer': 'https://tw.wanhai.com/views/Main.xhtml',
    }

    # 如果需要帶入查詢參數（例如船名代號或表單欄位）
    params = {
        'vesselName': vessel_name
        # 若有特定的 file_num 也可在此動態帶入
    }

    # 發送 GET 請求取得網頁內容
    response = requests.get(target_url, params=params, headers=headers, timeout=15)
    response.encoding = 'utf-8'

    if response.status_code == 200:
      # 使用 BeautifulSoup 解析 HTML 結構
      soup = BeautifulSoup(response.text, 'html.parser')

      # 尋找船期表格中的每一列（依據萬海頁面實際的 table 與 tr 結構）
      # 這邊會抓取頁面上所有符合的表格列
      rows = soup.find_all('tr')

      for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all('td')]
        # 篩選出包含有效停靠港資料的列（根據欄位數量過濾）
        if len(cols) >= 10:
          schedule_rows.append({
              'status_type': cols[0],
              'port': cols[1],
              'arr_voyage': cols[2],
              'arr_date': cols[3],
              'arr_time': cols[4],
              'berth_date': cols[5],
              'berth_time': cols[6],
              'dep_voyage': cols[7],
              'dep_date': cols[8],
              'dep_time': cols[9],
              'status': cols[10] if len(cols) > 10 else 'ESTIMATED',
          })

    # 如果因為萬海有些頁面是透過 JS 動態載入導致 requests 抓不到直屬 tr，
    # 我們可以進一步對應其實際的 CSS Selector 進行調整。
    # 若此時 schedule_rows 仍為空，會回傳提示讓前端確認。

    return jsonify({
        'status': 'success',
        'vessel': vessel_name,
        'route': 'Live Scraped via SkdByVsl',
        'schedule': schedule_rows,
    })

  except Exception as e:
    return jsonify({'status': 'error', 'message': f'爬蟲執行失敗: {str(e)}'})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
