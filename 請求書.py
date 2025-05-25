# �t�@�C���ǂݍ��݁i��: input.txt �ɖ�����f�[�^��������Ă���j
with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# ������
surnames = []
billing_amounts = []
toll_amounts = []

# �c���������o����֐��i��F�������Y �� �����j
def extract_surname(name):
    return name[:]  # �P���ȏ����i���ۂ͐l�͏C�����K�v�j

# �������o�p�̊֐�
def extract_number(text):
    number = ""
    for char in text:
        if char.isdigit():
            number += char
        elif number:
            break
    return number

# �f�[�^���`
for line in lines:
    line = line.strip()
    if not line:
        continue

    if "����" in line:
        num = extract_number(line)
        if num:
            billing_amounts.append(num)
    elif "����" in line:
        num = extract_number(line)
        if num:
            toll_amounts.append(num)
    else:
        name = extract_surname(line)
        surnames.append(name)

# ���ׂ�1��ɕ\��
all_data = surnames + billing_amounts + toll_amounts

# �o�́i1�s��1�j
for item in all_data:
    print(item)
