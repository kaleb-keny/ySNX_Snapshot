import argparse
import web3 as w3
from utils.dataGathering import prepareData
from utils.utility import parse_config

conf       = parse_config(r"config/conf.yaml")
ySNX       = parse_config(r"config/ySNX.yaml")
w3         = w3.Web3(w3.HTTPProvider('https://mainnet.infura.io/v3/{}'.format(conf["infura"])))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='get ySNX holders snapshots')

    parser.add_argument("-d",
                        "-dates",
                        type=str,
                        nargs='+',
                        required=True,
                        help='enter start and end dates like 01-jan-2021 and 31-jan-2021'
                        )
 
    args = parser.parse_args()
    
    
    if len(args.d) == 2 :
        data = prepareData(w3=w3, 
                           conf=conf,
                           ySNX=ySNX)
                          
        data.launchDataGathering(startDate=args.d[0],
                                 endDate=args.d[1])
            
        print("Data saved successfully under output folder")

    else:
        print("doing nothing wrong args")
