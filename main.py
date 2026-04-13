# Исправленный код

```python
from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ

header = contacts_list[0]
contacts = contacts_list[1:]

# регулярное выражение для телефона
phone_pattern = re.compile(
    r'(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*\(?(?:доб\.?)\s*(\d+)\)?)?'
)

new_contacts = []

for contact in contacts:
    # приводим строку к нужной длине
    contact = contact[:7]

    # 1. Нормализация ФИО
    fio_parts = []
    for i in range(3):
        if contact[i]:
            fio_parts.extend(contact[i].split())

    contact[0] = fio_parts[0] if len(fio_parts) > 0 else ""
    contact[1] = fio_parts[1] if len(fio_parts) > 1 else ""
    contact[2] = fio_parts[2] if len(fio_parts) > 2 else ""

    # 2. Нормализация телефона
    phone = contact[5]
    match = phone_pattern.search(phone)
    if match:
        contact[5] = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(6):
            contact[5] += f" доб.{match.group(6)}"

    new_contacts.append(contact)

# 3. Объединение дублей
result = {}

for contact in new_contacts:
    key = (contact[0], contact[1])

    if key not in result:
        result[key] = contact
    else:
        saved = result[key]
        for i in range(len(contact)):
            if saved[i] == "" and contact[i] != "":
                saved[i] = contact[i]

contacts_list = [header] + list(result.values())

pprint(contacts_list)

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
