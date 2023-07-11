from hand_crafted_features import hand_crafted_features
#from ae import auto_encoder
from searcher import Searcher
import cv2
from pathlib import Path
import csv
import numpy as np
import os



def display_results(query_result):
    """
    Function to display retrieved images.
    Parameters
    ----------
    query_result : dict
        retrieved image paths as keys and similarity score as value.
    """
    counter = 0
    results = list(query_result.items())
    for i in results:
        img = cv2.imread(i[0])
        cv2.imshow('Result', img)
        cv2.waitKey(0)


class Query:

    def __init__(self, path_to_index):
        """
        Init function of the Query class. Sets 'path_to_index' to the class variable 'path_to_index'. Class variables 'query_image_name' and 'results' are set to None.
        Parameters
        ----------
        path_to_index : string
            Path to the index file.
        """
        self.path_to_index = path_to_index
        self.query_image_name = None
        self.query_image = None
        self.features = None
        self.results = None


    def set_image_name(self, query_image_name):
        """
        Function to set the image name if it does not match the current one. Afterwards the image is loaded and features are retrieved.
        Parameters
        ----------
        query_image_name : string
            Image name of the query. For example: 'static/images/query/test.png'
        Tasks
        ---------
            - Check if 'query_image_name' is different to 'self.query_image_name'
            - If yes:
                - Set 'self.results' to None
                - Overwrite 'query_image_name'
                - Read in the image and save it under 'self.query_image'
                - Calculate features
        """
        # if different image
        if(self.query_image_name != query_image_name):
            # set results to None
            self.results = None                             
            # set image name
            self.query_image_name = query_image_name        
            # read in the image
            self.query_image  = cv2.imread(self.query_image_name, cv2.IMREAD_GRAYSCALE)
            # extract the features  
            self.calculate_features()
        else:
            pass

    def calculate_features(self):
        """
        Function to calculate features for the query image.
        Tasks
        ---------
            - Check if "self.query_image" is None -> exit()
            - Extract features with "FeatureExtractor" and set to "self.features"
        """
        extractor = hand_crafted_features()
        if isinstance(self.query_image, np.ndarray):
            self.features = extractor.extract(image=self.query_image)
        else:
            exit()

 
    def run(self, limit=10):
        """
        Function to start a query if results have not been computed before.
        Parameters
        ----------
        limit : int
            Amount of results that will be retrieved. Default: 10.
        Returns
        -------
        - results : list
            List with the 'limit' first elements of the 'results' list. 

        Tasks
        ---------
            - Check if 'self.results' is None
            - If yes:
                - Create a searcher and search with features
                - Set the results to 'self.results'
            - Return the 'limit' first elements of the 'results' list.
        """
        resultList = []
        if(self.results==None):
            CreatedSearcher = Searcher(self.path_to_index)
            self.resultList = CreatedSearcher.search(self.features, limit)
        
        return self.resultList



if __name__ == "__main__":
    path_to_data = os.path.abspath("exercise_2/Data")
    path_to_index = os.path.join(path_to_data, "index.csv")

    query = Query(path_to_index=path_to_index) # -> print rows

    query_image_name = os.path.join(path_to_data, "images", "3145.png")
    query.set_image_name(query_image_name=query_image_name)
    query_result = query.run()

    display_results(query_result)

    print("Retrieved images: ", query_result)
