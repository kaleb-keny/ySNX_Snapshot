import yaml

def parse_config(path):
    with open(path, 'r') as stream:
        return  yaml.load(stream, Loader=yaml.FullLoader)

def hexToInt(x):
    return int(x, 16)

                