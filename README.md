# vegetable-basket
The Vegetable-Basket Program (SED data protocal)

## Data file conversion
Definition:
- FRAME_ID:	**0-based**, frame id, *int32*
- NUM_OF_BOXES_IN_FRAME: num of boxes in a frame, *int32*
- BOX: Structure contains coordinates: [x0, y0, x1, y1] *int32* and confidence *float32*
- CLASS: Class ID, *int32*

Type of data files:
- .data
`[[FRAME_ID][NUM_OF_BOXES_IN_FRAME][NUM_OF_BOXES_IN_FRAME * BOX]]`
- .dt

- .dtm

- .pkl
