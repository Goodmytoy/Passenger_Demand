import pandas as pd
import numpy as np

# +
import pandas as pd
import numpy as np

def preprocessing_school_data(school_data):    
    school_data = school_data[["schoolNm", "schoolSe", "rdnmadr", "latitude", "longitude"]]
    school_data = school_data.rename(columns = {"schoolNm" : "name",
                                                "schoolSe" : "category",
                                                "rdnmadr" : "addr"})
    
    return school_data

