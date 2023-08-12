import requests
from bs4 import BeautifulSoup
from time import sleep
import os
import datetime

def runParameter():
    """ Description: Read inputFile-1 This record has 3 fields named 
                    ReportNamePrefix 
                    WaitTime
                    OutputCriteria 
        return: ReportNamePrefix, WaitTime, OutputCriteria,url
    """
    count=0
    try:
        with open('..\inputs\RunParameters.txt', 'r') as file:
            # Read first line 
            line1 = file.readline().strip()
            fields = line1.split(',')

            if len(fields) != 3:
                print("Error: line 1 does not contain 3 fields separated by commas.")
                return None
            
            if fields[1].isdigit() and (fields[2].lower() == "selected" or fields[2].lower() == "all") :

                # You can access the fields using fields[0], fields[1], and fields[2]
                ReportNamePrefix = fields[0]
                WaitTime = int(fields[1])
                OutputCriteria = fields[2]

                # # Read Second Line contain paths 
                # line2 = file.readline().strip()
                # line2 = line2.replace('\\',"\\\\")
                # paths = line2.split(';')
                # if len(paths) != 3:
                #     print("Error:line 2 does not contain 3 paths separated by ; \n\tshould contain input and executable and output path in order.")
                # #     return None
                # else:
                #     input_path = paths[0]
                #     exe_path = paths[1]
                #     output_path = paths[2]

                # Read Third Line contain url 
                url = file.readline().strip()

                return ReportNamePrefix, WaitTime, OutputCriteria,url
            else:
                print("Error: Check Fields Of line1 Either WaitTime is not number OR\n "+
                    "\tOutputCriteria not equal selcted or all ")
    except FileNotFoundError:
        print("Error: runParameter File not found.")
        return None

def StockSymbols():
    """
        Description: Read StockSymbols file which has 0 to N records source&symbol
        return: list of data contain tuples of source and symbol
    """
    data = []
    try:
        with open('..\inputs\StockSymbols.txt', 'r') as file:
            for line in file:
                try:
                    source, symbol = line.strip().split(',')
                    data.append((source, symbol))
                except:
                    continue

            # print("End Of StockSymbols file!\n----------------------------------")
        if len(data) == 0:
            print("StockSymbols File Is Empty!!")
    except FileNotFoundError:
        print("Error: StockSymbols File not found.")
        return None

    return data

def data_scrapper(url, ticker):
    url = url + ticker

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        recommendation = soup.find('div', {'id': 'Content_LastSignal'}).text
        recommendation

        soup = BeautifulSoup(res.text, 'html.parser')
        current_signal = soup.find('div', {'class': 'row mx-0 px-0 my-0 pt-1 pb-0'}).find('div', {'class':"row mx-0 px-0"}).find('div',{'id':"Content_LastSignal"}).text.split()[0:3]
        current_signal = ' '.join(current_signal) 
        current_signal = current_signal.strip()
        # print(current_signal)
        Date = soup.find('td', {'id': 'Content_SignalHistory_SignalShortHistoryGrid_tccell0_0'}).text.strip()
        # print (Date)
        price = soup.find('td', {'class': 'dxbs-nlb dxbs-nrb text-right'}).text
        # print (price) 
        signal = soup.find('td', {'id': 'Content_SignalHistory_SignalShortHistoryGrid_tccell0_2'}).text.replace("\n","")
        # print (signal)

        return Date,price,signal,current_signal
    except:
        return ticker

def output(ReportNamePrefix,info,OutputCriteria):
    """Create new output file with this format Growth_StockReport_YYYYMMDD_HHMMSS.txt"""

    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time in the desired format
    formatted_date = now.strftime("%Y%m%d")
    formatted_time = now.strftime("%H%M%S")

    # Create the filename using the formatted date and time
    filename = f"{ReportNamePrefix}_StockReport_{formatted_date}_{formatted_time}.txt"
    path="..\outputs\\"
    # Combine the specified save_path with the filename
    file_path = os.path.join(path, filename)

    # Create the file
    with open(file_path, 'w') as file:
        if OutputCriteria.lower()=="all":
            file.write("SOURCE\t SYMBOL\t DATE\t PRICE\t SIGNAL\t CURRENT SIGNAL\n")
            file.write("------\t ------\t ----\t -----\t ------\t --------------\n")
        else:
            file.write("SOURCE\t SYMBOL\t DATE\t PRICE\t SIGNAL\n")
            file.write("------\t ------\t ----\t -----\t ------\n")
        for l in info:
            # it means that invalid symbol 
            # print(len(l))
            # print(l)
            if len(l)==2:
                file.write(f"{l[0]}\t {l[1]}\t - Invalid Symbol\n")
            else:
                if OutputCriteria.lower()=="all":
                    #  print(l[5])
                     file.write(f"{l[0]}\t {l[1]}\t {l[2]}\t {l[3]}\t {l[4]}\t {l[5]}\n")
                     
                elif  OutputCriteria.lower()== "selected":
                    if l[5] == "BUY" or l[5] == "SELL" or l[5] == "SHORT":
                        file.write(f"{l[0]}\t {l[1]}\t {l[2]}\t {l[3]}\t {l[4]}\n")
                    else:
                        continue



             

    print(f"New file created: {filename}")

if __name__== "__main__":
    data = list()
    result =runParameter()
    count = 1
    if result: 
        print("[INFO]: Program runs wait to finish!!")
        ReportNamePrefix, WaitTime, OutputCriteria,url= result

        source_tickers = StockSymbols()

        for source, ticker in source_tickers:
            try:
                date,price,signal,graph= data_scrapper(url,ticker)
                data.append([source, ticker,date,price,signal,graph])
            except:
                ticker = data_scrapper(url,ticker)
                data.append([source,ticker])
            
            print(f"Currently processing in symbol'{ticker}', which is {count} out of {len(source_tickers)}")
            
            sleep(WaitTime)
            count +=1

        output(ReportNamePrefix,data,OutputCriteria)
    