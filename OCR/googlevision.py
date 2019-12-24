import io
import os
from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()

file_name = os.path.join(
	os.path.dirname(__file__),
	'reciept.jpg'
	)
with io.open(file_name, 'rb') as image_file:
	content = image_file.read()

image = types.Image(content=content)

response = client.document_text_detection(image=image)

document = response.full_text_annotation

os.chdir('/home/pi/gcloudstuff')
file = open('output.txt', 'w')
file.write(str(document))
file.close
