from fastapi import FastAPI, File, UploadFile, Request
import uvicorn
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
from fastapi.templating import Jinja2Templates

import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

app = FastAPI()

CLASSES = ["Potato___Early_blight", "Potato___healthy", "Potato___Late_blight"]

MODEL = tf.keras.models.load_model('Models/1')


templates = Jinja2Templates(directory="htmldir")


## defining endpoints
@app.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

def read_image(data):
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    
    image_data = await file.read()
    image = read_image(image_data)
    img_batch = np.expand_dims(image, 0)
    prediction = MODEL.predict(img_batch)
    index = np.argmax(prediction[0])
    predicted_cls = CLASSES[index]
    confidence = float(np.max(prediction[0]))

    return {
        "class": predicted_cls,
        "confidence": confidence
    }

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request":request})


# main function
if __name__=="__main__":
    uvicorn.run("app:app", reload=True)
