from datetime import datetime
import os
import inspect
import functools

def check_execution_time(func, start_log):
    """
        시간을 측정하는 Decorator 함수

        Args: 
            func: 대상 Function

        Returns:
            wrapper function
            
        Exception: 
    """
    @ functools.wraps(func)
    def wrapper_check_execution_time(*args, **kwargs):
        start_time = datetime.now()
        print(start_log, end = " ")

        result = func(*args, **kwargs)
        
        end_time = datetime.now()
        print(f"Finished (Function execution time: {end_time - start_time})")
        return result
    return wrapper_check_execution_time


