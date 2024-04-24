# JSON Data Cleaning for Time Series Data(fill_gaps(1).py)

## Problem Description
The problem involves cleaning JSON data representing time series data captured by Linux. The data contains occasional instances where numeric values, such as open, high, low, close, and volume, are recorded as zeros. These zero values need to be replaced with the respective values from the previous non-zero entry to ensure the integrity of the time series data.

## Solution Overview
The provided solution is implemented in Python and utilizes the pandas library for data manipulation. It includes functionality to read JSON data in chunks, clean the data by replacing zero values with the previous non-zero values, and write the cleaned data back to a JSON file.

## Example JSON Data
Here's an example snippet of the input JSON data:

```json
{"time":1675461598000,"symbol":"ESH3","open":4146250000000.0,"high":4146250000000.0,"low":4146000000000.0,"close":4146000000000.0,"volume":156.0}
{"time":1675461599000,"symbol":"ESH3","open":4146250000000.0,"high":4146250000000.0,"low":4146000000000.0,"close":4146000000000.0,"volume":3.0}
{"time":1675461600000,"symbol":"ESH3","open":0.0,"high":0.0,"low":0.0,"close":0.0,"volume":0.0}
{"time":1675461601000,"symbol":"ESH3","open":0.0,"high":0.0,"low":0.0,"close":0.0,"volume":0.0}
{"time":1675461602000,"symbol":"ESH3","open":0.0,"high":0.0,"low":0.0,"close":0.0,"volume":0.0}
```
## Code Explanation
- The `fill_missing_values()` function iterates over the data and replaces zero values with the respective values from the previous non-zero entry.
- Data processing is done in chunks to efficiently handle large datasets, with each chunk being processed concurrently using threads.
- The script loads the JSON data in chunks, processes them concurrently using threads, concatenates the filled chunks into a single DataFrame, and writes the cleaned data back to a JSON file.

## Customization
- **Chunk Size**: Adjust the `chunk_size` variable in the script to optimize memory usage based on your system's capacity and dataset size.
- **Input Data**: Replace `'ES.json'` with the path to your input JSON file containing time series data.

## Dependencies
- Python 3.x
- pandas library
