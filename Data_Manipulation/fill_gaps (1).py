import pandas as pd
import threading

def fill_missing_values(data):
    filled_data = data.copy()

    for index, row in filled_data.iterrows():
        if row['open'] == 0.0:
            prev_row_index = index - 1
            if prev_row_index >= 0:
                filled_data.at[index, 'open'] = filled_data.at[prev_row_index, 'open']
                filled_data.at[index, 'high'] = filled_data.at[prev_row_index, 'high']
                filled_data.at[index, 'low'] = filled_data.at[prev_row_index, 'low']
                filled_data.at[index, 'close'] = filled_data.at[prev_row_index, 'close']

    return filled_data

def process_chunk(chunk, filled_chunks):
    chunk.reset_index(drop=True, inplace=True)  # Reset index for each chunk
    filled_chunk = fill_missing_values(chunk)
    filled_chunks.append(filled_chunk)

# Chunk processing size
chunk_size = 100000  # Adjust according to your system's memory capacity

# Load JSON data into pandas DataFrame in chunks
chunks = pd.read_json('ES.json', lines=True, chunksize=chunk_size)

# Process chunks using threads
filled_chunks = []
threads = []
for chunk in chunks:
    thread = threading.Thread(target=process_chunk, args=(chunk.copy(), filled_chunks))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Concatenate filled chunks into a single DataFrame
filled_df = pd.concat(filled_chunks)

# Write filled data back to JSON file
filled_df.to_json('filled_data.json', orient='records', lines=True)








