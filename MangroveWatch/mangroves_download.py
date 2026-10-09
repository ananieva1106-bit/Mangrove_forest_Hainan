import urllib.request
import patoolib
import os # could be removed, added in main.py

# Function that downloads and unpacks the mangroves in china vector dataset
def mangroves_download(output_path = "data/vector"):
    # Downloading the Mangroves in China vector rar file(Source: https://stackoverflow.com/questions/19602931/basic-http-file-downloading-and-saving-to-disk-in-python)
    if not os.path.exists('data/vector/mangroveschina.rar'):
        urllib.request.urlretrieve('https://china.scidb.cn/download?fileId=519056ceb0f18ff4b9c70ac82b3a9e9e&traceId=fcf56882-aef5-47a2-b321-a5f1a176a63b', 'data/vector/mangroveschina.rar')
    else: 
        print('RAR file already downloaded!')

    # Creating output folder for the rar file contents
    if not os.path.exists("data/mangroveschina"): # source : exercice 10 solution
        os.mkdir("data/mangroveschina")

    # Unpacking the rar file (Source: https://stackoverflow.com/a/26178369)
    patoolib.extract_archive("data/vector/mangroveschina.rar", outdir=output_path)

