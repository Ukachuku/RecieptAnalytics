from wand.image import Image as Img
import os, io
from google.cloud import vision
from google.cloud.vision import types

#convert pdf to jpg
os.chdir('/home/pi/Downloads/MarketPdf')
files = [f for f in os.listdir('.') if f.endswith('.pdf')]

for i in range(len(files)):
    with Img(filename=files[i], resolution=500) as img:
        img.compression_quality = 99
        img.save(filename='image_name' + str(i) + '.jpg')
        
jpgfiles = [f for f in os.listdir('.') if f.endswith('.jpg')]       
#google vision        
client = vision.ImageAnnotatorClient()

for i in range(len(jpgfiles)):
    file_name = os.path.join(
        os.path.dirname(__file__),
        jpgfiles[i]
        )
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        
        image = types.Image(content=content)
        response = client.document_text_detection(image=image)
        document = response.full_text_annotation
        
        file = open('output' + str(i) + '.txt', 'w')
        file.write(str(document))
        file.close