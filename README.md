# Geoscripting project : Mangrove forest development in Hainan, China
## Authors : Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger, Roxane Marguerat
***Period 1, october 2026***

*This script is licensed under the MIT License*

*Sources are reference throughout the script*

## Description of the project
The objective of our project is to visualize the changes in health, cover and quality of mangrove forest on Hainan Island (China).

The health and quality of mangrove forest is defined by three indexes :
- NDVI : normalized difference vegetation index
- NDMI : normalized difference moisture index
- Fragmentation index assessed by the edge-to-area ratio

All these indexes as well as the cover area of the mangrove are vizualized on an interactive map over on time points between 1996 and 2020.


## Instruction for running
In order to correctly carry out the first step of the pipeline (downloading the Mangrove cover in China vector dataset),
the function has to be ran as a task through pixi from the bash (or pixi) shell.

**Option 1**- from the bash shell:
In the bash terminal type: 

``pixi run mangrovesdownload``

**Option 2** - from the pixi shell:
In the bash terminal open the pixi shell by tiping: 

`pixi shell`

Then in the pixi terminal type: 

`run mangrovesdownload`

Once the Mangrove cover in China dataset in downloaded, simply run the main.py script.

## Instruction to retrieve data manually (if needed)
We made our data available on Teams ***(put a link ?)*** in case something goes wrong with the downloading, so it's still possible to run the rest of the script; or if it takes too long to download everything from the script.

Before running the main script :
- Put the content of "mangrove vector data " in the following directory :

`data/vector/Mangrove Dynamics in China`

- Put the content of "landsat data" in the following directory :

`data/landsat_data`

- Comment the section DOWNLOAD DATA in main.py
- Skip the instruction about downlaoding the mangrove data using pixi and run main.py normally


## Data sources (to update ?)
https://www.scidb.cn/en/detail?dataSetId=195bcf0052384d599917c2f656e2dc4a#detail_start <- link to mangrove vector data from 1990 to 2020 in China

Bbox for Hainan from bboxfinder.com: 
- EPSG4326 WGS84: 108.506470, 18.151072, 111.088257, 20.190035,  (Lng/Lat) # (Lng/Lat) is the preferred method for python functionality
- EPSG3857 WGS84: 2055238.8165,12078884.9577,2295556.8335,12366288.1841 (Lat/Lng)

https://earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/

