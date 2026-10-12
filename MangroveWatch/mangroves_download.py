### Running this script will download and unpack the .rar file containing 
### shapefile vectors for mangrove cover in China from 1990 to 2020

# Importing necessary packages
import urllib.request
import patoolib
import os

# Create vector folder subdirectory here independently of main.py (Source: Exercise 10 solution)
if not os.path.exists("data/vector"):
    os.mkdir("data/vector")

# Downloading the Mangroves in China vector rar file 
# Source - https://stackoverflow.com/a/56129059, Posted by Om Sao, Retrieved 2026-10-12, License - CC BY-SA 4.0
if not os.path.exists('data/vector/mangroveschina.rar'):
    urllib.request.urlretrieve('https://china.scidb.cn/download?fileId=519056ceb0f18ff4b9c70ac82b3a9e9e&traceId=fcf56882-aef5-47a2-b321-a5f1a176a63b', 'data/vector/mangroveschina.rar')
else: 
    print('RAR file already downloaded!')

# Unpacking the rar file (Source: https://stackoverflow.com/a/26178369)
if not os.path.exists('data/vector/Mangrove Dynamics in China'):
    patoolib.extract_archive("data/vector/mangroveschina.rar", outdir="data/vector", interactive=False)
else:
    print('Folder containing the vector shapefiles already exist!')

