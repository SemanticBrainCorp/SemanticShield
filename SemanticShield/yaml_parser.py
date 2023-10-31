import yaml
from yaml.resolver import Resolver

# remove yaml resolver entries for On/Off
for ch in "Oo":
    if len(Resolver.yaml_implicit_resolvers[ch]) == 1:
        del Resolver.yaml_implicit_resolvers[ch]
    else:
        Resolver.yaml_implicit_resolvers[ch] = [x for x in
                Resolver.yaml_implicit_resolvers[ch] if x[0] != 'tag:yaml.org,2002:bool']

def yaml_parser(string: str) -> dict:
    obj = yaml.safe_load(string)
    return obj

def yaml_file_parser(file_path: str) -> dict:
    with open(file_path, "r") as f:
        obj = yaml.safe_load(f)
    return obj
