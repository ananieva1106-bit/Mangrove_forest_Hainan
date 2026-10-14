# Geoscripting project : Mangrove forest development in Hainan, China
## Authors : Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger, Roxane Marguerat
***Period 1, october 2026***

*This script is licensed under the MIT License*

*Sources are referenced throughout the script*

## Description of the project
The objective of our project is to visualize the changes in health, cover and quality of mangrove forests on Hainan Island (China).

The health and quality of mangrove forest are indicated by three indexes :
- NDVI : normalized difference vegetation index (range: -1 to 1; detecting how "green" vegetation is; the closer the index value is to 1, the greener vegetation is)
- NDMI : normalized difference moisture index (range: -1 to 1; detecting how "moist" vegetation is; the closer the index value is to 1, the higher the moisture of vegetation)
- Fragmentation index assessed by the edge-to-area ratio (the lower the value, the less mangrove forests are fragmented)

For more information on NMVI and NDMI, we suggest to consult the folowing web-page: https://www.agricolus.com/en/vegetation-indices-ndvi-ndmi/ 

All these indexes as well as the cover area of the mangrove are vizualized on an interactive map over time points between 1996 and 2020.


## Instructions for running
First, isntall the environment by running 

`pixi install`

In order to correctly carry out the first step of the pipeline (downloading the Mangrove cover in China vector dataset),
the function has to be ran as a task through pixi from the bash (or pixi) shell.

**Option 1**- from the bash shell:
In the bash terminal type: 

``pixi run mangrovesdownload``

**Option 2** - from the pixi shell:
In the bash terminal open the pixi shell by typing: 

`pixi shell`

Then in the pixi terminal type: 

`run mangrovesdownload`

Once the Mangrove cover in China dataset in downloaded, simply run the `main.py` script.

Note : the layers can take a little time to show on the dashboard

## Instruction to retrieve data manually (if needed)
The script is supposed to retrieve the data automatically.
However, in case something goes wrong with the downloading, or if it takes too long to download everything from the script, we made our data available on Teams (https://wageningenur4.sharepoint.com/:f:/s/Geoscripting-MangroveWatch/IgAwigoJ2lGCR7SoWSx-h5JSAUY9uhcNlea80h5TtdGHbyU?e=008M3h) so it's still possible to run the rest of the script.

Before running the main script :
- Put the content of "vector data" in the following directory :

`data/vector/Mangrove Dynamics in China`

- Put the content of "landsat data" in the following directory :

`data/landsat_data`

- Comment the section DOWNLOAD DATA in main.py
- Skip the instruction about downlaoding the mangrove data using pixi and run main.py normally

### OPTIONAL: Instruction to change the years chosen for the analysis
If the user wishes to analyze different years than the default ones, this can be done by changing the `years` variable to include the years the user wishes to utilize (ranging from 1996 to 2020). Updating this variable has to be done **in the same way** in these two places:

1. In `main.py`
2. In `map_dash.py`

## Data sources
- Mangrove extent vector data :
https://www.scidb.cn/en/detail?dataSetId=195bcf0052384d599917c2f656e2dc4a#detail_start 

- Catalogue use to retrive landsat data:
https://earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/

- Bbox for Hainan from bboxfinder.com: 
https://bboxfinder.com



