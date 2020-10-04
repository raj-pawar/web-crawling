from requests import get
from bs4 import BeautifulSoup
import pandas as pd

common_url = 'https://komalsreviews.wordpress.com/'
#dates = ['2018/04/']

#names = ['April 2018']

urls = [common_url+dates[i] for i in range(len(dates))]

###Single Page
##url1 = urls[0]
##response = get(url1)
##html = BeautifulSoup(response.text, 'html.parser')
##
##blogs_on_page = html.find_all('h2', class_ = 'entry-title')
##blog_titles = []
##
##for i in range(len(blogs_on_page)):
##    blog_title = html.find_all('h2', class_ = 'entry-title')[i].text
##    blog_titles.append(blog_title)
##
##blog_urls_containers = html.find_all('div', class_ = 'entry-summary')
##blog_urls = []
##
##for i in range(len(blog_urls_containers)):
##    blog_urls.append(blog_urls_containers[i].p.a['href'])
##
##blogs = []
##last_paras = []
##
##for blog_url in blog_urls:
##    response_blog = get(blog_url)
##    html_blog = BeautifulSoup(response_blog.text, 'html.parser')
##
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

##response_blog = get(blog_urls[4])
##html_blog = BeautifulSoup(response_blog.text, 'html.parser' )
##a = html_blog.find('div', class_='entry-content')
##b = a.find_all('p')
##blog = []
##for i in range(len(b)):
##    blog.append(b[i].text)
##    if i == len(b)-1:
##        last_para = b[i].text
##blog = ' '.join(blog)

c = 0
for url in urls:
    response = get(url)
    html = BeautifulSoup(response.text, 'html.parser')

    blogs_on_page = html.find_all('h2', class_ = 'entry-title')
    blog_titles = []

    for i in range(len(blogs_on_page)):
        blog_title = html.find_all('h2', class_ = 'entry-title')[i].text
        blog_titles.append(blog_title)

    blog_urls_containers = html.find_all('div', class_ = 'entry-summary')
    blog_urls = []

    for i in range(len(blog_urls_containers)):
        if blog_urls_containers[i].p is not None:
            blog_urls.append(blog_urls_containers[i].p.a['href'])
        

    blogs = []
    last_paras = []

    for blog_url in blog_urls:
        response_blog = get(blog_url)
        html_blog = BeautifulSoup(response_blog.text, 'html.parser')

        blog_container = html_blog.find('div', class_='entry-content')
        blog_paras = blog_container.find_all('p')
        blog = []
        for i in range(len(blog_paras)):
            blog.append(blog_paras[i].text)
            if i == len(blog_paras)-1:
                last_para = blog_paras[i].text
                last_paras.append(last_para)
        blog = ' '.join(blog)
        blogs.append(blog)

    df = pd.DataFrame({'Title': blog_titles,
                       'Blog': blogs,
                       'LastParagraph': last_paras})
    df.to_csv('C:\\Users\\Manju Pawar\\Desktop\\New folder\\'+names[c]+'.csv', index=False)
    
    print(c)
    c = c+1
