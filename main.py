from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# init Ninja Api
app = FastAPI()

#---------------------------------#
def scrapp_nbt(date):
    nbt2 = requests.get(f"https://nbt.tj/ru/kurs/export_xml.php?date={date}&export=xmlout")
    soup2 = BeautifulSoup(nbt2.content, 'lxml')
    valutes = soup2.find_all('valute')
    keys = soup2.find_all('charcode')
    values = soup2.find_all('value')
    VALUTES = {keys[i].text:values[i].text for i in range(len(valutes)-1)}
    return VALUTES


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/nbt")
def read_root():
    return scrapp_nbt(str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day))
