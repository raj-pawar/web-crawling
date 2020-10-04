'''Script to scrape information on all the movies available on the website https://www.boxofficeindia.com
At the time of scrapping the website contained around 3700 odd movies with the ids ranging from 1 to 3749
For further use the variable list 'ids' should be changed accordingly as per the range of ids present on the website'''

# Importing the required libraries
from requests import get
from bs4 import BeautifulSoup
import re

## Creating all the urls for the movies and storing them in a list  
ids = list(range(1,3749))
ids = [str(ids[i]) for i in range(len(ids))]
urls = ["https://www.boxofficeindia.com/movie.php?movieid="+ids[i] for i in range(len(ids))]

## Creating empty lists to store all the scrapped information
titles = []
mids = []
verdicts = []
dates = []
screenslist = []
first_day_collections = []
opening_notes = []
first_weekend_collections = []
first_week_collections = []
budgets = []
india_gross_collections = []
overseas_gross_collections = []
worldwide_gross_collections = []
all_time_ranks = []
footfalls = []
adj_net_gross_collections = []
overseas_first_weekend_collections = []
worldwide_first_weekend_collections = []
overseas_first_week_collections = []
worldwide_first_week_collections = []
Production_House_Information = []
Crew_Information = []
india_collections = []
mumbai_collections = []
delhiandup_collections = []
eastpunjab_collections = []
rajasthan_collections = []
cpberar_collections = []
ci_collections = []
nizamandandhra_collections = []
mysore_collections = []
tamilnandkerala_collections = []
bihar_collections = []
westbengal_collections = []
assam_collections = []
orrisa_collections = []
box_office_notes = []

## Loop to go through each url in the urls list and scrape the data available on that page.
for url in urls:
    # Fetching HTML document for the url
    response = get(url)
    # Creating BeautifulSoup object from the fetched html document
    html = BeautifulSoup(response.text, 'html.parser')

    # To check if its a valid url, skip url if it is not
    if html.find('div', class_ = 'bl_tle_mvi blue_tlte') is not None:
        title = html.find('div', class_ = 'bl_tle_mvi blue_tlte').text
        titles.append(title)
    else:
        continue

    # Scrapping data on the page and appending it to appropriately named lists
    
    movieid = re.findall(r'\d+', str(html.find('div', class_ = 'bl_tle_mvi blue_tlte').a['href']))[0]
    mids.append(movieid)

    verdict = html.find('strong').text
    verdicts.append(verdict)
    
    date = html.find('span', class_='redtext').text
    dates.append(date)

    Primary_Stats = html.find_all('div', class_ ='movieboxssec')[1]

    screens = Primary_Stats.find_all('td', class_ = 'td_cst_wd')[1].text
    screenslist.append(screens)
    
    first_day = Primary_Stats.find_all('td')[5].text
    first_day_collections.append(first_day)
    
    opening_note = Primary_Stats.find_all('td')[8].text
    opening_notes.append(opening_note)
    
    first_weekend = Primary_Stats.find_all('td')[11].text
    first_weekend_collections.append(first_weekend)

    Movie_Sales = html.find_all('div', class_ = 'movieboxssec')[3]

    first_week = Movie_Sales.find_all('td', class_ = "td_cst_wd")[1].text
    first_week_collections.append(first_week)

    budget = Movie_Sales.find_all('td')[6].text
    budgets.append(budget)
    
    india_gross = Movie_Sales.find_all('td')[9].text
    india_gross_collections.append(india_gross)
    
    overseas_gross = Movie_Sales.find_all('td')[12].text
    overseas_gross_collections.append(overseas_gross)
    
    worldwide_gross = Movie_Sales.find_all('td')[15].text
    worldwide_gross_collections.append(worldwide_gross)

    all_time_rank = Movie_Sales.find_all('td')[20].text
    all_time_ranks.append(all_time_rank)

    footfall = Movie_Sales.find_all('td')[24].text
    footfalls.append(footfall)

    adj_net_gross = Movie_Sales.find_all('td')[28].text
    adj_net_gross_collections.append(adj_net_gross)

    First_Week_Sales = html.find('table', class_ = "hide_in_mobile")

    overseas_first_weekend = First_Week_Sales.find_all('td')[4].text
    overseas_first_weekend_collections.append(overseas_first_weekend)

    worldwide_first_weekend = First_Week_Sales.find_all('td')[5].text
    worldwide_first_weekend_collections.append(worldwide_first_weekend)
    
    overseas_first_week = First_Week_Sales.find_all('td')[6].text
    overseas_first_week_collections.append(overseas_first_week)

    worldwide_first_week = First_Week_Sales.find_all('td')[7].text
    worldwide_first_week_collections.append(worldwide_first_week)

    Production_House_Info = html.find('div', class_ ="movieboxssec bluelink movieim7 pro_cst_cls").text
    Production_House_Information.append(Production_House_Info)
    
    Crew_Info = html.find('table', class_= "actrsmovie").text
    Crew_Information.append(Crew_Info)

    Territory_Sales = html.find_all('div', class_ = 'boxlisting2 bluelink firstrow')

    india_sales = Territory_Sales[0].find_all('td')[1].text
    india_collections.append(india_sales)

    mumbai_sales = Territory_Sales[1].find_all('td')[1].text
    mumbai_collections.append(mumbai_sales)

    delhiandup_sales = Territory_Sales[2].find_all('td')[1].text
    delhiandup_collections.append(delhiandup_sales)
    
    eastpunjab_sales = Territory_Sales[3].find_all('td')[1].text
    eastpunjab_collections.append(eastpunjab_sales)
    
    rajasthan_sales = Territory_Sales[4].find_all('td')[1].text
    rajasthan_collections.append(rajasthan_sales)

    cpberar_sales = Territory_Sales[5].find_all('td')[1].text
    cpberar_collections.append(cpberar_sales)

    ci_sales = Territory_Sales[6].find_all('td')[1].text
    ci_collections.append(ci_sales)

    nizamandandhra_sales = Territory_Sales[7].find_all('td')[1].text
    nizamandandhra_collections.append(nizamandandhra_sales)

    mysore_sales = Territory_Sales[8].find_all('td')[1].text
    mysore_collections.append(mysore_sales)

    tamilnandkerala_sales = Territory_Sales[9].find_all('td')[1].text
    tamilnandkerala_collections.append(tamilnandkerala_sales)

    bihar_sales = Territory_Sales[10].find_all('td')[1].text
    bihar_collections.append(bihar_sales)

    westbengal_sales = Territory_Sales[11].find_all('td')[1].text
    westbengal_collections.append(westbengal_sales)

    assam_sales = Territory_Sales[12].find_all('td')[1].text
    assam_collections.append(assam_sales)

    orrisa_sales = Territory_Sales[13].find_all('td')[1].text
    orrisa_collections.append(orrisa_sales)

    if len(html.find_all('div', 'moviegraybox bluelink'))>1:
        box_office_note = html.find_all('div', 'moviegraybox bluelink')[1].text
        box_office_notes.append(box_office_note)
    else:
        box_office_notes.append("NA")

    print(title)
    print(url)
            

