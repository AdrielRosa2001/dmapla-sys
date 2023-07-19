
import cv2 
from pyzbar.pyzbar import decode
   
def BarcodeReader(image): 

    img = cv2.imread(image) 
       
    
    detectedBarcodes = decode(img)
       
    
    if not detectedBarcodes: 
        return "Codigo de barras não detectado!\nTente tirar uma foto mais legivel e com totalmente focada no codigo!"
    else: 
      for barcode in detectedBarcodes:
        if barcode.data!="": 
                return (str(barcode.data).replace("b","")).replace("'", "")

