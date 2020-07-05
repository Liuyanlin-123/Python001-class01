import requests
from bs4 import BeautifulSoup as bs
import lxml.etree
#from time import sleep
import pandas as pd
       
def get_url_name(myurl):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"

    header = {'user-agent':user_agent}

#    myurl='https://maoyan.com/films?showType=3'

    response = requests.get(myurl,headers=header)

    print(f'返回码是：{response.status_code}')

    bs_info = bs(response.text,'html.parser')

    movie_list = []

    for tags in bs_info.find_all('div',attrs={'class':'movie-hover-info'})[:10]:
        name = tags.find('span', attrs={'class': 'name'}).text
        # 电影名称
        content = tags.find_all('span', attrs={'class':'hover-tag'})
        movie_type = content[0].next_sibling.strip()   
        # 电影类型
        movie_time = content[2].next_sibling.strip()  
        # 上映时间
        movie_list.append([name, movie_type, movie_time])
    
    movies = pd.DataFrame(data=movie_list, columns=['电影名称', '电影类型', '上映时间'])
    movies.to_csv('./maoyanmovies.csv', encoding='gbk', index=False, header=False)

                        

#生成包含所有页面的元组
urls = tuple(f'https://maoyan.com/films?showType=3&offset={page * 30}' for page in range(1))
print(urls)

for page in urls:
    get_url_name(page)
    