# Creating dataframe from the scrapped data and exporting it to a csv file
import pandas as pd

df = pd.DataFrame({'BoxOfficeIndiaID': mids,
                   'ReleaseDate': dates,
                   'BOIVerdict': verdicts,
                   'Title': titles,
                   'Screens': screenslist,
                   'FirstDayCollection': first_day_collections,
                   'OpeningNote': opening_notes,
                   'FirstWeekendCollection': first_weekend_collections,
                   'FirstWeekCollection': first_week_collections,
                   'Budget': budgets,
                   'IndiaGrossCollection': india_gross_collections,
                   'OverseasGrossCollection': overseas_gross_collections,
                   'WorldwideGrossCollection': worldwide_gross_collections,
                   'AllTimeRankBOI': all_time_ranks,
                   'Footfall': footfalls,
                   'AdjustedNetGrossCollection': adj_net_gross_collections,
                   'OverseasFirstWeekendCollection': overseas_first_weekend_collections ,
                   'WorldwideFirstWeekendCollection': worldwide_first_weekend_collections ,
                   'OverseasFirstWeekCollection': overseas_first_weekend_collections ,
                   'WorldwideFirstWeekCollection': worldwide_first_week_collections ,
                   'ProductionHouses': Production_House_Information ,
                   'Crew': Crew_Information ,
                   'IndiaCollection': india_collections ,
                   'MumbaiCollection': mumbai_collections ,
                   'DelhiAndUPCollection': delhiandup_collections ,
                   'EastPunjabCollection': eastpunjab_collections ,
                   'RajasthanCollection': rajasthan_collections ,
                   'CPBerarCollection': cpberar_collections ,
                   'CICollection': ci_collections ,
                   'NizamAndAndhraCollection': nizamandandhra_collections ,
                   'MysoreCollection': mysore_collections,
                   'TamilNaduAndKeralaCollection': tamilnandkerala_collections ,
                   'BiharCollection': bihar_collections ,
                   'WestBengalCollection': westbengal_collections,
                   'AssamCollection': assam_collections,
                   'OrrisaCollection':orrisa_collections,
                   'BoxOfficeNote': box_office_notes})

df.to_csv('C:\\Users\\Manju Pawar\\Desktop\\BOIscrappeddata.csv', index=False)
