from requests import get
from bs4 import BeautifulSoup

#url = 'https://timesofindia.indiatimes.com/entertainment/hindi/movie-reviews'
#response = get(url)

with open('C:\\Users\\Manju Pawar\\Desktop\\response.txt', 'r') as myfile:
    response=myfile.read()
html = BeautifulSoup(response, 'html.parser')
movie_containers = html.find_all('div', class_ = 'mr_lft_box')
titles = []
movie_review_urls = []
TOIratings1 = []
TOIratings2 = []
certificates = []

for movie in movie_containers:
    #Movie name
    title = movie.h3.text
    titles.append(title)
    #Rating 1
    rating1 = movie.find_all('div', class_ = 'mrB10 clearfix')[0].text
    TOIratings1.append(rating1)
    #Rating 2
    rating2 = movie.find_all('div', class_ = 'mrB10 clearfix')[1].text
    TOIratings2.append(rating2)
    #Movie Certificates
    certificate = movie.find_all('div', class_ = 'mrB10 clearfix')[2].text
    certificates.append(certificate)
    #Movie Review Page IDS
    movie_review_id = movie.find('div', class_ = 'FIL_right').a['href']
    movie_review_urls.append('https://timesofindia.indiatimes.com'+movie_review_id)


c = 0

toi_reviews = []
in_depth_analyses = []
mumbai_mirror_reviews = []
mm_ratings = []
TOIauthors = []
mmauthors = []


for url in movie_review_urls:
    movie_review_response = get(url)
    html_review = BeautifulSoup(movie_review_response.text, 'html.parser')

    if html_review.find('div', class_ = 'Normal') is not None:
        toi_review = html_review.find('div', class_ = 'Normal').text
        toi_reviews.append(toi_review)
    else:
        toi_reviews.append("NA")

    if html_review.find('span', class_ = 'md_byline') is not None:
        author = html_review.find('span', class_ = 'md_byline').text
        TOIauthors.append(author)
    else:
        TOIauthors.append("NA")
        
    if len(html_review.find_all('div', class_ = 'depth_anlys_left clearfix')) > 0:
            
        in_depth_analysis = html_review.find_all('div', class_ = 'depth_anlys_left clearfix')
        
        l = []
        for i in range(len(in_depth_analysis)):
            l.append(in_depth_analysis[i].text)
        tmp_string = ''.join(l)
        in_depth_analyses.append(tmp_string)
    else:
        in_depth_analyses.append("NA")

    
    mumbai_mirror_response = get(url+'?filter=mumtab')
    html_mumbai_mirror = BeautifulSoup(mumbai_mirror_response.text, 'html.parser')
    if html_mumbai_mirror.find('div', class_ = 'Normal') is not None:
        mumbai_mirror_review = html_mumbai_mirror.find('div', class_ = 'Normal').text
        mumbai_mirror_reviews.append(mumbai_mirror_review)
    else:
        mumbai_mirror_reviews.append("NA")

    if html_mumbai_mirror.find('span', class_='critc_txt') is not None:
        mm_rating = html_mumbai_mirror.find('span', class_='critc_txt').text
        mm_ratings.append(mm_rating)
    else:
        mm_ratings.append('NA')

    if html_mumbai_mirror.find('span',class_='md_byline') is not None:
        mmauthor = html_mumbai_mirror.find('span',class_='md_byline').text
        mmauthors.append(mmauthor)
    else:
        mmauthors.append('NA')

    print(c)
    c = c + 1
    
    
import pandas as pd

df = pd.DataFrame({'Name': titles,
                   'TOIReviewURL': movie_review_urls,
                   'TOIRating1': TOIratings1,
                   'TOIRating2': TOIratings2,
                   'MovieInfo': certificates,
                   'TOIReview': toi_reviews,
                   'TOIScoring': in_depth_analyses,
                   'TOIauthor': TOIauthors,
                   'MMReview': mumbai_mirror_reviews,
                   'MMRatings': mm_ratings,
                   'MMauthor': mmauthors})

df.to_csv('C:\\Users\\Manju Pawar\\Desktop\\TOI&MMreviews1.csv', index=False)
