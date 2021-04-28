import googlemaps


def get_geocode(x, google_key):
    """
        Google Map API를 활용하여 geocoding을 하는 함수

        Args: 
            x: 주소 (str)
            google_key: Google API Key (str)

        Returns: 
            result: 위경도 좌표 (Dictionary)

        Exception: 
    """
    gmaps = googlemaps.Client(key= google_key)
    
    try:
        result = gmaps.geocode(x)[0]["geometry"]["location"]
        
    except:
        result = None
    
    return result
    

def get_geocodeDf(df, col, google_key):
    """
        DataFrame의 주소 컬럼에 대해서 Geocoding을 통해 주소 -> 위/경도 좌표 변환하는 함수

        Args: 
            df: 데이터프레임 (Pandas.DataFrame)
            col: 주소 컬럼명 (str)
            google_key: Google API Key (str)

        Returns: 
            tempDf: 위/경도 좌표 컬럼(latitude, longitude)이 추가된 데이터 프레임 (Pandas.DataFrame)

        Exception: 
    """
    tempDf = df.copy()
    tempDf["lat_lng"] = tempDf[col].apply(lambda x: get_geocode(x, google_key))
    
    tempDf = tempDf[tempDf['lat_lng'].notnull()].copy()
    tempDf["latitude"] = tempDf["lat_lng"].apply(lambda x: x["lat"])
    tempDf["longitude"] = tempDf["lat_lng"].apply(lambda x: x["lng"])
    
    del tempDf["lat_lng"]
    return tempDf