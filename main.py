import os 
import glob
import random
from image_handler import convertImageMaker
from image_generator import imageGeneratorOpenAI

# imageGenerator = imageGeneratorOpenAI()
# imageGenerator.generate_image("A picture of a building with clear lines and edges, such as a skyscraper or a bridge.", 1, '512x512', 'b64_json') 
# imageGenerator.write_image()

files = glob.glob('./crop_images/*')
for f in files:
    os.remove(f)

convertTest = convertImageMaker() 
convertTest.image_extract('pokemon') 
# convertTest.image_save_crop_location() 
# convertTest.image_convert(convert_type=random.randint(1, 2)) 
# convertTest.image_convert(convert_type=1) 
convertTest.image_convert2() 
# convertTest.image_convert(convert_type=1)