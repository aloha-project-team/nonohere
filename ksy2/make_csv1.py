import csv
import pandas as pd
import re

def csv_make():
    with open("basic.csv","w",newline="",encoding="utf-8") as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerow(['Name','Call','Address','Operation','Naver_link','rank'])
        
basic_df=pd.read_csv('./place_info.csv')
etc_df=pd.read_csv('./etc.csv')

csv_make()
idx = 0

with open('basic.csv', 'a', newline='', encoding='utf-8') as csvfile:
    csvwriter=csv.writer(csvfile)
    # csvwriter.writerow([music, singer])

    for name in basic_df["name"]:
        
        input_list=[]
        input_list.append(name)
        
        phone=etc_df['phone'][idx]
        input_list.append(phone)
        
        input_list.append(etc_df['address'][idx])
        input_list.append(etc_df['hour'][idx])
        input_list.append(etc_df['url'][idx])
        csvwriter.writerow(input_list)
        idx+=1
   
   # 평점
    star_list = []
    for star in basic_df["rating"]:
        star_list.append(int(star[:1]))
    # 업종(categoty)
    categoty_list = []
    for c in basic_df["sort"]:
        categoty_list.append(c)

    visitor_list = []
    blog_list = []

    for df in basic_df['reviews']:
        a=df.replace(',','') # ',' 을 없앰
        b=a.replace('\'방문자리뷰 ','')
        c=b.replace('\'블로그리뷰 ','')
        pattern = '/\w*/\d*/\w*/\w*'
        text = re.sub(pattern=pattern, repl='',string=c)

        pattern = '\s\'\s'
        text1 = re.sub(pattern=pattern, repl=',',string=text)
        text1=text1.replace(' \'','')
        text1=text1.replace('[','')
        text1=text1.replace(']','')
        visitor, blog = text1.split(',')
        visitor = int(visitor)
        blog = int(blog)
        visitor_list.append(visitor)
        blog_list.append(blog)

# basi.csv에 저장
df_a=pd.read_csv('./basic.csv')
df_a['star_score']=star_list
df_a['Visitors']= visitor_list
df_a['Blog']= blog_list
df_a['Category']= categoty_list
# csv로 저장
df_a.to_csv("./final.csv",index=False, mode='w')



final_df=pd.read_csv('./final.csv')
# Name,Call,Address,Operation,Naver_link,Visitors,Blog

# basic_df=pd.read_csv('./place_info.csv')


# 순위 측정 알고리즘 

# 스코어 저장 리스트
star_score=[]

# 2개의 리뷰 갯수를 더한 값을 저장한 리스트
total_review=[]

# place   name  sort  rating  reviews
# reviews '방문자리뷰 33,267, /place/11583235/review/visitor', '블로그리뷰 7997




# 중복 제거
df_d= final_df.drop_duplicates(["Category"])
# print(df_d)
c_list=[]
for df in df_d["Category"]:
    c_list.append(df)
count=len(c_list)
review_sum_list=[0 for x in range(count)]



# 2개의 리뷰를 더한 전체 갯수를 구해줌
for i in range(len(c_list)):
    idx=0
    for df in final_df['Category']:
        if(df == c_list[i]):
            review_sum_list[i]+=final_df['Visitors'][idx]
            review_sum_list[i]+=final_df['Blog'][idx]
        idx+=1

a_list=[]
for i in range(len(c_list)):
    idx=0
    for df in final_df['Category']:
        if(df == c_list[i]):
            aa=(final_df['Visitors'][idx]+final_df['Blog'][idx]) / review_sum_list[i]
            # print(aa)
            bb=aa*final_df['star_score'][idx]*0.2
            # print(bb)
            result=aa+bb
            # result=round(result,2)
            # print(aa,bb)
            # final_df['rank'][idx]=result
            # print(result)
            # print()
            a_list.append(result)
        idx+=1
final_df['rank']=a_list

final_df.to_csv("./final.csv",index=False, mode='w')
# 수정된 분류 점수 알고리즘
# a= 현재 리뷰수 / 전체 리뷰수
# b= a* 0.(별점)
# result = a-b

# 리뷰수가 많으면 1에 가까워지고, 
# a를 기준으로 별점이 낮으면 0에 가까워진다.
# 결과 1에 가까운 값이 출력

# 리뷰수가 적으면 0에 가까워지고
# 별점이 높으면 0에 근사값이 나온다.
# 결과 0에 가까운 값이 출력



# for a in review_sum_list:
#     print(a)
# for df in df_d[""]:

# one_score_list=[0 for x in range(count)]

    # one_score= review_sum_list[i]
    
    # 실수2자릿수까지 표현하고 반올림
    # one_score=round(one_score,2)
    # print(one_score)
# for i in range(len(total_review)):
#     a=total_review[i]*one_score + star_score[i]
#     rank_list.append(a)


# print(rank_list) # 랭크를 매길 수 있는 점수 리스트


# with open("rank.csv","w",newline="",encoding="utf-8") as csvfffile:
#     csvwriter=csv.writer(csvfffile)
#     csvwriter.writerow(['name','catagory','rank_score','recent_review','total_review'])

# with open("rank.csv","a",newline="",encoding="utf-8") as csvffffile:
#     csvwriter=csv.writer(csvffffile)
#     for i in range(len(total_review)):
#         csvwriter.writerow([basic_df['name'][i],basic_df['catagory'][i],rank_list[i],total_review[i],sum(total_review[:])])

fainal_df=pd.read_csv('./final.csv')
# pandas 오름차순 정리
df_sorted_by_value = fainal_df.sort_values(by='rank', ascending=False)
# csv로 저장
df_sorted_by_value.to_csv("./No.csv",index=False, mode='w')

# pandas 내림차순 정리
df_sorted_by_value1 = fainal_df.sort_values(by='rank')
# csv로 저장
df_sorted_by_value1.to_csv("./Yes.csv",index=False, mode='w')