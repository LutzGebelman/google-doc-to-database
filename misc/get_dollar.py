import requests
import xml.etree.ElementTree as ET 

def get_cur_value(id: str):
    return (ET.fromstring(requests.get("http://www.cbr.ru/scripts/XML_daily.asp").text).find(f".//Valute[@ID='{id}']/Value").text)
