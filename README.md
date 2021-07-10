# ySNX Stakeholder Snapshot
The repo contains the tools necessary to get the staked amount per address, in snx, with  daily snapshots between 2 specified dates:

## Prerequisites

The code needs miniconda, as all packages were installed and tested on conda v4.9.2. Installation of miniconda can be done by running the following:

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -p $HOME/miniconda3
```

## Installing Enviroment

The enviroment files are available under conda_env folder. Enviroment setup can be done with the one of the below actions:

```
conda create --name ySNX --file=environment.yaml
```

## Conf File

Note the below conf file needs to be appended under config as conf.yaml, being the api keys of infura and etherscan

```
---
infura:    'XXXXXXXXXXXXXXXXXXXXXXX'
etherscan: 'XXXXXXXXXXXXXXXXXXXXXXX'
```

## Running the model

To run the model for the period spanning between 01-may-2021 and 31-may-2021 simply run the following:

```
python main.py -d 01-may-2021 31-may-2021
```

The output will be saved under the output folder.
