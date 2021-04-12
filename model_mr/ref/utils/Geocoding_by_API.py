import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBRxjIW7qfFhaVyCsc2xhk5mf1hXUSi9DI')

def get_geocode(x):
    try:
        result = gmaps.geocode(x)[0]["geometry"]["location"]
        
    except:
        result = None
    
    return result

def get_geocodeDf(df, col):
    tempDf = df.copy()
    tempDf["lat_lng"] = df[col].apply(lambda x: get_geocode(x))
    df["latitude"] = tempDf["lat_lng"].apply(lambda x: x["lat"])
    df["longitude"] = tempDf["lat_lng"].apply(lambda x: x["lng"])
    
    return df
