import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NotHereProject.settings")
django.setup()

from NotHereApp.models import StoreDB, ReviewDB

CSV_PATH =".\MovieData_new.csv"
# CSV_PATH2=".\last_review.csv"
#csv 파일 확정되면 경로 설정()
#poster까지 병합된 파일 기준으로 작성 가져오기

count = 0
with open(CSV_PATH, newline='', encoding='UTF8') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        
        StoreDB.objects.create(
            store_id = row['movie_id'],
            name = row['title'],
            visitors_reviews = row['rating'],
            blog_reviews = row['genres'],
            call = row['running_time'],
            address = row['opening_date'],
            operation = row['director'],
            naver_link = row['appearances'],
            score =row['gender_age_rating'],
            category = row['poster_link'],
            addcode =row[''],
            predict=row['']
        )
        count += 1

        if count % 100 == 0:
            print(count)

print(count)
print('store DB end')

# count = 0
# with open(CSV_PATH2, newline='', encoding='UTF8') as csvfile:
#     data_reader = csv.DictReader(csvfile)
#     for row in data_reader:
        
#         ReviewDB.objects.create(
#             # review_id = row['movie_id'],
#             store_name = row['place'],
#             nickname = row['nickname'],
#             score = row['rating'],
#             text = row['review'],
#             date = row['visited'],
#         )
#         count += 1

#         if count % 100 == 0:
#             print(count)

# print(count)
# print('review DB end')