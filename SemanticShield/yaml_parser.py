import yaml
from yaml.resolver import Resolver

import pandas as pd

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

def yaml_role_to_df(file_path: str):
    print("Starting role based access")

    with open(file_path, "r") as f:
        obj = yaml.safe_load(f)
    
    role_config_df = pd.DataFrame(columns=['role', 'sys_content_file', 'min_len', 'max_len', 'lang_filter', 'fail_action'])
    num_roles = len(obj['role'])

    for i in range(num_roles):
        for role_key in obj['role'][i]:
            print(role_key)
            print(obj['role'][i][role_key])
            print()

            sys_content_file = 'sales.txt'
            min_len = 150
            max_len = 300
            lang_filter = True
            fail_action = 'retry'

            for role_config_item in obj['role'][i][role_key]:
                for role_config_key in role_config_item.keys():
                    print(role_config_key, role_config_item[role_config_key])

                    if role_config_key == 'system_content':
                        sys_content_file = role_config_item[role_config_key]
                    elif role_config_key == 'text_length':
                        for len_item in role_config_item[role_config_key]:
                            for len_item_key in len_item.keys():
                                if len_item_key == 'min_len':
                                    min_len = len_item[len_item_key]
                                elif len_item_key == 'max_len':
                                    max_len = len_item[len_item_key]
                    elif role_config_key == 'language_filter':
                        lang_filter == True
                    elif role_config_key == 'fail_action':
                        fail_action = 'retry'

            role_config_df.loc[i] = [role_key, sys_content_file, min_len, max_len, lang_filter, fail_action]

    print()
    print(role_config_df)
    print()

    return role_config_df
