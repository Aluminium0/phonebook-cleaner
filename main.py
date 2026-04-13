from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)

# --- решение ---

header = contacts_list[0]
contacts = contacts_list[1:]

# 1. Приводим ФИО в порядок
for contact in contacts:
    fio = " ".join(contact[:3]).split()
    contact[0] = fio[0]
    contact[1] = fio[1] if len(fio) > 1 else ""
    contact[2] = fio[2] if len(fio) > 2 else ""

# 2. Приводим телефоны к формату
pattern = r'(\+7|8)\D*(\d{3})\D*(\d{3})\D*(\d{2})\D*(\d{2})(\D*(\d+))?'

for contact in contacts:
    contact[5] = re.sub(
        pattern,
        r'+7(\2)\3-\4-\5 доб.\7' if "доб" in contact[5] else r'+7(\2)\3-\4-\5',
        contact[5]
    ).strip()

# 3. Убираем дубли
result = {}

for contact in contacts:
    key = contact[0] + contact[1]
    if key not in result:
        result[key] = contact
    else:
        old = result[key]
        for i in range(len(contact)):
            if old[i] == "":
                old[i] = contact[i]

contacts_list = [header] + list(result.values())

pprint(contacts_list)

# запись
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(contacts_list)
