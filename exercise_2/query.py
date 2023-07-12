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
    results = query_result
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
        self.old_limit = 0

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
            - Extract features wit "FeatureExtractor" and set to "self.features"
        """
        extractor = hand_crafted_features()
        if self.query_image is None: #isinstance(self.query_image, np.ndarray):
            exit()
        else:
            self.features = extractor.extract(image=self.query_image)
        
    def run(self, counter = 0, quantity = 10):
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
        #self.results = []
        limit = counter + quantity
        if(self.results is None) or (self.old_limit != limit):
            CreatedSearcher = Searcher(self.path_to_index)
            self.results = CreatedSearcher.search(self.features, limit)
            #self.results = self.searcher.search_tree(self.features, limit)
            if (self.results is False):
                print("Results is empty")
                quit()
        
        self.old_limit = limit
        
        #return our (limited) results
        return self.results[counter : counter + quantity]



    def relevance_feedback(self, selected_images, not_selected_images, limit):
        """
        Function to start a relevance feedback query.
        Parameters
        ----------
        selected_images : list
            List of selected images.
        not_selected_images : list
            List of not selected images.
        limit : int
            Amount of results that will be retrieved. Default: 10.
        Returns
        -------
        - results : list
            List with the 'limit' first elements of the 'results' list. 
        """

        # TODO:
        pass

    def get_feature_vector(self, image_names):
        """
        Function to get features from 'index' file for given image names.
        Parameters
        ----------
        image_names : list
            List of images names.
        Returns
        -------
        - features : list
            List with of features.
        """
        """if Path(self.path_to_index).exists():
            with open(self.path_to_index) as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                for row in csvreader:
                    for i in images_names:

                    res = [float(i) for i in row[1:]]
                     
        else:
            raise ValueError('No path to index file is given.') 
        
            """
        #TODO:
        pass
    
def rocchio(original_query, relevant, non_relevant, a = 1, b = 0.8, c = 0.1):
    """
    Function to adapt features with rocchio approach.

    Parameters
    ----------
    original_query : list
        Features of the original query.
    relevant : list
        Features of the relevant images.
    non_relevant : list
        Features of the non relevant images.
    a : int
        Rocchio parameter.
    b : int
        Rocchio parameter.
    c : int
        Rocchio parameter.
    Returns
    -------
    - features : list
        List with of features.
    """
    
    # TODO:
    pass

if __name__ == "__main__":
    path_to_data = os.path.abspath("exercise_2/static")
    path_to_index = os.path.join(path_to_data, "index.csv")

    query = Query(path_to_index= path_to_index)

    query_image_name = os.path.join(path_to_data, "images", "database", "3145.png")
    query.set_image_name(query_image_name=query_image_name)
    query_result = query.run()
    print("Retrieved images: ", query_result)

    display_results(query_result)