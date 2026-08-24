from flask import Flask, jsonify, render_template, request
from playwright.sync_api import sync_playwright

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
    with sync_playwright() as p:
      # 啟動無頭瀏覽器
      browser = p.chromium.launch(
          headless=True,
          args=['--no-sandbox', '--disable-setuid-sandbox'],
      )
      page = browser.new_page()

      # 前往萬海船期查詢頁面
      page.goto(
          'https://tw.wanhai.com/views/quick/skd_by_vessel.xhtml',
          timeout=60000,
      )

      # 1. 定位並輸入船名（需根據萬海實際頁面的 input 屬性調整）
      # 假設輸入框有特定 placeholder 或 selector
      page.wait_for_selector(
          "input[type='text'], input"
      )  # 等待輸入框載入
      # 假設我們要填入輸入框（實際可依 F12 檢視該 input 的 name 或 id 進行微調）
      page.fill("input[type='text']", vessel_name)

      # 2. 模擬點擊查詢按鈕
      # page.click("button:has-text('查詢'), input[type='submit']")

      # 3. 等待查詢結果的表格動態渲染出來
      page.wait_for_timeout(4000)  # 給予時間等待非同步表格載入

      # 4. 抓取表格所有列
      rows = page.locator('table tr').all()
      for row in rows:
        cols = row.locator('td').all_inner_texts()
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

      browser.close()

    if not schedule_rows:
      return jsonify({
          'status': 'error',
          'message': (
              '未能即時抓取到資料，可能需要精準對應萬海的查詢按鈕與輸入框'
              ' Selector。'
          ),
      })

    return jsonify({
        'status': 'success',
        'vessel': vessel_name,
        'route': 'Real-time Live Scraped',
        'schedule': schedule_rows,
    })

  except Exception as e:
    return jsonify({
        'status': 'error',
        'message': f'即時爬蟲執行失敗: {str(e)}',
    })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
