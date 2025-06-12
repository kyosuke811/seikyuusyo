import re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
import streamlit as st
import io

# -----------------------------
# Streamlitの画面設定
# -----------------------------
st.title("請求書作成")
date = st.text_input("作成したい請求書の日付を入力してください(MM/DD)")
text_input = st.text_area("処理するテキストを入力してください: ")

# テキストを行単位で分割
lines = text_input.splitlines()

# -----------------------------
# 各種判定・抽出関数の定義
# -----------------------------

# ドライバー情報の開始行かを判定
def is_driver_start_line(line):
    return line.count('時') >= 2

# 氏名を抽出（漢字2文字 or カタカナ3文字）
def extract_name(line):
    pattern = r'[一-?]{2}|[ァ-ヴ]{3}'
    match = re.findall(pattern, line)
    return match[0] if match else ""

# 請求行（求＋高速）かどうか
def is_seikyu_line(line):
    return '求' in line and '高速' in line

# 請求額と高速代を抽出（"123,456円" 形式）
def is_seikyu_kousoku(line):
    pattern = r'(\d{1,3}(?:,\d{3})*)円'
    match = re.findall(pattern, line)
    seikyu = int(match[0].replace(',', ''))
    kousoku = int(match[1].replace(',', ''))
    return seikyu, kousoku

# ￥形式に整形
def format_yen(value):
    return f"￥{int(value):,}"

# -----------------------------
# 請求データの抽出ロジック
# -----------------------------
drivers_data = []
i = 0
while i < len(lines):
    line = lines[i]
    if is_driver_start_line(line):
        name = extract_name(line)
        j = i + 1
        while j < len(lines) and not is_driver_start_line(lines[j]):
            line = lines[j]
            if is_seikyu_line(line):
                seikyu, kousoku = is_seikyu_kousoku(line)
                drivers_data.append([name, seikyu, kousoku])
            j += 1
        # 抽出済み部分を削除してリストを前詰めに
        del lines[i:j]
        i = 0
    else:
        i += 1

# -----------------------------
# Excelファイルの作成
# -----------------------------
wb = Workbook()
ws = wb.active
ws.title = "請求書"

# タイトル行の作成
ws.merge_cells("A1:J1")
ws["A1"] = f"請求書{date}"
ws["A1"].font = Font(size=14, bold=True)
ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws["A2"] = "下記の通りに御請求申し上げます"

# 和暦形式で日付出力
if "/" in date:
    month, day = date.split("/")
else:
    st.error("日付はMM/DDの形式で入力してください")
    st.stop()

if int(month) + 1 < 13:
    ws["I2"] = f"令和7年{int(month)+1}月1日"
else:
    ws["I2"] = f"令和8年{int(month)-11}月1日"

# 請求額セル（合計）
ws.merge_cells("A3:C3")
ws["A3"] = "御請求額"
ws["A3"].alignment = Alignment(horizontal="center", vertical="center")
ws.merge_cells("D3:J3")
ws["D3"] = f"=SUM(J5:J{5+len(drivers_data)})"
ws["D3"].number_format = '"￥"#,##0'
ws["D3"].font = Font(size=16, bold=True)
ws["D3"].alignment = Alignment(horizontal="center", vertical="center")

# ヘッダー行
ws.append([
    "日付", "曜日", "案件名", "内容", "担当", "車種", "単価", "消費税", "高速代", "合計"
])

# -----------------------------
# 各ドライバーのデータを追加
# -----------------------------
row_num = 5
for driver in drivers_data:
    name, seikyuu, kousoku = driver
    goukei = int(seikyuu) * 1.1 + int(kousoku)

    ws.append([
        f"2025/{date}",
        "=CHOOSE(WEEKDAY(A5, 1), \"日\", \"月\", \"火\", \"水\", \"木\", \"金\", \"土\")",
        "川崎DC",
        "時間貸し輸送",
        name,
        "4t冷蔵",
        int(seikyuu),
        f"=G{row_num}*0.1",
        int(kousoku),
        f"=G{row_num}+H{row_num}+I{row_num}"
    ])
    row_num += 1

# -----------------------------
# 枠線（Border）の設定
# -----------------------------
border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin'),
)

for row in ws.iter_rows(min_row=3, max_row=3+len(drivers_data)+1, min_col=1, max_col=10):
    for cell in row:
        cell.border = border

# -----------------------------
# Excelの保存＆ダウンロード処理
# -----------------------------
excel_buffer = io.BytesIO()
wb.save(excel_buffer)
excel_buffer.seek(0)

safe = date.replace('/', '_')  # ファイル名用のスラッシュ置換

st.download_button(
    label="請求書作成",
    data=excel_buffer,
    file_name=f"{safe}請求書.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
