import os 
import glob
from image_handler import convertImageMaker
from image_generator import imageGeneratorOpenAI

# imageGenerator = imageGeneratorOpenAI()
# imageGenerator.generate_image("a pokemon picture", 1, '512x512', 'b64_json') 
# imageGenerator.write_image()

files = glob.glob('./crop_images/*')
for f in files:
    os.remove(f)


convertTest = convertImageMaker() 
convertTest.image_extract('pokemon') 
convertTest.image_convert(convert_type=5)