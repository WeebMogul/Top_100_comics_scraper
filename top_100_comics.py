import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import numpy as np

urls = ['https://www.amazon.com/Best-Sellers-Books-Manga-Comics-Graphic-Novels/zgbs/books/4367/ref=zg_bs_pg_1?_encoding=UTF8&pg=1',
         'https://www.amazon.com/Best-Sellers-Books-Manga-Comics-Graphic-Novels/zgbs/books/4367/ref=zg_bs_pg_2?_encoding=UTF8&pg=2']

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

book_stats = []

for url in urls:

   s = HTMLSession()
   r = s.get(url,headers=headers)

   r.html.render(sleep=1)

   for i in range(1,51):
      try:
         books = r.html.xpath(f'//*[@id="zg-ordered-list"]/li[{str(i)}]/span/div/span/a/div',first=True).attrs['title']
      except:
         books = r.html.xpath(f'//*[@id="zg-ordered-list"]/li[{str(i)}]/span/div/span/a/div',first=True).text
      
      try:
         # author = r.html.xpath(f'//*[@id="zg-ordered-list"]/li[{str(i)}]/span/div/span/div[1]/span',first=True).text
         author = r.html.xpath(f'//*[@id="zg-ordered-list"]/li[{str(i)}]/span/div/span/div[1]/a',first=True).text
      except:
         author = 'No author'
      
      try:
         ratings = r.html.xpath(f'//*[@id="zg-ordered-list"]/li[{str(i)}]/span/div/span/div[2]/a[1]/i',first=True).text
      except:
         ratings = 'No ratings'

      try:
         # price = r.html.xpath(f'//*[@id="zg-ordered-list"]/li[{str(i)}]/span/div/span/div[4]/a/span/span',first=True).text
         # price = r.html.xpath(f'//*[@id="zg-ordered-list"]/li[{str(i)}]/span/div/span/div[3]/a/span/span',first=True).text
         # //*[@id="zg-ordered-list"]/li[11]/span/div/span/div[4]/a/span/span
         price = r.html.find('span.p13n-sc-price')[i-1].text.strip().replace('$','')
      except:
         price = "No price"
      # except :
      #    price = r.html.xpath(f'//*[@id="zg-ordered-list"]/li[{str(i)}]/span/div/span/a[2]/span/span/span',first=True).text
      
      book_info = {'Books':books, 'Author':author, 'Ratings':ratings, 'Price':price}
      book_stats.append(book_info)


df = pd.DataFrame(book_stats)
df.index = np.arange(1,len(df) + 1)
# df = df.rename(columns={' ','Rank'})
df.to_csv('Top 100 Manga.csv')




