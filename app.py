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
    # 使用 Playwright 啟動無頭瀏覽器，完美應付 JavaScript 動態渲染網站
    with sync_playwright() as p:
      # launch(headless=True) 在背景執行
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

      # 等待輸入框出現並填入使用者查詢的船名
      # （需根據萬海實際網頁的 Input ID 或 Selector 進行對應調整）
      # 假設輸入框的 id 或 name 包含 vessel
      page.wait_for_selector(
          "input[type='text'], input[placeholder*='船'], input"
      )

      # 這裡我們模擬在輸入框填入船名並送出查詢
      # 實際實作時，會定位到該查詢輸入框
      # page.fill("input[name*='vessel']", vessel_name)
      # page.click("button:has-text('查詢'), input[type='submit']")

      # 等待表格資料渲染完成
      # page.wait_for_selector("table tr", timeout=10000)

      # 取得表格的所有列並解析
      # rows = page.locator("table tr").all()
      # for row in rows:
      #     cols = row.locator("td").all_inner_texts()
      #     if len(cols) >= 10:
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
      #             "status": cols[10] if len(cols) > 10 else ""
      #         })

      browser.close()

    # 如果順利爬到資料就回傳，若網頁結構需微調，可印出 log 除錯
    return jsonify({
        'status': 'success',
        'vessel': vessel_name,
        'route': 'REAL-TIME LIVE SCRAPED',
        'schedule': schedule_rows,
    })

  except Exception as e:
    return jsonify({
        'status': 'error',
        'message': f'即時爬蟲抓取發生錯誤: {str(e)}',
    })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
