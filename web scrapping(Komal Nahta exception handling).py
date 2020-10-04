from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re

url = 'https://komalsreviews.wordpress.com/2012/09/'

###Single Page
response = get(url)
html = BeautifulSoup(response.text, 'html.parser')

#blogs_on_page = html.find_all('h2', class_ = 'entry-title')
blog_titles = []

#for i in range(len(blogs_on_page[0:3])):
#    blog_title = html.find_all('h2', class_ = 'entry-title')[i].text
#    blog_titles.append(blog_title)

blog_urls_containers = html.find_all('div', class_ = 'entry-summary')
blog_urls = ['https://komalsreviews.wordpress.com/2012/09/01/jalpari-the-desert-mermaid-review/',
             'https://komalsreviews.wordpress.com/2012/09/01/from-sydney-with-love-review/',
             'https://komalsreviews.wordpress.com/2012/09/01/joker-review/']

##for i in range(len(blog_urls_containers)):
##    if(i == 1):
##        continue
##    if(i == 4):
##        continue
##    if(i == 5):
##        continue
##    if(i == 6):
##        continue
##    if(i == 7):
##        continue
##    if(i == 8):
##        continue
##    if(i == 9):
##        continue
##    print(i)
##    blog_urls.append(blog_urls_containers[i].p.a['href'])
    
blogs = []
last_paras = []
    
##for blog_url in blog_urls:
##    response_blog = get(blog_url)
##    html_blog = BeautifulSoup(response_blog.text, 'html.parser')
##
##    blog_title = html_blog.find('div', class_='entry-content').p.strong.text
##    blog_titles.append(blog_title)
##    blog_container = html_blog.find('div', class_='entry-content')
##    blog_paras = blog_container.find_all('p')
##    blog = []
##    for i in range(len(blog_paras)):
##        blog.append(blog_paras[i].text)
##        if i == len(blog_paras)-1:
##            last_para = blog_paras[i].text
##            last_paras.append(last_para)
##    blog = ' '.join(blog)
##    blogs.append(blog)
##
##
##df = pd.DataFrame({'Title': blog_titles,
##                   'Blog': blogs,
##                   'LastParagraph': last_paras
##                   })
##
##df.to_csv('C:\\Users\\Manju Pawar\\Desktop\\CP\\Data\\Komal Nahta Blogs\\Feb 2013.csv', index=False)
    
for blog_url in blog_urls:
    response_blog = get(blog_url)
    html_blog = BeautifulSoup(response_blog.text, 'html.parser')

    blog_title = html_blog.find('td', attrs = {'valign':'top'}).strong.text
    blog_titles.append(blog_title)
    blog_paras = html_blog.find_all('p')[:25]
    blog = []
    for i in range(len(blog_paras)):
        tmp_list = re.findall('On the whole,', str(blog_paras[i]))
        if(len(tmp_list)>0):
            last_para_index = i
            last_para = blog_paras[last_para_index].text
            last_paras.append(last_para)
    for i in range(last_para_index+1):
        blog.append(blog_paras[i].text)
        

    blog = ' '.join(blog)
    blogs.append(blog)


df = pd.DataFrame({'Title': blog_titles,
                   'Blog': blogs,
                   'LastParagraph': last_paras
                   })

df.to_csv('C:\\Users\\Manju Pawar\\Desktop\\CP\\Data\\Komal Nahta Blogs\\Sep 2012a.csv', index=False)
