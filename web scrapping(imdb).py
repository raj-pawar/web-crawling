'''Script to scrape information of top 50 movies by popularity released in a particular year from the advanced search page of imdb.
Same code can be used for any advanced search query on the imdb page by changing the variable named 'url' below with the url of the page to be scrapped.'''

## Importing the required libraries
from requests import get
from bs4 import BeautifulSoup

## Fetching the HTML code of the web-page and creating a BeautifulSoup object from it
#url = 'https://www.imdb.com/search/title?title_type=feature&release_date=2012-01-01,2012-12-31&countries=in&languages=hi&count=100'
base_url = 'https://www.imdb.com/search/title?title_type=feature&release_date='
end_url = '&countries=in&languages=hi&count=50'
years = ['2012','2013','2014','2015','2016','2017']

for year in years:
    url = base_url+year+'-01-01,'+year+'-12-31'+end_url
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    print(url)
    ## Storing the html code for each movie container on the page as seperate elements in the list after identifying it's unqiue class on the webpage 
    movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

    ## Creating empty lists to store scrapped information
    names = []
    ids = []
    metascores = []
    genres = []
    casts = []
    #directors = []
    #actors = []
    plots = []
    certificates = []
    runtimes = []
    collections = []
    imglinks = []
    imdbratings = []
    check = []
    votes = []
    production_years = []

    import re

    ## Loop to go through each container containing a movie on the page

    for container in movie_containers:

        ## Extracting various information from the container and storing it in
        ## seperate lists
        #Movie names
        name = container.h3.a.text
        names.append(name)
        #tconst ids
        mid = container.div.find('div', attrs = {'class':'ribbonize'})['data-tconst']
        ids.append(mid)
        print(container.h3.a.text)
        #Movie Genres
        if container.find('span', class_ = 'genre') is not None:
            genre = container.find('span', class_ = 'genre').text.split("\n")[1]
            genres.append(genre)
        else:
            genres.append("NA")
        #Plot
        try:
            plot = container.find('div', class_ = "lister-item-content").find_all('p', class_ = "text-muted")[1].text.split("\n")[1]
            plots.append(plot)
        except:
            plots.append('NA')
        #Cast
        try:
            cast = container.find_all('p')[2].text
            casts.append(cast)
        except:
            casts.append('NA')
        #Directors and Actors
        #tmp = container.find_all('p')
        #tmp = str(tmp[2])
        #tmp = tmp.split("|")
        #director = re.findall(r"[A-Z]\w+ [A-Z]\w+",tmp[0])
        #director = ', '.join(director)
        #directors.append(director)

        #actor = re.findall(r"[A-Z]\w+ [A-Z]\w+",tmp[len(tmp)-1])
        #actor = ', '.join(actor)
        #actors.append(actor)

        #Image Links
        try:
            imglink = container.img['loadlate']
            imglinks.append(imglink)
        except:
            imglinks.append('NA')
        #Metascores
        if container.find('div', class_ = 'ratings-metascore') is not None:
            m_score = container.find('span', class_ = 'metascore').text
            metascores.append(int(m_score))
        else:
            metascores.append(int(-1))
        #Certificate
        if container.find('span', class_ = "certificate") is not None:
            certificate =  container.find('span', class_ = "certificate").text
            certificates.append(certificate)
        else:
            certificates.append("NA")
        #Runtime
        if container.find('span', class_ = "runtime") is not None:
            runtime = container.find('span', class_ = "runtime").text
            runtimes.append(runtime)
        else:
            runtimes.append("NA")

        #Gross collections
        if len(container.find_all('span', attrs = {'name':'nv'}))<2:
            collections.append("NA")
        else:
            collection = container.find_all('span', attrs = {'name':'nv'})[1]['data-value']
            collections.append(collection)

        #IMDB Rating
        if container.strong is not None:
            imdbrating = container.strong.text
            imdbratings.append(imdbrating)
        else:
            imdbratings.append('NA')
        #No. of Votes
        if container.find('span', attrs= {'name':'nv'}) is not None:
            vote = container.find('span', attrs= {'name':'nv'})['data-value']
            votes.append(vote)
        else:
            votes.append('NA')

        #Production Year
        if container.find('span', class_ = 'lister-item-year') is not None:
            production_year = container.find('span', class_ = 'lister-item-year').text
        else:
            production_year.append('NA')
        #Data Cleaning
        production_year = production_year.replace('(','')
        production_year = production_year.replace(')','')
        production_year = production_year.replace('I ','')
        production_year = production_year.replace('II ','')
        production_year = production_year.replace('I','')
        production_year = production_year.replace('II','')
        production_years.append(production_year)
        
    #Director and Actors column check
    #for i in range(len(actors)):
    #    if(actors[i]==directors[i]):
    #        check.append(i+2)
    #    if(actors[i] == ""):
    #        check.append(i+2)
    #    if(directors[i] == ""):
    #        check.append(i+2)

    #check = set(check)
    #print("These Director and Actors rows are messed up (excel index)\n")
    #print(check)

    #Data cleaning
    for i in range(len(movie_containers)):
        casts[i] = re.sub('\s',' ',casts[i])

    # Loop to fetch release dates from individual movie page using movie's imdb id
    common_url = 'https://www.imdb.com/title/'
    release_dates = []
    for movie_id in ids:
        movie_url = common_url+movie_id+'/'
        response_movie = get(movie_url)
        movie_html = BeautifulSoup(response_movie.text, 'html.parser')
        release_date = movie_html.find('a', attrs = {'title':'See more release dates'}).text
        release_date = release_date.replace('\n', '')
        release_dates.append(release_date)


    # Storing all the information in a dataframe
    import pandas as pd

    df = pd.DataFrame({'tconst': ids,
                       'movie': names,
                       'metascore': metascores,
                       'genre': genres,
                       'cast': casts,
                       'plot': plots,
                       'certificate': certificates,
                       'runtime': runtimes,
                       'grosscollection': collections,
                       'imglinks': imglinks,
                       'imdbrating': imdbratings,
                       'noofvotes': votes,
                       'production_year': production_years,
                       'release_date': release_dates
                       })
    #Exporting the dataframe to a csv file
    df.to_csv('C:\\Users\\Manju Pawar\\Desktop\\imdb'+year+'.csv', index=False)
    print(year)

# Checking and going through the variables of the dataframe to ensure sanity of data
##print("Cast")
##print(df['cast'].describe())
##print("Certificate")
##print(df['certificate'].describe())
##print("Genre")
##print(df['genre'].describe())
##print("Gross Collection")
##print(df['grosscollection'].describe())
##print("Image Links")
##print(df['imglinks'].describe())
##print("Metascores")
##print(df['metascore'].unique())
##print("Plot")
##print(df['plot'].describe())
##print("Runtime")
##print(df['runtime'].describe())
##print("tconst")
##print(df['tconst'].describe())
##print(df.head())
