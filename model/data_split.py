import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def split(X_data,
          Y_data,
          split_ratio, 
          seed = 1234):
    """
        데이터 Split 시행하는 함수

        Args: 
            split_ratio:  train, valid, test의 비율을 지정 (list[float])
                         길이가 2면 train, valid,
                         길이가 3이면 train, valid, test로 인식
            return_data: 데이터를 반환할지, 내부 attribute로만 가지고 있을지 선택 (Logical)
                         내부 attribute 로 있을 때는 splitted_data로 접근가능

        Returns: 
            None

        Exception: 
            None
    """
    # train - test split
    if len(split_ratio) == 2:
        X_train, X_test, Y_train, Y_test = train_test_split(X_data.reset_index(drop = True), Y_data.reset_index(drop = True),
                                                            train_size = split_ratio[0],
                                                            test_size = split_ratio[1], 
#                                                             stratify = Y_data, 
                                                            random_state = seed)

        splitted_data = {"X_train" : X_train, 
                         "X_test" : X_test,
                         "Y_train" : Y_train,
                         "Y_test" : Y_test}
     

    elif len(split_ratio) == 3:
        # data -> train + test
        X_train, X_test, Y_train, Y_test = train_test_split(X_data.reset_index(drop = True), Y_data.reset_index(drop = True),
                                                            train_size = split_ratio[0] + split_ratio[1],
                                                            test_size = split_ratio[2], 
#                                                             stratify = Y_data, 
                                                            random_state = seed)

        # train -> train + valid 
        X_train, X_valid, Y_train, Y_valid = train_test_split(X_train, Y_train,
                                                              train_size = (split_ratio[0]/(split_ratio[0] + split_ratio[1])),
                                                              test_size = (split_ratio[1]/(split_ratio[0] + split_ratio[1])), 
#                                                               stratify = Y_train, 
                                                              random_state = seed)

        splitted_data = {"X_train" : X_train, 
                         "X_valid" : X_valid,
                         "X_test" : X_test,
                         "Y_train" : Y_train,
                         "Y_valid" : Y_valid,
                         "Y_test" : Y_test}

        # 데이터 Return
        return splitted_data