import numpy as np
import pandas as pd
import requests
from utils.utility import hexToInt
from datetime import datetime
import time

class prepareData():
    def __init__(self, w3,conf,ySNX):
        self.w3            = w3
        self.ySNX          = ySNX
        self.conf          = conf
        self.filter        = {'address': ySNX["address"],
                              "fromBlock": hex(1),
                              "toBlock": 'latest',
                              'topics': [w3.keccak(text='Transfer(address,address,uint256)').hex()]}
        
    def launchDataGathering(self,startDate,endDate):

        #First get the timesteps
        timesteps  = self.getTimesteps(startDate,endDate)
        
        #Remove future timesteps
        timesteps  = [timestep for timestep in timesteps if timestep < time.time() - 3600]
        
        #Get blockNumbers of these timesteps
        blocksteps = [self.getBlockNumber(timestep) for timestep in timesteps]
        
        #First get all transfer topics
        df      = self.getTransferTopics(blocksteps)
        
        #get vector of pps
        ppsList = self.getPricePerShareList(blocksteps)
        
        #Figure out the snx balance for each addy
        df = df.multiply(ppsList).divide(1e36)
        
        #get the average balance
        avgDF = df.mean(axis=1)
        
        #format them
        cols = [self.getDateStringFromTimestamp(timestamp) for timestamp in timesteps]
        cols.append('avg')
        df   = pd.concat([df,avgDF],
                         axis=1,
                         ignore_index=True)
        df.columns = cols
        
        df = df.query("avg>0").copy()
        
        df.to_csv("output/dataOutput.csv")
                
    def getTransferTopics(self,blocksteps):
        
        df                 = pd.DataFrame(self.w3.eth.filter(self.filter).get_all_entries())
        df["from_address"] = '0x'+ df.topics.str[1].apply(lambda x : x.hex()).str[-40:]
        df["to_address"]   = '0x'+ df.topics.str[2].apply(lambda x : x.hex()).str[-40:]
        df["value"]        = df.data.apply(hexToInt)
        df                 = df[~(df["from_address"]==df["to_address"])].copy()
        df                 = df[["blockNumber","from_address","to_address","value"]].copy()
        
        finalDF            = pd.DataFrame()
        
        #get list of unique addy's
        addresses = set(df.from_address).union(df.to_address)
        
        #iterate on all addresses
        for address in addresses:
            
            #filter the address
            dfFiltered           = df.query("from_address ==  @address or to_address == @address").copy()
            #flip to + 1 if inflow -1 if outflow
            dfFiltered["amount"] = dfFiltered["to_address"].apply( lambda x: 1 if x == address else -1) * df["value"]
            
            #do some matrix map/reduction
            matrixBlockNumber = np.repeat(a=dfFiltered[["blockNumber"]].to_numpy(),repeats=len(blocksteps)).reshape(len(dfFiltered),len(blocksteps))
            matrixAmount      = np.repeat(a=dfFiltered[["amount"]].to_numpy(),repeats=len(blocksteps)).reshape(len(dfFiltered),len(blocksteps))

            #save the result
            tempDF = pd.DataFrame(data = np.where(matrixBlockNumber<=blocksteps,matrixAmount,0),
                                  columns=blocksteps).sum(axis=0)
            
            #Make column name as the addy
            tempDF.rename(address,inplace=True)
            
            #group with final DF
            finalDF           =  pd.concat([finalDF,tempDF],axis=1)
            
        return finalDF.T
                        
    def getPricePerShareList(self,blocksteps):
        #get the contract
        contract = self.w3.eth.contract(address=self.ySNX["address"],
                                        abi=self.ySNX["abi"])
                
        ppsList = [contract.functions.pricePerShare().call(block_identifier=blockNumber) for blockNumber in blocksteps]
            
        return ppsList

    def getTimesteps(self,initialDate,endingDate):
        
        initialTimestamp = self.getTimestampFromString(initialDate)
        endingTimestamp  = self.getTimestampFromString(endingDate)
        
        return list(range(initialTimestamp,endingTimestamp,3600*24 + 1))

    def getTimestampFromString(self,dateString):
        return int(datetime.strptime(dateString, '%d-%b-%Y').timestamp())

    def getDateStringFromTimestamp(self,timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%d/%b/%Y")

        
    def getBlockNumber(self,timestamp):
        etherscanKey = self.conf["etherscan"]
        url          = f'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={etherscanKey}'
        result = requests.get(url)
        return int(result.json()["result"])
        
        
#%%
if __name__ == '__main__':
    data = prepareData(w3 = w3,conf=conf,ySNX=ySNX)
    self = data
    
