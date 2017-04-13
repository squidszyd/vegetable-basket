# vegetable-basket                                                               
The Vegetable-Basket Program (SED data protocal)                                 
                                                                                  
## Data file conversion                                                          
### Definition:                     
|VAR_NAME    |   MEANING |
|:----------:|:---------:|
|FRAME_ID   | **0-based** frame id  [*int32*]    |
|NUM_OF_BOXES_IN_FRAME  |num of boxes in a frame    [*int32*]  |
|COORDINATE |Box coordinate [x1, x2, y1, y2]   [*4\*int32*]  |
|CONFIDENCE |Box confidence [*float32*] |
|CLASS_ID   |Box class [*int32*]    |

### Structure of different types of data files:                                                              
- [.data]   No matter how many boxes a frame contains, FRAME_ID and NUM_OF_BOXED_IN_FRAME will be saved
```
{[FRAME_ID][NUM_OF_BOXES_IN_FRAME][NUM_OF_BOXES_IN_FRAME * BOX]} x frame_nums
```
- [.dt] Stores boxes, each box is represented by FRAME_ID and COORDINATE
```
{[FRAME_ID][COORDINATE]} x box_nums
```                                                                                 
- [.dtm] Stores extended boxes, with FRAME_ID, CLASS_ID, CONFIDENCE and COORDINATE
```
{[FRAME_ID][CONFIDENCE][CLASS_ID][COORDINATE]} x box_nums
```                    
- [.pkl]    Python dict in which the keys are FRAME_IDs and the values are lists [CONFIDENCE, CLASS_ID, COORDINATE]
```
{
    0:  [CONFIDENCE, CLASS_ID, COORDINATE]
    1:  [CONFIDENCE, CLASS_ID, COORDINATE]
    ...
    N:  [CONFIDENCE, CLASS_ID, COORDINATE]
}
```

.data and .dt are **not** recommended to be used. Use .dtm (C++) and .pkl (Python) instead.
To convert from one type to another, call:
```
python data_converter.py --source [datafile.xxx | list-of-file-to-be-converted.txt] --savetype [data | dt | dtm | pkl | xml]
```
