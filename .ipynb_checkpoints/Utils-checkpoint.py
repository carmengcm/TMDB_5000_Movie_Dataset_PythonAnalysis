"""
    Creating DataFrames Section
"""

def getJSONDataFrame(pd, dfMerge, objeto):
    """
    @P1: pd --> pandas import
    @P2: dfMerge --> dataframe merged (movies and credits)
    @P3: Objeto --> (cast, crew, genres...). Column name which contains a JSON 
    Returns: Dataframe from json list
    """
    #df = dfMerge[['movie_id', str(objeto)]]
    json = []
    #dfReturn = []
    
    #print("df", len(df))
    
    objetos = { 'cast': ['movie_id', 'name', 'character', 'gender'],
               'crew': ['movie_id', 'name', 'gender', 'department', 'job'],
               'genres': ['movie_id', 'name'],
               'keywords': ['movie_id', 'name'],
               'production_countries': ['movie_id', 'name'],
               'spoken_languages': ['movie_id', 'name']
              }
    # 'Crew': 25, 'Genres': 30, 'Keywords': 21, 'PCountries': 32, 'SLanguages': 2
    
    dfReturn = pd.DataFrame()
    cont = 0
    for i in range(len(dfMerge)):
        # Obtaining the movie_id
        id = dfMerge['movie_id'][i]
        #print(id)
        # Setting up the casts dataframe
        json = pd.read_json(dfMerge[objeto][i])
        cont = cont + len(json)
        json['movie_id'] = id
        #jsonModificado = json[objetos[str(objeto)]]
        dfReturn = dfReturn.append(json)
        json = []
    
    print("longitud df --> ", len(dfReturn), "Contador --> ", cont)
    
    return(dfReturn.reset_index())    

"""
    Getting different dataframes Section
"""

def getTopDataframe(df, objeto, size):
    """
    @P1: df --> Main dataframe
    @P2 : Objeto --> (Budget, Popularity, Runtime, revenue, vote_count, vote_average)
    @P3: Size --> sets the size of the returning dataframe
    Returns a dataframe with the top budget
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

    
"""

"""

def getDataFrameFromMovieIds(df, ids, cols):
    """
    """
    dfFiltered = df[df['movie_id'].isin(ids)]
    return(dfFiltered[cols])
    
    
def addColCountJson(pd, dfMerge, objeto, cols):
    """
    @P1: pd --> pandas library
    @P2: df --> dataframe
    @P3: object --> Json column (cast, crew, etc) 
    @P4: cols --> Columns you want to show
    Return --> returns a daframe containing the count of json in a column
    """
    size = 0
    colsToShow = ['movie_id','original_title', objeto]
    colsToShow.append(cols)
    
    dfMerge = dfMerge[colsToShow].copy()
    dfMerge.is_copy = False

   # print(dfReturn.head(1))    
    for i in range(len(dfMerge)):
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


def decorate_table(x):
    """
    @P1: x --> Numeric value
    Returns the color of the number according to if is max number or negative. 
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
    
    

