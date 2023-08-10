# Creates app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pickle
import json 
import uvicorn
import logging


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Specifying to ensure the right input from requests
class model_input(BaseModel):
   
   zipcode: int
   lot_len: float
   lot_area: int
   house_area:int
   garden_size: int
   y_coor: int
   energy_eff: int
   
   # loading the saved model
model = pickle.load(open('model.pkl', 'rb'))

@app.post('/house_prediction')
def house_predd(input_parameters : model_input):
    logging.info(f"Received prediction request: {input_parameters}")

    input_data = input_parameters.json()
    # Converts to dict
    input_dictionary = json.loads(input_data)
    
    # Gets the values of the keys
    zip = input_parameters.zipcode
    lotl = input_parameters.lot_len
    lota = input_parameters.lot_area
    house = input_parameters.house_area
    garden = input_parameters.garden_size
    y_coor = input_parameters.y_coor
    eff = input_parameters.energy_eff

    input_list = [zip, lotl, lota, house, garden, y_coor, eff]    
    # Use saved model to predict
    prediction = model.predict([input_list])
    # Inside your route function
    prediction_result = prediction[0]
    response_data = {"prediction": prediction_result}
    return JSONResponse(content=response_data)
    


