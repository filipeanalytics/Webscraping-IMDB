# Libraries imported to webscrape:
import time
from selenium import webdriver
from bs4 import BeautifulSoup
# Pandas to deal with Dataframes and read and write to CSV files.
import pandas as pd
# Regular Expressions to do text manipulations:
import re
# Libraries imported to plot graphs:
import matplotlib.pyplot as plt
import numpy as np


# Webscrape IMDB, treat the result, convert to Dataframe, then to CSV.
def webScraping(CSVPath):

    #  Connect to Browser
    DRIVER_PATH = "C:/Users/filip/Documents/PythonFiles/chromedriver"
    browser = webdriver.Chrome(DRIVER_PATH)

    # Access website
    URL = "https://www.imdb.com/"
    browser.get(URL)
    # Give the browser time to load all content.
    # time.sleep(2)

    # Click on Menu button
    menuButton = browser.find_element_by_css_selector('#imdbHeader-navDrawerOpen--desktop')
    menuButton.click()
    time.sleep(2)

    # Select Most Popular Movies from Menu items
    mostPopMovies = browser.find_element_by_css_selector(
        '#nav-link-categories-mov+ ._299G6wcz6LCpY_QFQJtc76 .ipc-list__item--indent-one:nth-child(4)')
    mostPopMovies.click()
    time.sleep(2)

    # Sort by IMDB rating descending, so I don't collect movies without IMDB ratings.
    sortByButton = browser.find_element_by_css_selector(
        "#lister-sort-by-options [value='ir:descending']")
    sortByButton.click()

    # Extract selected contents
    mainInfoList = browser.find_elements_by_css_selector('.titleColumn')
    ratingList = browser.find_elements_by_css_selector('.imdbRating')

    # Create DataFrame to store result
    df = pd.DataFrame(columns=['Title', 'Year', 'Ranking', 'Rating'])

    # Loop through 87 elements (excluding movies without rating)
    for i in range(87):
        # Prepare overal text result
        start = mainInfoList[i].get_attribute('innerHTML')
        # Beautiful soup allows us to remove HTML tags from our content, if it exists.
        soup = BeautifulSoup(start, features="lxml")
        # Remove leading and trailing whitespaces
        rawString = soup.get_text().strip()
        # Remove hidden characters for tabs and new lines.
        rawString = re.sub(r"[\n\t]*", "", rawString)  # re.sub(pattern, repl, string, count=0, flags=0)
        # Replace(remove) two or more consecutive empty spaces with ''
        rawString = re.sub('[ ]{2,}', '', rawString)

        # Extract TITLE
        titleCutOff = rawString.index('(')
        title = rawString[:titleCutOff]
        # title.strip()

        # Extract YEAR
        yearCutOff = rawString.index(')')  # RANKING after this point
        year = rawString[titleCutOff + 1:yearCutOff]

        # Extract RANKING
        # Here I find the second (, which determines the end index for Ranking
        rankingCutOff = [m.start() for m in re.finditer("\(", rawString)][1]
        ranking = rawString[yearCutOff + 1:rankingCutOff]

        # Extract RATING
        start = ratingList[i].get_attribute('innerHTML')
        # Beautiful soup allows us to remove HTML tags from our content if it exists.
        soup = BeautifulSoup(start, features="lxml")
        rating = soup.get_text().strip()  # Leading and trailing whitespaces are removed

        # Adding info on a Data Frame
        moviesInfo = {'Title': title, 'Year': year, 'Ranking': ranking, 'Rating': rating}
        df = df.append(moviesInfo, ignore_index=True)

    # Show all columns.
    pd.set_option('display.max_columns', None)
    # Show all rows.
    pd.set_option('display.max_rows', None)
    # Increase number of columns that display on one line.
    pd.set_option('display.width', 1000)
    print("\nTop 87 Movies listed in descending order of IMDB Rating")
    print(df)

    # Saving results in a CSV file
    df.to_csv(CSVPath)

