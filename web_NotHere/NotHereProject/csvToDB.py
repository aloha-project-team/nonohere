import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NotHereProject.settings")
django.setup()

from NotHereApp.models import StoreDB, ReviewDB, StoreDB2

CSV_PATH ="./Yes.csv"
CSV_PATH2=".\last_review.csv"
CSV_PATH3 ="./No.csv"
#csv 파일 확정되면 경로 설정()
#poster까지 병합된 파일 기준으로 작성 가져오기

count = 0
with open(CSV_PATH, newline='', encoding='UTF8') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        
        StoreDB.objects.create(
            name = row['Name'],
            visitors_reviews = row['Visitors'],
            blog_reviews = row['Blog'],
            call = row['Call'],
            address = row['Address'],
            operation = row['Operation'],
            naver_link = row['Naver_link'],
            score =row['star_score'],
            category = row['Category'],
            # addcode =row[''],
            # predict=row['']
        )
        count += 1

        if count % 100 == 0:
            print(count)

print(count)
print('store DB end')

count = 0
with open(CSV_PATH2, newline='', encoding='UTF8') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        
        ReviewDB.objects.create(
            # review_id = row['movie_id'],
            store_name = row['place'],
            nickname = row['nickname'],
            score = row['rating'],
            text = row['review'],
            date = row['visited'],
        )
        count += 1

        if count % 100 == 0:
            print(count)

print(count)
print('review DB end')

count = 0
with open(CSV_PATH3, newline='', encoding='UTF8') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        
        StoreDB2.objects.create(
            name = row['Name'],
            visitors_reviews = row['Visitors'],
            blog_reviews = row['Blog'],
            call = row['Call'],
            address = row['Address'],
            operation = row['Operation'],
            naver_link = row['Naver_link'],
            score =row['star_score'],
            category = row['Category'],
            # addcode =row[''],
            # predict=row['']
        )
        count += 1

        if count % 100 == 0:
            print(count)

print(count)
print('store DB2 end')