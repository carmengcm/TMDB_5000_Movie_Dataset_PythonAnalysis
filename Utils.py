"""
    This document contains functions used in the .ipynb
"""

def getJSONDataFrame(pd, dfMerge, objeto):
    """
    @P1: pd --> pandas import
    @P2: dfMerge --> dataframe merged (movies and credits)
    @P3: Objeto --> (cast, crew, genres...). Column name which contains a JSON 
    Returns: Dataframe from json list
    """

    json = []
    dfReturn = pd.DataFrame()
    cont = 0
    for i in range(len(dfMerge)):
        # Obtaining the movie_id
        id = dfMerge['movie_id'][i]
        # Setting up the casts dataframe
        json = pd.read_json(dfMerge[objeto][i])
        cont = cont + len(json)
        json['movie_id'] = id
        dfReturn = dfReturn.append(json)
        json = []
    
    #print("longitud df --> ", len(dfReturn), "Contador --> ", cont)
    
    return(dfReturn.reset_index())    

def getTopDataframe(df, objeto, size):
    """
    @P1: df --> Main dataframe
    @P2 : Objeto --> (Budget, Popularity, Runtime, revenue, vote_count, vote_average)
    @P3: Size --> sets the size of the returning dataframe
    Returns a dataframe with the top object
    """

    # Dataframe with the first 100 movies with largest budget.
    df = df.sort_values(by= str(objeto), ascending=False).head(size)
    return(df)

def getDataFrameCountPerMovie(df, size): 
    """
    @P1: df --> the dataframe which contains the crew | cast | countries | .. json dataframes
    @P2: size --> sets the size of the returning dataframe
    Returns a dataframe which contains the movie_id and the total number of crew in that movie
    """
    df = df.groupby(['movie_id']).size().reset_index(name='count').sort_values(by="count", ascending=False)
    return(df.head(size))

    
""" 
    Getting lists Section
    
"""
def getMovieIds(df):
    """
    @P1: dataframe 
    Returns a list of movie_ids from df
    """
    return(df['movie_id'].tolist())
    
    
def getKeyboardsFromMovies(dfKW, ids):
    """
    @P1: dfKB --> keywords dataframe
    Returns a list of keywords filtered by the movie ids
    """
    # Keybords from the selected movies
    dfKwsFiltered = dfKW[dfKW['movie_id'].isin(ids)]
    # We aggrupate keybords by name, then sort them by count.
    dfKwsFiltered = dfKwsFiltered.groupby(['name']).count().reset_index().sort_values(by="movie_id", ascending=False)
    # Convert the dataframe to a list which only contains the sorted Keybords.
    keywordsList = dfKwsFiltered['name'].tolist()
    keywordsList = " ".join(keywordsList)
    return(keywordsList)
    
def addColCountJson(pd, dfMerge, objetos, cols):
    """
    @P1: pd --> pandas library
    @P2: df --> dataframe
    @P3: object --> Json column (cast, crew, etc) 
    @P4: cols --> Columns you want to show
    Return --> returns a daframe containing the count of json in a column
    """
    size = 0
    colsToShow = ['movie_id','original_title']
    colsToShow.extend(objetos)
    colsToShow.extend(cols)
    
    
    dfMerge = dfMerge[colsToShow].copy()
    
    dfMerge.is_copy = False
    
    # print(dfReturn.head(1))    
    for i in range(len(dfMerge)):
        for objeto in objetos:
            # Getting the json dataframe
            json = pd.read_json(dfMerge[objeto][i])
            # Getting the length
            size = len(json)
            json = []
            # Setting the length to the object column
            dfMerge.is_copy = False
            #dfMerge.ix[i, objeto] 
            newCol = objeto + "_count"
            dfMerge.loc[i, newCol] = size
        
    return(dfMerge)

