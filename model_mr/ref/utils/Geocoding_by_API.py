import googlemaps

gmaps = googlemaps.Client(key='AIzaSyDfLv3OzniRbUc7tTRBJndpiuyepHSmUrE')

def get_geocode(x):
    try:
        result = gmaps.geocode(x)[0]["geometry"]["location"]
        
    except:
        result = None
    
    return result

def get_geocodeDf(df, col):
    tempDf = df.copy()
    tempDf["lat_lng"] = tempDf[col].apply(lambda x: get_geocode(x))
    
    tempDf = tempDf[tempDf['lat_lng'].notnull()].copy()
    tempDf["latitude"] = tempDf["lat_lng"].apply(lambda x: x["lat"])
    tempDf["longitude"] = tempDf["lat_lng"].apply(lambda x: x["lng"])
    
    del tempDf["lat_lng"]
    return tempDf
