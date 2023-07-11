import os, sys
from flask import Flask, render_template, request, send_from_directory, jsonify, make_response

from preprocessing import preprocessing_main
from query import Query
from irma import IRMA

"""
This is the main file to run the medical information retrieval server.
The following dataset can be used to retrieve similar images: https://publications.rwth-aachen.de/record/667228
"""
base_path = os.path.abspath("exercise_2/static")
database_path = os.path.join(base_path, "images", "database")
index_path =  os.path.join(base_path, "index.csv")
feeback_result = None
selected_image = None

query = Query(path_to_index= index_path)
irma = IRMA()
# TODO: remove comments not needed
quantity = 10

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    # base directory for the frozen app
    #base_dir  = os.path.join(sys._MEIPASS, 'templates')

    APP_ROOT = os.path.dirname(sys.executable)
    app = Flask(__name__, 
                static_folder=os.path.join(APP_ROOT, 'static'),
                template_folder=os.path.join(APP_ROOT, 'templates'))
elif __file__:
    APP_ROOT = os.path.dirname(__file__)
    app = Flask(__name__)

@app.route("/")
def index():
    global selected_image
    return render_template("start.html", selected_image= selected_image)

@app.route("/selected_image", methods=['POST'])
def select_query_image():
    global selected_image
    target = os.path.join(APP_ROOT, 'static/images/query')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        filename = file.filename
        if filename == '':
            return render_template("start.html", selected_image= selected_image)
        destination = "/".join([target, filename])
        file.save(destination)

    selected_image = filename

    global page
    page = 1

    return render_template("start.html", selected_image= selected_image)

@app.route("/query_result", methods=['POST'])
def start_query():

    target = os.path.join(APP_ROOT, 'static/images/query/')

    if not os.path.isdir(target):
        os.mkdir(target)

    query.set_image_name(query_image_name= target + selected_image)
    query_result = query.run(counter= 0, quantity= quantity)
    return visualize_query(query_result)

def visualize_query(query_result):
    image_names = [os.path.basename(x[1]) for x in query_result]

    # input infos
    input_code = irma.get_irma(image_names= [selected_image])
    input_info =[irma.decode_as_str(x) for x in input_code]

    return render_template("query_result.html", 
        zipped_input=zip([selected_image], input_code, input_info))#,  
     #zipped_results= zip(image_names, image_distances, image_codes, irma_infos))

@app.route("/load")
def load():
    """ Route to return the query results """

    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

    query_result = query.run(counter= counter, quantity= quantity)

    if len(query_result) == 0:
        print("No more posts")
        res = make_response(jsonify({}), 200)
        return res
    image_names = [os.path.basename(x[1]) for x in query_result]

    # results for retrieved images
    image_codes = irma.get_irma(image_names=image_names)
    irma_infos =[irma.decode_as_str(x) for x in image_codes]

    bundle = [ list(x) + [y] + z for x, y, z in zip (query_result, image_codes, irma_infos)]
    #bundle: 
    #distance 0
    #bildpfad
    #irma code
    #infos irma
    res = make_response(jsonify(bundle), 200)

    return res

@app.route("/recalc", methods=['POST'])
def recalc_index():

    preprocessing_main(image_directory = database_path, output_path="static/")

    global selected_image
    return render_template("start.html", selected_image= selected_image)

@app.route('/relevance_feedback', methods=['POST', 'GET'])
def relevance_feedback():
    global feeback_result

    # POST request
    if request.method == 'POST':

        images = request.get_data().decode('utf-8')
        images = images.split(';')

        selected_images = images[0].split(',')
        not_selected_images = images[1].split(',')

        selected_images = names_start_with(selected_images, start = database_path)
        not_selected_images = names_start_with(not_selected_images, start = database_path)

        global counter 
        counter = 0
        feeback_result = query.relevance_feedback(selected_images, not_selected_images, limit= quantity)

        return 'OK', 200

    if request.method == 'GET':
        return visualize_query(feeback_result)

def names_start_with(l, start):
    for i, name in enumerate(l):
        if not name.startswith(start):
            l[i] = start + name
    return l

if __name__ == "__main__":
    app.run(port=4555, debug=True)