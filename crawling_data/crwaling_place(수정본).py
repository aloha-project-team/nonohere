from bs4 import BeautifulSoup
import requests
import json
import csv

from selenium import webdriver
import time
# id / 방문지 / 방문자 리뷰 수 / 블로그 리뷰수 / 전화번호 / 주소 / 운영시간 및 추가 정보 / 링크
# 방문지 / 리뷰아이디(평점 / 글)



with open('review.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(['place', 'rating', 'nickname', 'review', 'visited'])

with open('place_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(['place','name', 'sort', 'rating', 'reviews'])

with open('etc.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(['place', 'phone', 'address', 'hour', 'url'])


search = ["롯데월드", "에버랜드", "여의도 한강공원", "연희 38 애비뉴"]
# search = "롯데월드"

def make_url(search):

    # url = f"https://map.naver.com/v5/search/{search}"
    url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={search}&oquery=네이버플레이스&tqi=U2Ws%2Flp0YihssKRsK3Vssssssw0-450263"

    response = requests.get(url)

    # print(response.text)
    place_url = response.text[response.text.find("PlaceSummary:")+len("PlaceSummary:"):response.text.find("\",\"typename\":\"PlaceSummary")]
    # print(place_url)

    if len(place_url) > 100:
        # print("잘못됨")
        soup = BeautifulSoup(response.text, "html.parser")
        place_url = soup.find("a", class_="api_more_theme")["href"].split("?c=")[0].split("/")[-1]


    return place_url

def place_info(place_url, search):

    headers = {
        'authority': 'pcmap.place.naver.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    }


    response = requests.get(f'https://pcmap.place.naver.com/place/{place_url}', headers=headers)

    soup = BeautifulSoup(response.content.decode("utf-8", "replace"), "html.parser")

    name = soup.find("span", class_="_3XamX").text
    sort = soup.find("span", class_="_3ocDE").text

    review = soup.find("div", class_="_1kUrA")

    reviews = []

    for line in review.select("span"):
        if line.select_one("a") == None:
            rating = line.text
        else:
            reviews.append(line.text + ", " +line.select_one("a")["href"])
    
    with open('place_info.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerow([search, name, sort, rating, reviews])

    return {"name" : name, "sort" : sort, "rating" : rating, "reviews" : reviews}


# -------------------------------------------------------------
# print("\n---전화번호 등등---")

def etc(place_url, search):

    headers = {
        'sec-fetch-mode': 'cors',
    }

    params = (
        ('lang', 'ko'),
    )

    response = requests.get(f'https://map.naver.com/v5/api/sites/summary/{place_url}', headers=headers, params=params)

    etc = {}

    result_dict = json.loads(response.text)

    if result_dict["phone"] == None:
        etc["phone"] = ""
    else :
        etc["phone"] = result_dict["phone"]
    if result_dict["roadAddr"]["text"] == None:
        etc["address"] = ""
    else :
        etc["address"] = result_dict["roadAddr"]["text"]
    if result_dict["bizHour"] == None:
        etc["hour"] = ""
    else :
        etc["hour"] = result_dict["bizHour"][0]["type"] + result_dict["bizHour"][0]["startTime"] + "-" +result_dict["bizHour"][0]["endTime"]

    if result_dict["urlList"] == []:
        etc["url"] = ""
    else:
        etc["url"] = result_dict["urlList"][0]["url"]

    with open('etc.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerow([search, etc["phone"], etc["address"], etc["hour"], etc["url"] ])

    return etc


# 더보기 누르고싶다.....
# print("\n---더보기---")

def crawling_review(place_url , search):
    
    headers = {
        'content-type': 'application/json',
    }
    # businessId랑 page를 변경해야함

    info_list = []

    for idx in range(1, 11):
        data = '{"operationName":"getVisitorReviews","variables":{"input":{"businessId":'+f'"{place_url}"'+',"businessType":"place","item":"0","bookingBusinessId":"215255","page":'+f'{idx}'+',"display":10,"isPhotoUsed":false,"theme":"allTypes","includeContent":true},"id":"11583235"},"query":"query getVisitorReviews($input: VisitorReviewsInput) {\\n visitorReviews(input: $input) {\\n items {\\n id\\n rating\\n author {\\n id\\n nickname\\n from\\n imageUrl\\n objectId\\n url\\n __typename\\n }\\n body\\n thumbnail\\n media {\\n type\\n thumbnail\\n __typename\\n }\\n tags\\n status\\n visitCount\\n viewCount\\n visited\\n created\\n reply {\\n editUrl\\n body\\n editedBy\\n created\\n replyTitle\\n __typename\\n }\\n originType\\n item {\\n name\\n code\\n options\\n __typename\\n }\\n language\\n highlightOffsets\\n translatedText\\n businessName\\n showBookingItemName\\n showBookingItemOptions\\n bookingItemName\\n bookingItemOptions\\n __typename\\n }\\n starDistribution {\\n score\\n count\\n __typename\\n }\\n hideProductSelectBox\\n total\\n __typename\\n }\\n}\\n"}'

        response = requests.post('https://pcmap-api.place.naver.com/place/graphql', headers=headers, data=data)

        result_dict = json.loads(response.text)

        for item in response.json()["data"]["visitorReviews"]["items"]:

            info = {}

            info["rating"] = item["rating"]
            info["nickname"] = item["author"]["nickname"]
            info["review"] = str(item["body"]).replace("\n","")
            info["visited"] = item["visited"]

            with open('review.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter=csv.writer(csvfile)
                csvwriter.writerow([search, info["rating"], info["nickname"], info["review"], info["visited"]])

            info_list.append(info)

    return info_list

for s in search:
    place_url = make_url(search)
    print(place_url)
    print(place_info(place_url, s))
    print(etc(place_url, s))
    print(crawling_review(place_url, s))






