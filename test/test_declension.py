import json
import requests

API_URL = "http://127.0.0.1:8000/decline"

with open("test_cases.json", encoding="utf-8") as f:
    TEST_CASES = json.load(f)

print(f"Запускаем тесты, всего кейсов: {len(TEST_CASES)}")

errors = []
for case in TEST_CASES:
    response = requests.post(API_URL, json={
        "fio": case["original"],
        "case": case["case"]
    })
    if response.status_code != 200:
        errors.append(f"{case['original']} ({case['case']}): HTTP {response.status_code}")
        continue

    result = response.json()
    declined = result.get("declined")
    if declined != case["expected"]:
        errors.append(f"{case['original']} ({case['case']}): expected '{case['expected']}', got '{declined}'")

if errors:
    print("Ошибки склонения:")
    for e in errors:
        print(" -", e)
    raise AssertionError("Есть ошибки склонения!")
else:
    print("Все тесты пройдены ✅")
