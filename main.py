from flask import Flask, make_response, request, render_template

app = Flask(__name__)

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route('/')
def form():
    return render_template("index.html")

@app.route('/transform', methods=["POST"])
def transform_view():
    request_file = request.files['data_file']
    data_type = request.form["data_type"]
    if not request_file:
        return "No file"

    file_contents = request_file.stream.read().decode("utf-8")

    if data_type == "json":
        result = transform(file_contents)
    elif data_type == "csv":
        result  =transform(file_contents)

    print(data_type)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response
