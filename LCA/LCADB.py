import numpy as np
import csv
import pandas as pd
from pandas import DataFrame as df

class LCADB:

    def __init__(self, filepath):

        #Load LCA database from directory

        dataset = []
        with open(filepath, 'rt') as csvfile:
            lines = csv.reader(csvfile)

            for row in lines:
                dataset.append(row)

        csvD = []

        #csvD.append(dataset[0])
        for i in range(0, len(dataset)):
            row = []
            for j in range(0, len(dataset[i])):
                if i == 0:
                    row.append(dataset[i][j])
                else:
                    item = dataset[i][j]
                    row.append(item)
            csvD.append(row)
            # print np.array(data).astype(np.float)

            self.dataArray = csvD
            self.LCAdf = pd.DataFrame(data=csvD[1:], columns=csvD[0])
            self.LCA = {k: g["global_warming_potential_kg CO2-eq_c2g"].tolist() for k,g in self.LCAdf.groupby("CPID")}



    def factor (self, CPID):

        return float(self.LCA[CPID][0])

    def thickness(self, CPID):

        return float(self.LCA[CPID][0])

        #Specify material and retrieve the corresponding GWP factor
        #read through uploaded LCA csv and retrieve GWP factor for corresponding material

