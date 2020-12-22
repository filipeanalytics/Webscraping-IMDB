# Webscraping IMDB
 This Python application scrapes IMDB most popular movies, summarizes the data dynamically and plots a graph. It’s divided into 3 main functions. The first webscrapes IMDB website, cleanse the data, convert it to a Dataframe and then save into a csv file. The second reads data from the csv file, performs a set of aggregation functions, converts the result to a Dataframe and then prints the results. The third and last function reads the data from the csv file and plots a Scatter Plot for Rating x Ranking.



Download ChromeDriver from https://chromedriver.chromium.org/ Save it in a folder that you can find easily.

In the Python code, update the path to where you saved your chrome plugin (chromedriver.exe) DRIVER_PATH = "C:/Users/filip/Documents/PythonFiles/chromedriver" browser = webdriver.Chrome(DRIVER_PATH)

Install these 2 Python libraries: pip install selenium pip install webdriver-manager

Update the paths to the csv file to the folder where you want to save your file. PATH = "C:/Users/filip/Documents/PythonFiles/" CSV_FILE = "IMDB Analysis.csv"
