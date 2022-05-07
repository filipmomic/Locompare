# development/testing script to simulate app

import addressfinder as addrfinder
import pointofinterest as poi
import distances as dist
import pandas as pd
import dataframeconversion as dfConv

if __name__ == "__main__":
    livingAddress1 = getInputAddress("1234 Address")
    print(livingAddress1)
    livingAddress2 = getInputAddress("5678 Address")

    # remove duplicates if entered by user
    arrPOI = ['target','starbucks','costco']
    mode = 'driving' #bicycling / walking
    print(arrPOI) 

    address1WithPOI = poi.searchForPOI(livingAddress1, arrPOI)
    address2WithPOI = poi.searchForPOI(livingAddress2, arrPOI)

    dist1 = dist.getDistanceMatrix(livingAddress1,address1WithPOI, mode)
    dist2 = dist.getDistanceMatrix(livingAddress2,address2WithPOI, mode)

    dfAddr1Results = dfConv.convertToDataFrame('current',livingAddress1, arrPOI, dist1)
    dfAddr2Results = dfConv.convertToDataFrame('new',livingAddress2, arrPOI, dist2)
    finalDf = pd.concat([dfAddr1Results, dfAddr2Results])
    finalDf.to_csv('results_walk.csv')
