from preprocessing import get_images_paths
from query import Query
from irma import IRMA

import cv2
import sys
import numpy as np
from pathlib import Path
import csv
import os
from tqdm import tqdm


def count_codes(code_path = os.path.abspath("exercise_2/Data/IRMA_data/image_codes.csv")): 
    """
    Counts the occurrence of each code in the given "CSV" file.

    Parameters
    ----------
    code_path : string
        Path to the csv file. Default= irma_data/image_codes.csv"
    Returns
    -------
    results : dict
        Occurrences of each code. Key is the code, and value the amount of occurrences.
    Task
    -------
        - If there is no code file -> Print error and return False [Hint: Path(*String*).exists()]
        - Open the code file
        - Read in CSV file [Hint: csv.reader()]
        - Iterate over every row of the CSV file
            - Make an entry in a dict
        - Close file
        - Return results
    """
    count_dict = {}
    if Path(code_path).exists():
        with open(code_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                if row[1] in count_dict:
                    count_dict[row[1]] += 1
                else:
                    count_dict[row[1]] = 1
        csv_file.close()
        return count_dict
    
    else:
        return False
   


def precision_at_k(correct_prediction_list, k = None):
    """
    Function to calculate the precision@k.

    Parameters
    ----------
    correct_prediction_list : list
        List with True/False values for the retrieved images.
    k : int
        K value.
    Returns
    -------
    precision at k : float
        The P@K for the given list.
    Task
    -------
        - If k is not defined -> k should be length of list
        - If k > length -> Error
        - If k < length -> cut off correct_prediction_list at k
        - Calculate precision for list
    Examples
    -------

        print("P@K: ", precision_at_k([True, True, True, False]))
        >>> P@K:  0.75

        print("P@K: ", precision_at_k([True, True, True, False], 2))
        >>> P@K:  1.0
    """
    length = len(correct_prediction_list)

    if k == None:
        k = length

    if k > length:
        raise ValueError('k is greater than the length of the list, reduce k.')
    
    elif k < length:
        correct_prediction_list = correct_prediction_list[0:k]
    
    precision = sum(correct_prediction_list) / len(correct_prediction_list)

    return precision

        

def average_precision(correct_prediction_list, amount_relevant= None):
    """
    Function to calculate the average precision.

    Parameters
    ----------
    correct_prediction_list : list
        List with True/False values for the retrieved images.
    amount_relevant : int
        Number of relevant documents for this query. Default is None.
    Returns
    -------
    average precision : float
        The average precision for the given list.
    Tasks
    -------
        - If amount_relevant is None -> amount_relvant should be the length of 'correct_prediction_list'
        - Iterate over 'correct_prediction_list'
            - Calculate p@k at each position
        - sum up values and divide by 'amount_relevant'
    Examples
    -------

        print("AveP: ", average_precision([True, True, True, False]))
        >>> P@AveP:  0.75

        print("AveP: ", average_precision([True, True, False, True], 3))
        >>> AveP:  0.9166666666666666
    """
    sumup = 0
    
    if amount_relevant == None:
        amount_relevant = len(correct_prediction_list)
    
    for i in range(1, len(correct_prediction_list)+1):
        rel = correct_prediction_list[:i]
        sumup += precision_at_k(rel, i)

    aveP = sumup / amount_relevant

    return aveP


def mean_average_precision(limit = 10000):
    """
    Function to calcualte the mean average precision of the database.

    Parameters
    ----------
    limit : int
        Limit of the query. Default is None.
    Returns
    -------
    mean average precision : float
        The meanaverage precision of the selected approach on the database.
    Tasks
    -------
        - Create irma object and count codes.
        - Iterate over every image path (you can use 'tqdm' to check the run time of your for loop)
            - Create and run a query for each image
            - Compute a correct_prediction_list
            - Remove the first element (its the query image)
            - Compute AP (function) and save the value
        - Compute mean of APs
    """
    pathname = os.path.abspath("exercise_2/Data/images")
    base_path = os.path.abspath("exercise_2/Data")

    irma_path = os.path.abspath("exercise_2/Data/IRMA_data")
    code_path = os.path.abspath("exercise_2/Data/IRMA_data/image_codes.csv")
    index_path = os.path.join(base_path, "index.csv")

    irma = IRMA(irma_path)
    count_dict = count_codes(code_path) 

    image_paths = get_images_paths(image_directory = pathname, file_extensions= (".png", ".jpg"))
    aver_prec = []
    for path in tqdm(image_paths):
        correct_prediction_list = []
        query = Query(path_to_index=index_path)
        query.set_image_name(query_image_name=path)
        query_result = query.run()

        orig_code = irma.get_irma(path)

        for key in query_result:
            code = irma.get_irma(key)
            
            if code == orig_code:
                correct_prediction_list = correct_prediction_list + [True]
            
            else:
                correct_prediction_list = correct_prediction_list + [False]
            
        #remove first element
        correct_prediction_list.pop(0)
        aver_prec = aver_prec + [average_precision(correct_prediction_list)]

    map = sum(aver_prec) / len(image_paths)

    return map


if __name__ == "__main__":
    #test count coder:
    #print(count_codes(os.path.abspath("exercise_2/Data/IRMA_data/image_codes.csv")))

    test = [True, False, True, False]
    print("Examples with query results: ", str(test)) 
    print("P@K: ", precision_at_k(test, 4))
    print("AveP: ", average_precision(test, 3))

    result = mean_average_precision()
    print("\n\n")
    print("-"*50)
    print("Evaluation of the database")
    print("MAP: ", result)

    #MAP of thumbnail_features is: 0.26
    #MAP of histogramm_features is: 0.55
