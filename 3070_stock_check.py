from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import re
import time

#### Checking Stock of individual store locations of GTX 3070 and GTX 3070 TI

store_dict = {
'online / main warehouse' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=PWH&mfr=&pr=",
'burlington' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=BURL&mfr=&pr=",
'st catherines' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=SCAT&mfr=&pr=",
'hamilton' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=HAM2&mfr=&pr=",
'oakville' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=OA&mfr=&pr=",
'mississauga' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=MISS&mfr=&pr=",
'waterloo' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=WATERLOO&mfr=&pr=",
'etobicoke' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=ETOB&mfr=&pr=",
'scarborough' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=1203&mfr=&pr=",
'brampton': "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=1304&mfr=&pr=",
'north york' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=NO&mfr=&pr=",
'markham' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=MU&mfr=&pr=",
'london' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=LOND&mfr=&pr=",
'vaughan' : "https://www.canadacomputers.com/index.php?sort=3b&cPath=43_557_559&sf=:3_6,3_7&loc=VAUG&mfr=&pr="}
list = []


print('Current Stock of Canada Computers for GTX 3070 and 3070ti ...' + "\n" + "-------------------------------")

### Checking each store for stock

for i in store_dict:
    raw_data = urlopen(store_dict[i])
    unparsed = raw_data.read()
    gpu_soup = soup(unparsed, 'html.parser')


### Using CSS selectors to return each GPU details, and GPU price details from HTML

    htmlstring = gpu_soup.select('#product-list > div > div  div.col-12.productImageDesc span.text-dark') 
    price = gpu_soup.select('#product-list   div div  div.col-12.productImageDesc  div  span.d-block.mb-0') 

    pattern1 = r"href=(.+?)\>"                      ### Pulling out GPU URL from HTML
    pattern2 = r"\>([A-Z].+?)\</a></span>"          ### Pulling out GPU Name from HTML
    pattern3 = r"\<strong\>(.+?)\</strong\>"        ### Pulling out GPU Price from HTML

    price = re.findall(pattern3,str(price))
    store_name = str(i).title()
    dict = {}
    gpu_name = []
    gpu_price = []
    gpu_url = []
 


    for t in range(0,len(re.findall(pattern2, str(htmlstring)))):
        gpu_name.append(str(re.findall(pattern2, str(htmlstring))[t]))
        gpu_price.append(str(price[t]))
        gpu_url.append(str(re.findall(pattern1,str(htmlstring))[t]))

        


    if len(gpu_name) == 0:
        name = str(i).title()
        list.append(store_name)


### Returning location of stocked stores and each graphics card details as soon as found

    else: 
        for t in gpu_name:
            for g in gpu_price:
                for h in gpu_url:
                    
                     print(f"In Stock at Store Location: {store_name} " + "\n" + str(t) +  "\n" + "Price: " + str(g) + "\n" + "URL: " + str(h) + "\n" + "-------------------------------")

string = ""
for i in list:
    if i == list[len(list)-1]:
        string = string + i
    else:    
        string = string + i + ", "


### Returning location of out of stock stores at the end

print("Store Locations " + string + " are Out of Stock")

