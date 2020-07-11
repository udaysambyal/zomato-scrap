import requests
from bs4 import BeautifulSoup
import pandas

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

pagenum = 1
rest_list =[]

for page in range(1,10):
    
    response = requests.get("https://www.zomato.com/agra/restaurants?page={0}".format(pagenum), headers=headers)
    content = response.content
    
    soup = BeautifulSoup(content, "html.parser")
    search = soup.find_all("div", {'id': 'orig-search-list'})
    
    item = search[0].find_all("div", {'class': 'content'})
    for i in range(0,15):
        
        data={} 
        data['rest_name'] = item[i].find("a", {'data-result-type': 'ResCard_Name'}).text.replace('\n', ' ').strip()
        data['locality'] = item[i].find("b").text.replace('\n',' ').strip()
        
        ratings = item[i].find("div", {'class': 'flex align-center both-rating'})
    
        if ratings is None:
            continue
        data['ratings']=ratings.text.replace('\n',' ').strip()
        
        rest1 = item[i].find_all("div", {'class': 'search-page-text clearfix row'})
        rest2 = rest1[0].find_all("span", {'class': 'col-s-11 col-m-12 nowrap pl0'})
        rest3 = rest2[0].find_all("a")
        data['cuisines'] = [e.string for e in rest3]
        
        rest4 = rest1[0].find("div", {'class': 'res-cost clearfix'})
        if rest4 is None:
            continue
        rest5=rest4.find_all('span',{'class':'col-s-11 col-m-12 pl0'})
        data['cost_for_two']=''.join(i.text for i in rest5)
        
        rest_list.append(data)
    print('Scraped page {0}'.format(pagenum))
    pagenum+=1
print('-------------CONGRATULATIONS--------------')
print('Successfully scraped and imported to zomato_restaurants.csv')

                    # saving results to a dataframe
df = pandas.DataFrame(rest_list)
df = df[['rest_name','locality','ratings','cuisines','cost_for_two',]]
df.to_csv("zomato_restaurants.csv")
