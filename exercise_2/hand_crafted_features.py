import numpy as np
import cv2
from PIL import Image
from matplotlib import cm
 
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
        thumbnail = self.thumbnail_features(image)
        
        # TODO: You can even extend features with another method:
        #features.extend(self.thumbnail_features(image))

        return thumbnail
    
    def histogram(self, image):
        # Jasmin
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
        pass


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
        # implement resizing
        MAX_SIZE = (200, 200)
        image = Image.fromarray(np.uint8(cm.gist_earth(image)*255))
        image.thumbnail(MAX_SIZE)
        image = np.array(image).flatten()

        return image


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

        dim = (200,200)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        # split image in factor x faxtor parts
        batches = [image[x:x+factor,y:y+factor] for x in range(0,image.shape[0],factor) for y in range(0,image.shape[1],factor)]
        
        return batches

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
    
    def plot_image(self, image):
        cv2.imshow('image',image)
        cv2.waitKey(0)
        # Close all windows
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # Read the test image
    # TODO: You can change the image path here:
    example_image = cv2.imread("Data/ImageCLEFmed2007_test/765856.png", cv2.IMREAD_GRAYSCALE)
    print(example_image.shape)

    # Assert image read was successful
    assert example_image is not None

    # create extractor
    feature_extractor = hand_crafted_features()

    # describe the image
    features, thumbnail = feature_extractor.extract(example_image)
    print(thumbnail.shape)
    #feature_extractor.plot_image(thumbnail)

    batches = feature_extractor.extract_features_spatial(example_image, 50)
    batches = batches[0]
    print(batches.shape)
    feature_extractor.plot_image(batches)
    # print the features
    #print("Features: ", features)
    #print("Length: ", len(features))
