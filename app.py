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

      # 嘗試等待頁面載入完成，並擷取動態產生的表格列
      # （若萬海頁面結構有特定的 table 標籤，可在此處調整 selector）
      page.wait_for_timeout(3000)  # 給予 3 秒讓 JS 渲染

      # 抓取頁面中所有的表格列
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

    return jsonify({
        'status': 'success',
        'vessel': vessel_name,
        'route': 'Playwright Dynamic Render',
        'schedule': schedule_rows,
    })

  except Exception as e:
    return jsonify({'status': 'error', 'message': f'爬蟲執行發生錯誤: {str(e)}'})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
