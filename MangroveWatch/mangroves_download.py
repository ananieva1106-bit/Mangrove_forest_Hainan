# Geoscripting project : Mangrove forests in Hainan, China
# Authors : Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger, Roxane Marguerat
# Period 1, October 2026
# This script is licensed under the MIT License
# Sources are referenced throughout the script

# This script downloads extent of mangrove cover as shapefile vector 
# for the region of China between 1990 and 2020
# Run this script first before main.py, see README.md for instructions

# Importing the packages
import urllib.request
import patoolib
import os

# Creating data/vector subdirectories here independently of main.py 
if not os.path.exists("data"): # Source: Exercise 10 solution
    os.mkdir("data")

if not os.path.exists("data/vector"):
    os.mkdir("data/vector")

# Downloading the Mangroves in China vector rar file 
# Source - https://stackoverflow.com/a/56129059, Posted by Om Sao, Retrieved 2026-10-12, License - CC BY-SA 4.0
if not os.path.exists('data/vector/mangroveschina.rar'):
    urllib.request.urlretrieve('https://china.scidb.cn/download?fileId=519056ceb0f18ff4b9c70ac82b3a9e9e&traceId=fcf56882-aef5-47a2-b321-a5f1a176a63b', 'data/vector/mangroveschina.rar')
    print("Downloading mangroveschina.rar...")
else: 
    print('RAR file already downloaded!')

# Unpacking the rar file 
# Source - https://stackoverflow.com/a/26178369, Posted by Amir, modified by community. See post 'Timeline' for change history, Retrieved 2026-10-12, License - CC BY-SA 4.0
if not os.path.exists('data/vector/Mangrove Dynamics in China'):
    patoolib.extract_archive("data/vector/mangroveschina.rar", outdir="data/vector", interactive=False)
    print("Unpacking vector shapefiles...")
else:
    print('Folder containing the vector shapefiles already exist!')

