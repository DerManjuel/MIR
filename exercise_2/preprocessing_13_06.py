import cv2
from hand_crafted_features_13_06 import hand_crafted_features
#from ae import auto_encoder
import numpy as np
import glob
import sys
import os
from pathlib import Path
import csv


def get_images_paths(image_directory, file_extensions):
    """
    Function to receive every path to a file with ending "file_extension" in directory "image_directory".
    Parameters
    ----------
    image_directory : string
        Image directory. For example: 'static/images/database/'
    file_extensions : tuple
        Tuple of strings with the possible file extensions. For example: '(".png", ".jpg")'
    Returns
    -------
    - image_paths : list
        List of image paths (strings).
    Tasks
    -------
        - Iterate over every file_extension
            - Create a string pattern 
            - Use glob to retrieve all possible file paths (https://docs.python.org/3.7/library/glob.html )
            - Add the paths to a list  (extend)
        - Return result
    """
    
    result = []
    for i in file_extensions:
        pattern = image_directory + "/*" + i
        path = glob.glob(pattern)
        result.extend(path)
        #print('Result:', result)

    #test
    #example_image = cv2.imread(result[0], cv2.IMREAD_GRAYSCALE)
    #cv2.imshow("Example", example_image)
    #cv2.waitKey(0)
    return result


def create_feature_list(image_paths):
    """
    Function to create features for every image in "image_paths".
    Parameters
    ----------
    image_paths : list
        Image paths. List of image paths (strings).
    Returns
    -------
    - result : list of lists.
        List of 'feature_list' for every image. Each image is summarized as list of several features.
    Tasks
    -------
        - Iterate over all image paths
        - Read in the image
        - Extract features with class "feature_extractor"
        - Add features to a list "result"
    """
    result = []
    for path in image_paths:
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        # create extractor
        feature_extractor = hand_crafted_features()

        # describe the image
        features = feature_extractor.extract(image)

        result.extend([features])

    return result


def write_to_file(feature_list, image_paths, output_path):
    """
    Function to write features into a CSV file.
    Parameters
    ----------
    feature_list : list
        List with extracted features. Should come from 'create_feature_list':
    image_paths : list
        Image paths. List of image paths (strings). Should come from 'get_images_paths':
    output_path : string
        Path to the directory where the index file will be created.
    Tasks
    -------
        - Open file ("output_name")
        - Iterate over all features (image wise)
        - Create a string with all features concerning one image seperated by ","
        - Write the image paths and features in one line in the file [format: image_path,feature_1,feature_2, ..., feature_n]
        - Close file eventually

        - Information about files http://www.tutorialspoint.com/python/file_write.htm 
    """
    path = os.path.join(output_path, "index.csv")

    with open(path, 'w+') as f:
        writer = csv.writer(f, delimiter=',')
        count = 0
        for i in feature_list:
            my_array = image_paths[count].split(' ') + i
            if count == 0:
                print(my_array)
            writer.writerow(my_array)
            count = count + 1
    print('I`m done')
    pass

    '''fo = open(path, 'w')

    count = 0
    #print(len(feature_list))
    for i in feature_list:
        my_string = ""
        my_string = ','.join(map(str, i))
        #print(my_string)
        my_string = image_paths[count] + "," + my_string
        fo.write(my_string) # wir schreiben nur einen String in eine Datei, aber nicht konvertiert nach CSV!
        fo.write('\n')
        count += 1
    # Close opend file
    fo.close()
    #print(my_string)'''


def preprocessing_main(image_directory, output_path, file_extensions = (".png", ".jpg")):
    """
    Function which calls 'get_images_paths', 'create_feature_list' and 'write_to_file'
    """

    image_paths = get_images_paths(image_directory, file_extensions)

    feature_list  = create_feature_list(image_paths)

    write_to_file(feature_list, image_paths, output_path)

if __name__ == '__main__':
    pathname = os.path.abspath("exercise_2/Data/images")
    #print(pathname)
    path = os.path.abspath("exercise_2/Data")
    #print('Path', path)

    preprocessing_main(image_directory = pathname, output_path=path)