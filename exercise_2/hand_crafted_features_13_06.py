import numpy as np
import cv2
import os

class hand_crafted_features:
    """
    Class to extract features from a given image.

    Example
    --------
    feature_extractor = hand_crafted_features()
    features = feature_extractor.extract(example_image)
    print("Features: ", features)
    """

    def extract(self, image):
        """
        Function to extract features for an image.
        Parameters
        ----------
        - image : (x,y) array_like
            Input image.

        Returns
        -------
        - features : list
            The calculated features for the image.

        Examples
        --------
        >>> fe.extract(image)
        [126, 157, 181, 203, 213, 186, 168, 140, 138, 155, 177, 176]
        """
        # TODO: You can change your extraction method here:
        #features = self.image_pixels(image)
        features = self.histogram(image)
        
        # TODO: You can even extend features with another method:
        #features.extend(self.thumbnail_features(image))

        return features
    
    def histogram(self, image):
        """
        Function to extract histogram features for an image.
        Parameters
        ----------
        - image : (x,y) array_like
            Input image.
        
        Returns
        -------
        - features : list
            The calculated features for the image.

        Tipps
        -----
            - Use 'cv2.calcHist'
            - Create a list out of the histogram (hist.tolist())
            - Return a list (flatten)
        """
        #TODO:
        hist = cv2.calcHist(images=image, channels=[0], mask=None, histSize=[256], ranges=[0, 256])
        features = hist.tolist()
        features = [item for sublist in features for item in sublist]
        return features


    def thumbnail_features(self, image):
        """
        Function to create a thumbnail of an image and return the image values (features).
        Parameters
        ----------
        - image : (x,y) array_like
            Input image.
        
        Returns
        -------
        - features : list
            The calculated features for the image.

        Tipps
        -----
            - Resize image (dim(30,30))
            - Create a list from the image (np array)
            - Return a list (flatten)
        """
        #TODO: 
        

    def partitionbased_histograms(self, image, factor = 10):
        """
        Function to create partition based histograms.
        Parameters
        ----------
        - image : (x,y) array_like
            Input image.
        - factor : int
            Partitioning factor.
        
        Returns
        -------
        - features : list
            The calculated features for the image.

        Tipps
        -----
            - Resize image (dim(200, 200))
            - Observe (factor * factor) image parts
            - Calculate a histogramm for each part and add to feature list
        """
        #TODO:
        pass


    def extract_features_spatial(self, image, factor = 10):
        """
        Function to extract spatial features.
        Parameters
        ----------
        - image : (x,y) array_like
            Input image.
        - factor : int
            Partitioning factor.
        
        Returns
        -------
        - features : list
            The calculated features for the image.

        Tipps
        -----
            - Resize image (dim(200, 200))
            - Observe (factor * factor) image parts
            - Calculate max, min and mean for each part and add to feature list
        """
        #TODO:
        pass


    def image_pixels(self, image):
        """
        Function to return the image pixels as features.
        Example of a bad implementation. The use of pixels as features is highly inefficient!

        Parameters
        ----------
        - image : (x,y) array_like
            Input image.
        
        Returns
        -------
        - features : list
            The calculated features for the image.
        """
        # cast image to list of lists
        features =  image.tolist()
        # flatten the list of lists
        features = [item for sublist in features for item in sublist]
        # return 
        return features
    
def img_resize(img, factor=0.5):
    height = int(img.shape[0]*factor)
    width = int(img.shape[1] * factor)
    dim = (width, height)
    #resize image
    resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    return resized_img

if __name__ == '__main__':
    # Read the test image
    # TODO: You can change the image path here:
    pathname = os.path.join("static", "images", "database", "3145.png")
    print(pathname)
    example_image = cv2.imread(pathname, cv2.IMREAD_GRAYSCALE)
    
    cv2.imshow("Example", example_image)
    cv2.waitKey(0)

    # Assert image read was successful
    assert example_image is not None

    # create extractor
    feature_extractor = hand_crafted_features()

    # describe the image
    features = feature_extractor.extract(example_image)


    # print the features
    print("Features: ", features)
    print("Length: ", len(features))

    test_img = img_resize(example_image)
    cv2.imshow("Example", test_img)
    cv2.waitKey(0)
