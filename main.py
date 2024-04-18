from fastapi import FastAPI, UploadFile
from inference import FileParser

app = FastAPI(debug=True)
parser = FileParser()


@app.get("/")
def handle_get():
    return {'data': []}


@app.post('/')
def handle_post(file: UploadFile):
    return parser(file.file)
