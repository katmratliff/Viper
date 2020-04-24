# -*- coding: utf-8 -*-

#local imports
import time

def time_counter(seconds):
    """Pauses program for a user-specified time.
    
    Parameters
    ----------
    seconds : int
        number of seconds to pause program
    
    Returns
    -------
    ``None``
    """
    start = time.time()
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
#    print('done counting!')
    return None

def check_number(number,allowed):
    """Checks to see if a number is in allowed list.
    
    Parameters
    ----------
    number : number to check
    allowed : list of allowed numbers
    
    Returns
    -------
    boolean
        `True` if number is in allowed list. Otherwise, `False`
    """
    ok_num = 0
    if number in allowed:
        ok_num = 1
    return ok_num