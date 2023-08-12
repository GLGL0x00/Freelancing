# Step-by-Step Guide to Run the Stock Scraper Script

## Requirements:
- **Python Installed:** Make sure you have Python installed on your machine. You can download the latest version of Python from the [official website](https://www.python.org/downloads/).

## Setup:

1. **Install Required Libraries:** Open a command prompt or terminal, navigate to the directory where `requirements.txt` is located, and install the required libraries using pip:


## Notes:

- If you encounter any errors during execution, make sure you have fulfilled all the requirements and provided correct input files with valid data.

- Ensure your directory structure looks like this:

```
--exe
  	|
  	|
	- ReportStocks_Scrapping.exe
--inputs
	|
	|
	- StockSymbols.txt
	- RunParameters.txt
--outputs
	|
	| "here you will find output results"
```


- The script will fetch data from a specific URL for each stock symbol provided in the `StockSymbols.txt` file. If the URL or website structure changes, the script might need modification.

- For more information on the code and its functionality, you can refer to the comments within the `ReportStocks_Scrapping.py` file.
