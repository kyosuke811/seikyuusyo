# ファイル読み込み（例: input.txt に無造作データが書かれている）
with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 初期化
surnames = []
billing_amounts = []
toll_amounts = []

# 苗字だけ抽出する関数（例：佐藤太郎 → 佐藤）
def extract_surname(name):
    return name[:]  # 単純な処理（実際は人力修正も必要）

# 数字抽出用の関数
def extract_number(text):
    number = ""
    for char in text:
        if char.isdigit():
            number += char
        elif number:
            break
    return number

# データ整形
for line in lines:
    line = line.strip()
    if not line:
        continue

    if "請求" in line:
        num = extract_number(line)
        if num:
            billing_amounts.append(num)
    elif "高速" in line:
        num = extract_number(line)
        if num:
            toll_amounts.append(num)
    else:
        name = extract_surname(line)
        surnames.append(name)

# すべて1列に表示
all_data = surnames + billing_amounts + toll_amounts

# 出力（1行に1つ）
for item in all_data:
    print(item)
