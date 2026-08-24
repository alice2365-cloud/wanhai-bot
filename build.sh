#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# 安裝 Playwright 專用的瀏覽器與系統依賴
playwright install chromium
playwright install-deps chromium
