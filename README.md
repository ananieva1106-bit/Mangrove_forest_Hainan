### Instruction for running everything correctly
In order to correctly carry out the first step of the pipeline (downloading the Mangrove cover in China vector dataset),
the function has to be ran as a task through pixi from the bash (or pixi) shell.

Option 1 - from the bash shell:
In the bash terminal type: pixi run mangrovesdownload

Option 2 - from the pixi shell:
In the bash terminal open the pixi shell by tiping: pixi shell
In the pixi terminal type: run mangrovesdownload

## Handy information to quickly save
https://www.scidb.cn/en/detail?dataSetId=195bcf0052384d599917c2f656e2dc4a#detail_start <- link to mangrove vector data from 1990 to 2020 in China

Bbox for Hainan from bboxfinder.com: 
- EPSG4326 WGS84: 108.506470, 18.151072, 111.088257, 20.190035,  (Lng/Lat) # (Lng/Lat) is the preferred method for python functionality
- EPSG3857 WGS84: 2055238.8165,12078884.9577,2295556.8335,12366288.1841 (Lat/Lng)

https://earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/

