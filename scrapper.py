from helium import *
from bs4 import BeautifulSoup
from time import sleep
from datetime import date
from colorama import Fore

search = "&pagina="
url = "https://www.pcdiga.com/campanhas-e-ofertas/campanha/black-november?category=componentes"
TODAY = date.today().strftime("%Y%m%d")

def getFinalPageIndex(url):
    browser = start_firefox(url,headless=True)
    soup = BeautifulSoup(browser.page_source,'html.parser')
    ul = soup.find('ul',{'class':'flex items-center h-full gap-x-5'})
    li = ul.find_all('li')
    index = li[-1].find('button',{'class':'bg-background-off hover:bg-border-color h-9 w-9 sm:h-10 sm:w-10 rounded-sm lg:rounded-r3'}).text
    kill_browser()
    return index

def getInfo(url):
    browser = start_firefox(url,headless=True)
    soup = BeautifulSoup(browser.page_source,'html.parser')
    items = soup.find_all('div',{'class':'flex flex-col bg-background-off p-1.5 md:p-3 rounded-r4'})
    info = []

    for item in items:
        title = item.find('a',{'class':'h-8 mt-2 text-xs font-bold duration-150 rounded-md cursor-pointer md:h-12 with-tab md:text-base-sm md:leading-6 line-clamp-2 hover:text-primary'}).text
        price = item.find('div',{'class':'text-lg font-extrabold md:text-2xl text-primary'}).text
        info.append((title,price))
    
    kill_browser()
    save(info)
     
def save(data):
    print(f"Saving",end = "")
    save = open(f"./save{TODAY}","a")
    for item in data:
        print(f".",end = "")
        save.write(str(item))
        save.write(f"\n")
    save.close
    print(f"Done")

index = int(getFinalPageIndex(url))+1
for i in range(1,index):
    print(f"Getting page {i}")
    getInfo(url+search+str(i))
    sleep(1)
print(Fore.GREEN+"SCRAPE WAS SUCCESSFUL")