# =======================================================================================
# =======================================================================================
# Read from CSV treated result and give stats summary for rating.
def getSummary(CSVPath):
    df = pd.read_csv(CSVPath)

    countRat = df['Rating'].count()
    minRat = df['Rating'].min()
    maxRat = df['Rating'].max()
    meanRat = round(df['Rating'].mean(), 2)
    medianRat = round(df['Rating'].median(), 2)
    stdRat = round(df['Rating'].std(), 2)

    print("\nSummary statistics for Rating: \n"
          "Count:  " + str(countRat) + "\n" +
          "Min:    " + str(minRat) + "\n" +
          "Max:    " + str(maxRat) + "\n" +
          "Mean:   " + str(meanRat) + "\n" +
          "Median: " + str(medianRat) + "\n" +
          "Std:    " + str(stdRat) + "\n")

    # List number of movies per year
    dfStats = df.groupby('Year')['Ranking'].count().reset_index().rename(columns={
        'Ranking': 'Total'})

    dfRankingMean = df.groupby('Year')['Ranking'].mean().reset_index().rename(columns={
        'Ranking': 'Ranking Mean'})
    dfRankingMax = df.groupby('Year')['Ranking'].max().reset_index().rename(columns={
        'Ranking': 'Ranking Max'})
    dfRankingMin = df.groupby('Year')['Ranking'].min().reset_index().rename(columns={
        'Ranking': 'Ranking Min'})
    dfRankingStd = df.groupby('Year')['Ranking'].std().reset_index().rename(columns={
        'Ranking': 'Ranking Std'})

    dfStats['Ranking Min'] = dfRankingMin['Ranking Min']
    dfStats['Ranking Max'] = dfRankingMax['Ranking Max']
    dfStats['Ranking Mean'] = round(dfRankingMean['Ranking Mean'], 2)
    dfStats['Ranking Std'] = round(dfRankingStd['Ranking Std'])
    print("Summary statistics for all movies grouped by year:")

    # Show all columns.
    pd.set_option('display.max_columns', None)
    # Increase number of columns that display on one line.
    pd.set_option('display.width', 1000)
    print(dfStats)

# =======================================================================================
# =======================================================================================
# Read from CSV and plot a ScatterPlot for Rating x Ranking
def plotGraph(CSVPath):
    df = pd.read_csv(CSVPath)

    # Sort the data frame to make Rating go from best (10) to worse (0)
    df = df.sort_values(['Rating'], ascending=[False])
    # print(df[['Rating']])

    # This line inverts the y axis to show best Rating close to best ranking at (0,0)
    plt.gca().invert_yaxis()

    # Plot a Scatterplot for all the Rankings
    x = df['Ranking']
    y = df['Rating']
    plt.scatter(x, y, label="All movies",
                color="orange")
    # create a Trend Line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "o--")

    # Plot another Scatterplot with the top 10 in the rank
    dfTop10Rank = df[(df['Ranking'] <= 10)]
    x10 = dfTop10Rank['Ranking']
    y10 = dfTop10Rank['Rating']
    plt.scatter(x10, y10, label="Top 10 movies",
                color="red")
    # create a Trend Line
    z = np.polyfit(x10, y10, 1)
    p = np.poly1d(z)
    plt.plot(x10, p(x10), "r--")

    # Plot another Scatterplot with the top 20 in the rank
    dfTop20Rank = df[(df['Ranking'] <= 20)]
    x20 = dfTop20Rank['Ranking']
    y20 = dfTop20Rank['Rating']
    plt.scatter(x20, y20, label="Top 20 movies",
                color="green")
    # create a Trend Line
    z = np.polyfit(x20, y20, 1)
    p = np.poly1d(z)
    plt.plot(x20, p(x20), "g--")

    # Plot another Scatterplot with the top 30 in the rank
    dfTop30Rank = df[(df['Ranking'] <= 30)]
    x30 = dfTop30Rank['Ranking']
    y30 = dfTop30Rank['Rating']
    plt.scatter(x30, y30, label="Top 30 movies",
                color="black")
    # create a Trend Line
    z = np.polyfit(x30, y30, 1)
    p = np.poly1d(z)
    plt.plot(x30, p(x30), "k--")

    # Set up plot details
    plt.legend(loc=1)
    plt.xlabel("Ranking")
    plt.ylabel("Rating")
    plt.title("Ranking x Rating")

    plt.show()
    print(
        '\nIt\'s really interesting to notice that there is a positive correlation '
        'between Rating\n and Ranking for the Top 20 movies in the rank, where better the '
        'Rating (closer to 10), better\n is the Ranking(closer to 1st). The opposite '
        'happens when we consider the worst ranked movies( \n after top 20): We can see a '
        'negative correlation trend, where better the rating(closer to 10) \n means a worse '
        'rank(away from 1st).')
    # It's really interesting to notice that there is a positive correlation between Rating
    # and Ranking for the Top 20 movies in the rank, where better the Rating (closer to
    # 10), better is the Ranking(closer to 1st). The opposite happens when we consider the
    # worst ranked movies(after top 20): We can see a negative correlation trend, where
    # better the Rating(closer to 10) means a worse Ranking(away from 1st).

# =======================================================================================
# =======================================================================================


# Path for CSV file that's gonna be generated as a result of the webscraping:
PATH = "C:/Users/filip/Documents/PythonFiles/"
CSV_FILE = "IMDB Analysis.csv"
CSVPath = PATH+CSV_FILE

# Run the program
webScraping(CSVPath)  # Webscrape IMDB, treat the result, convert to Dataframe then to CSV
getSummary(CSVPath)  # Read from CSV treated result and give stats summary for rating.
plotGraph(CSVPath)  # Read from CSV and plot a ScatterPlot for Rating x Ranking







