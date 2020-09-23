from bs4 import BeautifulSoup
import requests
import json

# id / 방문지 / 방문자 리뷰 수 / 블로그 리뷰수 / 전화번호 / 주소 / 운영시간 및 추가 정보 / 링크
# 방문지 / 리뷰아이디(평점 / 글)


search = "여의도 한강공원"

url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={search}&oquery=네이버플레이스&tqi=U2Ws%2Flp0YihssKRsK3Vssssssw0-450263"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

place_url = soup.find("a", class_="api_more_theme")["href"].split("?c=")[0].split("/")[-1]

print(place_url)

headers = {
    'authority': 'pcmap.place.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://map.naver.com/',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=B3RUSGOHANUF6; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; BMR=s=1600820696786&r=https%3A%2F%2Fm.blog.naver.com%2Fcpath%2F221783795485&r2=https%3A%2F%2Fwww.google.com%2F; nx_ssl=2; page_uid=U2WbYwprvxZsshFERMRssssssZN-451114',
}


response = requests.get(f'https://pcmap.place.naver.com/place/{place_url}', headers=headers)

soup = BeautifulSoup(response.content.decode("utf-8", "replace"), "html.parser")

print(soup.find("span", class_="_3XamX").text)
print(soup.find("span", class_="_3ocDE").text)


review = soup.find("div", class_="_1kUrA")

for line in review.select("span"):
    if line.select_one("a") == None:
        print(line.text)
    else:
        print(line.text, end=" ")
        print(line.select_one("a")["href"])
        


# print(soup.find("li", {"class" : "_1M_Iz._3xPmJ"}))
# print(soup.select("script")[2])

headers = {
    'authority': 'map.naver.com',
    'accept': 'application/json, text/plain, */*',
    'pragma': 'no-cache',
    'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
    'cache-control': 'no-cache',
    'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'content-type': 'application/json',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://map.naver.com/',
    'cookie': 'NNB=B3RUSGOHANUF6; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; BMR=s=1600820696786&r=https%3A%2F%2Fm.blog.naver.com%2Fcpath%2F221783795485&r2=https%3A%2F%2Fwww.google.com%2F; nx_ssl=2; page_uid=b0c9505a-cf13-4b5e-afbf-8acf6954f7f8; page_uid=U2WbYwprvxZsshFERMRssssssZN-451114',
}

params = (
    ('lang', 'ko'),
)

response = requests.get(f'https://map.naver.com/v5/api/sites/summary/{place_url}', headers=headers, params=params)

# soup = BeautifulSoup(response.text,"html.parser")

result_dict = json.loads(response.text)
print("전화번호 : ", end="")
print(result_dict["phone"])
print("주소 : ", end="")
print(result_dict["roadAddr"]["text"])
print("시간 : ", end="")
print(result_dict["bizHour"][0]["type"], result_dict["bizHour"][0]["startTime"], "-",result_dict["bizHour"][0]["endTime"])
print("URL : ", end="")
print(result_dict["urlList"][0]["url"])

# print(str(soup)[341:])


headers = {
    'authority': 'pcmap-api.place.naver.com',
    'accept': '*/*',
    'accept-language': 'ko',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'content-type': 'application/json',
    'origin': 'https://pcmap.place.naver.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://pcmap.place.naver.com/place/11583235/review/visitor?from=map^&ts=20200924',
    'cookie': 'NNB=B3RUSGOHANUF6; NRTK=ag^#all_gr^#1_ma^#-2_si^#0_en^#0_sp^#0; BMR=s=1600820696786^&r=https^%^3A^%^2F^%^2Fm.blog.naver.com^%^2Fcpath^%^2F221783795485^&r2=https^%^3A^%^2F^%^2Fwww.google.com^%^2F; nx_ssl=2; page_uid=U2WbYwprvxZsshFERMRssssssZN-451114',
}

data = '^[^{^\\^operationName^\\^:^\\^getVisitorReviews^\\^,^\\^variables^\\^:^{^\\^input^\\^:^{^\\^businessId^\\^:^\\^11583235^\\^,^\\^businessType^\\^:^\\^place^\\^,^\\^item^\\^:^\\^0^\\^,^\\^bookingBusinessId^\\^:^\\^215255^\\^,^\\^page^\\^:1,^\\^display^\\^:10,^\\^isPhotoUsed^\\^:false,^\\^theme^\\^:^\\^allTypes^\\^,^\\^includeContent^\\^:true^}^},^\\^query^\\^:^\\^query'

response = requests.post('https://pcmap-api.place.naver.com/place/graphql', headers=headers, data=data)



print(response)
