### Running this script will download and unpack the .rar file containing 
### shapefile vectors for mangrove cover in China from 1990 to 2020

# Importing necessary packages
import urllib.request
import patoolib
import os

def mangroves_download(output_path = "data/vector"):
    """
    Retrieve the .rar file from url and unpack:
    Paramaters: output_path = desired path to unpack the downloaded .rar file"
    """
    # Create vector folder subdirectory here independently of main.py
    if not os.path.exists("data/vector"):
        os.mkdir("data/vector")

    #  (Source: https://stackoverflow.com/questions/19602931/basic-http-file-downloading-and-saving-to-disk-in-python)
    # Downloading the Mangroves in China vector rar file 
    # Source - https://stackoverflow.com/a/56129059
    # Posted by Om Sao
    # Retrieved 2026-10-12, License - CC BY-SA 4.0
    if not os.path.exists('data/vector/mangroveschina.rar'):
        urllib.request.urlretrieve('https://china.scidb.cn/download?fileId=519056ceb0f18ff4b9c70ac82b3a9e9e&traceId=fcf56882-aef5-47a2-b321-a5f1a176a63b', 'data/vector/mangroveschina.rar')
    else: 
        print('RAR file already downloaded!')

    # Creating output folder for the rar file contents
    if not os.path.exists("data/mangroveschina"): # source : exercice 10 solution
        os.mkdir("data/mangroveschina")

    # Unpacking the rar file (Source: https://stackoverflow.com/a/26178369)
    patoolib.extract_archive("data/vector/mangroveschina.rar", outdir=output_path)

