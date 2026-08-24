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

      # 1. 等待頁面上的輸入框載入（根據萬海實際的 input 屬性調整）
      page.wait_for_selector('input', timeout=10000)

      # 2. 填入船名（若有多個輸入框，需指定對應的 name 或 id）
      # 這裡嘗試填入第一個文字輸入框
      page.fill("input[type='text']", vessel_name)

      # 3. 模擬點擊查詢按鈕（可依據按鈕上的文字或 class 調整）
      # 例如點擊包含「查詢」字樣的按鈕
      try:
        page.click("button:has-text('查詢'), input[type='submit'], .search-btn")
      except:
        # 如果找不到按鈕，嘗試直接對輸入框按下 Enter 鍵
        page.press("input[type='text']", 'Enter')

      # 4. 給予足夠時間等待表格非同步載入
      page.wait_for_timeout(5000)

      # 5. 抓取表格資料
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
              '抓取不到資料：可能是萬海頁面的輸入框或查詢按鈕選擇器需要進一步對應。'
          ),
      })

    return jsonify({
        'status': 'success',
        'vessel': vessel_name,
        'route': 'Live Scraped',
        'schedule': schedule_rows,
    })

  except Exception as e:
    return jsonify({'status': 'error', 'message': f'爬蟲執行失敗: {str(e)}'})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
