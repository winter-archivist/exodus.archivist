import yaml


async def cacheRead(targetCache: str):
    with open(f'{targetCache}', 'r') as file:
        data = yaml.safe_load(file)
    return data


async def cacheWrite(targetCache: str, dataInput: dict):
    with open(f'{targetCache}', 'a' if dataInput else 'w') as file:
        yaml.dump(dataInput, file)


async def cacheClear(targetCache: str):
    with open(f'{targetCache}', 'w') as file:
        pass


async def cacheDataExist(targetCache: str, searchFor: str):
    with open(f'{targetCache}', 'r') as file:
        data = yaml.safe_load(file)
    if data is None:  # Checks if Data even Exists, this prevents error caused by checking for something in nothing
        return None
    elif searchFor in data:
        return True
    else:
        return False
