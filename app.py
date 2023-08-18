from fastapi import FastAPI, File, UploadFile   
import uvicorn
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf


app = FastAPI()

CLASSES = ["Potato___Early_blight", "Potato___healthy", "Potato___Late_blight"]

MODEL = tf.keras.models.load_model('Models/1')


## defining endpoints
@app.get("/")
def homepage():
    return "WELCOME TO FASTAPI"

def read_image(data):
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    
    image = read_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    prediction = MODEL.predict(img_batch)
    index = np.argmax(prediction[0])
    predicted_cls = CLASSES[index]
    confidence = float(np.max(prediction[0]))

    return {
        "class": predicted_cls,
        "confidence": confidence
    }

# main function
if __name__=="__main__":
    uvicorn.run("app:app", reload=True)