def getGenderPerYear(pd, dfMain, dfCast):
    """
    @P1: pd --> pandas library
    @P2: df --> dataframe
    @P3: object --> Json column (cast, crew, etc) 
    @P4: cols --> Columns you want to show
    Return --> returns a daframe containing the count of json in a column
    """
   
    dfReturn = pd.DataFrame(columns=['release_year', 'female_count', 'male_count'])
    
    # We get all the years
    years = dfMain["release_year"].unique().tolist()
    cont = -1 

    for year in years: 
        # We add 1 per year
        cont = cont + 1
        # we get the movies for that years
        ids = utl.getMovieIds(dfMain[dfMain['release_year'] == year])
        dfCastFiltered = dfCast[dfCast['movie_id'].isin(ids)].reset_index()
        # We get the female and man count
        femaleCount = dfCastFiltered[dfCastFiltered["gender"] == 1].count()['id']
        manCount = dfCastFiltered[dfCastFiltered["gender"] == 2].count()['id']
        # We add the counts to the df
        dfReturn.loc[cont, "release_year"] = year
        dfReturn.loc[cont, "female_count"] = femaleCount
        dfReturn.loc[cont, "male_count"] = manCount
            
    return(dfReturn)

def decorate_table(x):
    """
    @P1: x --> Numeric value
    Returns the color of the number according to if is max number or negative. Used in correlation.
    """
    color = 'black' 
    if x == 1:
        color = 'blue'
    elif x < 0:
        color = 'red'
    elif x > 0.5:
        color = 'blue'
    else:
        color = 'black'
        
    return 'color: %s' % color


def getDataFrameDataAveragePerCountryOrCompany(pd, dataframetype, df, dfMain, objeto):
    """
    @P1: dataframetype --> production_countries | production_companies
    @P2: df --> dataframe containing the countries or the companies
    @P3: dfMain --> main dataframe
    @P4: Objeto --> Campo a devolver budget | revenue | runtime | popularity | vote_average
    Returns a dataframe that contains the average budget | revenue | runtime | popularity | vote_average per country or company
    """
    dfReturn = pd.DataFrame(columns=[dataframetype, 'object_count', objeto, 'average'])
    cont = 1
    
    for i in range(len(df)):
        # We get the id
        id = df['movie_id'][i]
        # We get the country
        country = df['name'][i]
        # getting the budget value
        value = dfMain[dfMain["movie_id"] == id ][objeto].reset_index()[objeto][0]
        
        if country in dfReturn[dataframetype].tolist():
            # if the country is in the dataframe, we update it
            dfSelected = dfReturn.loc[dfReturn[dataframetype] == country] 
            row = dfSelected.index.values[0]
            dfReturn.loc[row, objeto] = dfSelected[objeto].reset_index()[objeto][0] + int(value)
            dfReturn.loc[row, 'object_count'] = dfSelected['object_count'].reset_index()['object_count'][0] + 1
        else:
            # if the country isnt in the dataframe, we add it
            dfReturn.loc[cont, dataframetype] = country
            dfReturn.loc[cont, 'object_count'] = 1
            dfReturn.loc[cont, objeto] = int(value)
            # we update cont here
            cont = cont +1
    # Getting the average of the column selected per country
    dfReturn['average'] =  dfReturn[objeto] / dfReturn['object_count']
    return(dfReturn.sort_values(by="average", ascending=False))
    

def getRandomMovies(random, dfMain, size):
    """
    @P1: random --> library random
    @P2: dfMain --> main dataframe
    @P3: size of the random dataframe you want in return
    Returns --> Random movies 
    """
    # We obtain the length of the dataframe
    dfSize = len(dfMain)
    print("Size of dataframe: ", dfSize)
    # We obtain the ids from the movies
    ids = getMovieIds(dfMain)
    # We choose n elements from the movies randomly
    randomIds = random.sample(ids,  size)
    # We get the random movies from the dataframe
    randomDataframe = dfMain[dfMain['movie_id'].isin(randomIds)]
    #display(randomDataframe)
    
    randomDataframe = randomDataframe[['movie_id', 'original_title', 'is_profitable']]
    return(randomDataframe)


def getPercentageOfProfitPerYear(pd, dfMain):
    """
    @P1: pd --> pandas library
    @P2: dfMain --> main dataframe
    Returns --> % of profit of movies per year
    """

    df = dfMain.groupby(['release_year'])

    dfReturn = pd.DataFrame(columns=['release_year', 'percentaje_profit'])
    # List of all the years: 
    years = list(df.groups.keys())

    cont = 0
    for year in years:
        # We obtain the movies
        dfMovies = dfMain[dfMain["release_year"] == year]
        # Size of the dtMovies
        size = len(dfMovies)
        dfReturn.loc[cont, 'release_year'] = year
        profit = dfMovies[dfMovies["is_profitable"] == True][['is_profitable']].reset_index()['is_profitable']
        dfReturn.loc[cont, 'percentaje_profit'] = round(sum(profit) /size * 100, 2)
        cont = cont + 1
    #display(dfReturn)
    return(dfReturn)

