import csv
import os

def csv_to_dict(file_path):
    """
    Function to read in a csv file and create a dict based on the first two columns.

    Parameters
    ----------
    - file_path : string
        The filepath to the CSV file.
    
    Returns
    -------
    - csv_dict : dict
        The dict created from the CSV file.

    Tipps
    -------
    - Read in the CSV file from the path
    - For each row, add an entry to a dict (first column is key, second column is value)
    - Return the dict
    """
    dict = {}

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if len(row) > 0:
                dict[row[0]] = row[1]  
    return dict
    
class IRMA:
    """
    Class to retrieve the IRMA code and information for a given file.
    """
    labels_long = ["Technical code for imaging modality", "Directional code for imaging orientation", "Anatomical code for body region examined", "Biological code for system examined"]
    labels_short = ["Imaging modality", "Imaging orientation", "Body region", "System"]

    def __init__(self, dir_path= os.path.abspath("exercise_2/Data/IRMA_data")):
        """
        Constructor of an IRMA element.

        Parameters
        ----------
        - dir_path : string
            The path where the irma data is. There should be a "A.csv", "B.csv", "C.csv", "D.csv" and "image_codes.csv" file in the directory.

        Tipps
        -------
        - Create a dict for part A, B, C, and D of the IRMA code (user csv_to_dict(file_path))
        - Save the dicts (list) as class variable
        - Save "image_codes.csv" as dict in a class variable
        """
        self.dictA = csv_to_dict(os.path.join(dir_path, "A.csv"))
        self.dictB = csv_to_dict(os.path.join(dir_path, "B.csv"))
        self.dictC = csv_to_dict(os.path.join(dir_path, "C.csv"))
        self.dictD = csv_to_dict(os.path.join(dir_path, "D.csv"))
        self.image_dict = csv_to_dict(os.path.join(dir_path, "image_codes.csv"))
        self.dict_lst =[self.dictA, self.dictB, self.dictC, self.dictD]
        

    def get_irma(self, image_names):
        """
        Function to retrieve irma codes for given image names.

        Parameters
        ----------
        - image_names : list
            List of image names.

        Returns
        -------
        - irma codes : list
            Retrieved irma code for each image in 'image_list'

        Tipps
        -------
        - Remove file extension and path from all names in image_names. Names should be in format like first column of 'image_codes.csv'
        - Use self.image_dict to convert names to codes. ('None' if no associated code can be found)
        - Return the list of codes
        """
        code_lst = []
        for names in image_names:
            spl = names.rsplit('.', 1)
            spl = spl[0]
            if spl in self.image_dict:
                code = self.image_dict[spl]
            else:
                code = None  
            code_lst.append(code)     
        
        return code_lst



    def decode_as_dict(self, code):
        """
        Function to decode an irma code to a dict.

        Parameters
        ----------
        - code : str
            String to decode.

        Returns
        -------
        - decoded : dict

        Tipps
        -------
        - Make use of 'labels_short'
        - Possible solution: {'Imaging modality': ['x-ray', 'plain radiography', 'analog', 'overview image'], ...}
        - Solution can look different
        """
        #labels_short = ["Imaging modality", "Imaging orientation", "Body region", "System"]
        counter = 0
        dict = {}
        str = ""
        for i in code:
            str = str + i
            if i == '-':
                counter = counter + 1
                str = ""
                continue
            
            else:
                curr_dict = self.dict_lst[counter]
                if str in curr_dict:
                    entry = curr_dict[str]
                else:
                    entry = "unspecified"

                if self.labels_short[counter] in dict:
                    dict[self.labels_short[counter]].append(entry)
                    
                else:
                    dict[self.labels_short[counter]] = [entry]                

        return dict         


    def decode_as_str(self, code):
        """
        Function to decode an irma code to a str.

        Parameters
        ----------
        - code : str
            String to decode.

        Returns
        -------
        - decoded : str
            List of decoded strings.

        Tipps
        -------
        - Make use of 'decode_as_dict'
        - Possible solution: ['Imaging modality: x-ray, plain radiography, analog, overview image', 'Imaging orientation: coronal, anteroposterior (AP, coronal), supine', 'Body region: abdomen, unspecified', 'System: uropoietic system, unspecified']
        - Solution can look different -> FLASK will use this representation to visualize the information on the webpage.
        """
        str_dict = self.decode_as_dict(code)
        #conv_str = str(str_dict) #less code but not as pretty as the other solution
        conv_str = "["
        for key in str_dict:
            conv_str += "'" + key + ": "
            for elem in str_dict[key]:
                conv_str += elem + ", "
            conv_str = conv_str.removesuffix(', ')
            conv_str += "', "
        conv_str = conv_str.removesuffix(', ')
        conv_str += "]"
        return conv_str


if __name__ == '__main__':
    #add your specific path here
    pathname = os.path.abspath("exercise_2/Data/IRMA_data")
    
    image_names = ["1880.png"]

    irma = IRMA(pathname)

    codes = irma.get_irma(image_names)
    print("Codes: ", codes)

    if codes is not None:
        code = codes[0]
        print("Dict: \n{}\n\n".format(irma.decode_as_dict(code)))
        print("String: \n{}\n\n".format(irma.decode_as_str(code)))

    '''
    Result could look like this:


    Codes:  ['1121-127-700-500']
    Dict:
    {'Imaging modality': ['x-ray', 'plain radiography', 'analog', 'overview image'], 'Imaging orientation': ['coronal', 'anteroposterior (AP, coronal)', 'supine'], 'Body region': ['abdomen', 'unspecified'], 'System': ['uropoietic system', 'unspecified']}
    #700 in csvC does not exist and 500 in csvD

    String:
    ['Imaging modality: x-ray, plain radiography, analog, overview image', 'Imaging orientation: coronal, anteroposterior (AP, coronal), supine', 'Body region: abdomen, unspecified', 'System: uropoietic system, unspecified']
    '''