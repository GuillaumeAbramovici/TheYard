import pandas as pd
import csv
import os
from pathlib import Path


def merge_csv(csv1, csv2):
    """
    Merge two csv files upon the Title, and keep the most recent of all the possibilities
    :param csv1: First CSV file
    :param csv2: Second CSV file
    """

    # Read csv files
    csv_file_1 = pd.read_csv(csv1)
    csv_file_2 = pd.read_csv(csv2)

    # Concatenate the values of the csv, then sort by timedate and finally drop duplicated titles by keeping the first
    # one
    merged = pd.concat([csv_file_1, csv_file_2])
    merged.sort_values(merged.columns[2],
                axis=0,
                ascending=[False],
                inplace=True)
    merged = merged.drop_duplicates(subset='Title', keep='first')
    merged.to_csv('merged.csv', index=False)


if __name__ == '__main__':

    header = ['Title', 'Content', 'Date']
    csv1_data = ['Toy Story', 'Animated Movie', '27/03/1996']
    csv1_data2 = ['The Good, The Bad and The Ugly', 'Spaghetti', '10/03/1996']
    csv1_data3 = ['The Good, The Bad and The Ugly', 'Sergio Leone', '18/03/1996']
    csv2_data = ['The Good, The Bad and The Ugly', 'Western', '08/03/1968']
    csv2_data2 = ['Toy Story', 'Pixar', '08/05/1980']

    csv1_path = str(Path(os.getcwd() + '/movie1.csv'))
    csv2_path = str(Path(os.getcwd() + '/movie2.csv'))

    with open('movie1.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerow(csv1_data)
        writer.writerow(csv1_data2)
        writer.writerow(csv1_data3)
    f.close()

    with open('movie2.csv', 'w', encoding='UTF8', newline='') as f2:
        writer = csv.writer(f2)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerow(csv2_data)
        writer.writerow(csv2_data2)
    f2.close()

    merge_csv(csv1_path, csv2_path)