def getLowerDataframe(df, objeto, size):
    """
    @P1: df --> Main dataframe
    @P2 : Objeto --> (Budget, Popularity, Runtime, revenue, vote_count, vote_average)
    @P3: Size --> sets the size of the returning dataframe
    Returns a dataframe with the lower object
    """

    # Dataframe with the first 100 movies with largest budget.
    df = df.sort_values(by= str(objeto), ascending=True).head(size)
    return(df)


def getMostUsedLanguagesDataFrame(pd, dfMain):
    """
    @P1: pd --> Pandas library
    @P2: dfMain --> main dataframe
    Returns a dataframe with the languages most used in movies
    """
    # Most used languages in the movies
    file = "~\\Documents\\TMDB_5000_Movie_Dataset_PythonAnalysis\\BaseDeDatos\\ISO_Languages.csv"
    # Read the csv
    dfLanguages = pd.read_csv(file, encoding="cp437", delimiter = '\t', usecols=['ISO 639-1 Code', 'English name of Language'])
    # Rename columns
    dfLanguages = dfLanguages.rename(columns={'ISO 639-1 Code': 'original_language'})
    #dfLanguages.head()

    dfMergeLanguagesMain = pd.merge(dfLanguages, dfMain)
    #df2.head()

    dfMergeLanguagesMain.original_language.replace({'af': 'ZA', 'ar': 'SA', 'cs': 'CZ', 'da': 'DK', 'el': 'GR', 
                                      'en': 'GB', 'fa': 'IR', 'he': 'IL', 'hi': 'IN', 'hu': 'HU', 
                                      'ja': 'JP', 'ko': 'KR', 'ky': 'KG', 'nb': 'NO', 'ps': 'AF', 
                                      'sl': 'SI', 'sv': 'SE', 'ta': 'IN', 'te': 'IN', 'vi': 'VN', 
                                      'zh': 'CN', 'es': 'ES', 'it': 'IT', 'fr': 'FR', 'de': 'DE', 
                                      'ro': 'RO', 'ru': 'RU', 'cn': 'CN', 'id': 'ID','is': 'IS',
                                      'nl': 'NL', 'no': 'NO', 'pl': 'PL', 'pt': 'PT', 'th': 'TH', 
                                      'tr': 'TR', 'te': 'IN', 'ta': 'LK'}, inplace=True, regex=True)

    dfMergeLanguagesMainGB = dfMergeLanguagesMain.groupby(["original_language", "English name of Language"]).size().reset_index(name="Time")
    dfMergeLanguagesMainGB.columns = ['ISO 3166 Country Code', 'English name of Language', 'Time']
    dfMergeLanguagesMainGB['Time'] = dfMergeLanguagesMainGB['Time'].astype('float64')
    row_index = dfMergeLanguagesMainGB.Time == 4505.0
    # then with the form .loc[row_indexer,col_indexer]
    dfMergeLanguagesMainGB.loc[row_index, 'Time'] = 500.00
    return(dfMergeLanguagesMainGB.head())

def getGeoLocations(pd):
    """
    @P1: pd --> pandas library
    Returns a dataframe containing worldwide geolocations
    """
    
    file = "~\\Documents\\TMDB_5000_Movie_Dataset_PythonAnalysis\\BaseDeDatos\\geolocations.csv"
    # Obtaining file
    dfGeo = pd.read_csv(file, encoding="cp437", delimiter = ',', quotechar='"')
    return(dfGeo)


def getColorsDictionary():
    """
    Returns a dictionary from 1 to 20 of colors
    """
    
    colors = {0: '#8F54FF', 1: '#649996', 2: '#FB9DDF', 3: '#FA7411', 4: '#11FAC2', 5: '#4D8175', 6: '#2030B2', 7: '#88FF0A',
              8: '#4B8013', 9: '#751269', 10: '#D3A4CE', 11: '#F9F503', 12: '#F90303', 13: '#F97303', 14: '#2A3028',
              15: '#AF0A0A', 16: '#C77D7D', 17: '#6C7D0C', 18: '#93EA9A', 19: '#649996'} 
    return(colors)

def getSex(sexInt):
    """
    @P1: int -> str
    Returns the label female | male for its number
    """  
    
    if sexInt == 1:
        return 'Female'
    else:
        return 'Male' 
