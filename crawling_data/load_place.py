from bs4 import BeautifulSoup
import requests
import json
import csv

from fake_useragent import UserAgent

cities = ["서울", "부산", "대구", "인천", "광주", "대전", "울산"]
sorts = ["식당", "카페", "영화관", "공원", "액티비티", "숙소", "마트"]

with open('place.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(["city", "sort", "place"])


for city in cities:
    print()
    print(city)
    

    for sort in sorts:

        print()
        print(sort)
    
        ua = UserAgent()

        headers = {
            'user-agent': str(ua.random),
        }

        params = (
            ('query', city+" "+sort),
        )

        response = requests.get('https://pcmap.place.naver.com/place/list', headers=headers, params=params)

        soup = BeautifulSoup(response.content.decode("utf-8", "replace"), "html.parser")

        ul_list = soup.find("ul", class_="undefined")

        if sort !="식당" and sort !="카페":

            if city == "부산" or city == "광주" or city =="대구":
                for line in ul_list:
                    # print(line.find("span", class_="es3Ot").text)
                    line = line.find("span", class_="es3Ot")
                    if line == None:
                        pass
                    else:
                        place = line.text
                        print(place)
                        with open('place.csv', 'a', newline='', encoding='utf-8') as csvfile:
                            csvwriter=csv.writer(csvfile)
                            csvwriter.writerow([city, sort, place])    

            
            elif city != "부산":

                for line in ul_list:
                    # print(line.find("div", class_="_1hEhO"))
                    line = line.find("div", class_="_1hEhO")
                    if line == None:
                        pass
                    else:
                        place = line.select_one("div > a > span").text
                        print(place)

                        with open('place.csv', 'a', newline='', encoding='utf-8') as csvfile:
                            csvwriter=csv.writer(csvfile)
                            csvwriter.writerow([city, sort, place])
        
        if sort == "식당" or sort == "카페":

            if city == "울산" or city == "부산" or city =="서울" or city == "인천":

                for line in ul_list:
                    # print(line.find("span", class_="es3Ot").text)
                    line = line.find("span", class_="es3Ot")
                    if line == None:
                        pass
                    else:
                        place = line.text
                        print(place)
                        with open('place.csv', 'a', newline='', encoding='utf-8') as csvfile:
                            csvwriter=csv.writer(csvfile)
                            csvwriter.writerow([city, sort, place])    

            if city =="대전":
                for line in ul_list:
                    # print(line.find("span", class_="_2EZQu").text)
                    line = line.find("span", class_="_2EZQu")
                    if line == None:
                        pass
                    else:
                        place = line.text
                        print(place)
                        with open('place.csv', 'a', newline='', encoding='utf-8') as csvfile:
                            csvwriter=csv.writer(csvfile)
                            csvwriter.writerow([city, sort, place])                        

            else :
            
                for line in ul_list:
                    line = line.find("div", class_="_1IVzZ")
                    # line = line.find("span", class_="es3Ot")
                    if line == None:
                        pass
                    else:
                        place = line.select_one("a > div > div > span").text
                        # place = line.text
                        print(place)
                        
                        with open('place.csv', 'a', newline='', encoding='utf-8') as csvfile:
                            csvwriter=csv.writer(csvfile)
                            csvwriter.writerow([city, sort, place])


# ua = UserAgent()

# headers = {
#     'user-agent': str(ua.random),
# }

# params = (
#     ('query', "대구 숙소"),
# )

# response = requests.get('https://pcmap.place.naver.com/place/list', headers=headers, params=params)

# soup = BeautifulSoup(response.content.decode("utf-8", "replace"), "html.parser")

# # print(soup.find("ul", class_="undefined"))
# ul_list = soup.find("ul", class_="undefined")

# for line in ul_list:
# #     # print(line.find("span", class_="es3Ot").text)
#     line = line.find("span", class_="es3Ot")
#     if line == None:
#         pass
#     else:
#         print(line.text)