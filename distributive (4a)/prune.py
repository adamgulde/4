import os
import pandas as pd

# combined_csv_df = pd.DataFrame() 
# directory = ''
# print(directory)
# files = os.listdir(directory)
# for file in files:
#     if file.endswith(".csv"):
#         combined_csv_df = pd.concat([pd.read_csv(os.path.join(directory,file)), combined_csv_df])
# print(combined_csv_df.shape)
# pruned_array = []
# for entry in combined_csv_df.itertuples():
#     if entry[2] == 1:
#         pruned_array.append(str(entry[1]).removesuffix('/info'))

# import datetime as dt
# timestamp = str(dt.datetime.now().date())
# with open(f'Users Downloaded at{timestamp}.txt', 'w') as f:
#     for entry in pruned_array:
#         f.write(f'{entry}\n')

def prune(filename):
    pruned_array = []
    csv_df = pd.read_csv(filename)
    for entry in csv_df.itertuples():
        if entry[2] == 1:
            pruned_array.append(str(entry[1]).removesuffix('/info').removeprefix('https://bishopmoore.schoology.com/user/'))
    return pruned_array