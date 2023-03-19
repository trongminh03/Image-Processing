from image_handler import convertImageMaker
import os 
import glob
import random
from image_generator import imageGeneratorOpenAI

imageGenerator = imageGeneratorOpenAI()
imageGenerator.generate_image("cartoon network picture", 1, '512x512', 'b64_json') 
imageGenerator.write_image()

files = glob.glob('./crop_images/*')
for f in files:
    os.remove(f)

convertTest = convertImageMaker() 
convertTest.image_extract() 
convertTest.image_save_crop_location() 
# convertTest.image_convert(convert_type=random.randint(1, 2)) 
convertTest.image_convert(convert_type=1)