import requests
from bs4 import BeautifulSoup
import csv


url = "https://guahm.sen.hs.kr/18515/subMenu.do"

# 페이지의 HTML 콘텐츠 가져오기
response = requests.get(url)
response.raise_for_status()  # 요청이 성공했는지 확인

#HTML 콘텐츠 파싱
soup = BeautifulSoup(response.content, 'html.parser')

# 급식 일정과 날짜 추출
meal_schedule = []
dates = []

# 급식 일정을 포함하는 테이블 찾기
table = soup.find('table', {'class': 'tbl_type3'})

if table:
    rows = table.find_all('tr')
    for row in rows[1:]:  # 첫 번째 행은 헤더일 가능성이 높으므로 제외
        cells = row.find_all('td')
        if len(cells) >= 2:
            date = cells[0].get_text(strip=True)
            meal = cells[1].get_text(strip=True)
            dates.append(date)
            meal_schedule.append(meal)

# 데이터 CSV 파일로 저장
with open('meal_schedule.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['날짜', '식단'])
    for date, meal in zip(dates, meal_schedule):
        writer.writerow([date, meal])

print("급식 일정 'meal_schedule.csv' 저장 완료")
