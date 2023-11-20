import base64
from functools import lru_cache
import json
import re
from typing import List, Optional

def gen_regex(config: dict) -> str:
    regex_parts = [
        f'(?=.*[A-Z]){{{config["num_uppercase"]},}}',  
        f'(?=.*[a-z]){{{config["num_lowercase"]},}}',  
        f'(?=.*\d){{{config["num_numerics"]},}}',      
        f'(?=.*[@$!%*?+\-&]){{{config["num_symbols"]},}}'
    ]
    regex = f"^{''.join(regex_parts)}.{{{config['min_length']},}}$"
    return regex

@lru_cache
def load_config(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            regex = gen_regex(config)
    except:
        with open(file_path, 'r') as file:
            regex = file.readline()
    return regex

def find_possible_passwords(string: str) -> List[str]:
    simple_pattern = r'\S{8,}'
    matches = re.findall(simple_pattern, string)
    
    return matches

def is_valid_password(password: str, regex: str) -> bool:
    return bool(re.match(regex, password))

def get_valid_passwords(password_list: List[str], regex: str) -> List[str]:
    valid_passwords = []
    for password in password_list:
        if is_valid_password(password, regex):
            valid_passwords.append(password)
    return valid_passwords

def find_base64_strings(test_str: str) -> List[str]:
    regex = r"(?![=])[\W\s]"
    matches = re.split(regex, test_str)
    matches = [m for m in matches if len(m) > 10 and (len(m) % 4) == 0]
    return matches

def valid_base64(word: str) -> Optional[str]:
    try:
        result = base64.b64decode(word, validate=True).decode('utf-8')
        return result
    except Exception as ex:
        return None
    
def filter_base64(text_list: List[str]):
    return list(filter(lambda x: x is not None, map(valid_base64, text_list)))

def get_line_passwords(line: str, regex: str) -> List[str]:
        possible_passwords = find_possible_passwords(line)
        base64s = find_base64_strings(line)
        decoded_base64s = filter_base64(base64s)
        possible_passwords.extend(decoded_base64s)
        possible_passwords = list(set(possible_passwords))
        
        valid_passwords = get_valid_passwords(possible_passwords, regex)
        return valid_passwords

def get_all_passwords(lines: str, regex: str) -> List[str]:
    all_valid_passwords = []    
    for index, line in enumerate(lines):
        valid_passwords = get_line_passwords(line, regex)
        for v in valid_passwords:
            all_valid_passwords.append({'line': index+1, 'match': v})
    return all_valid_passwords

def check_password(text: str, regex: str):
    passwords = get_line_passwords(text, regex)
    return passwords

def check_password_list(text: List[str], regex: str):

    passwords = get_all_passwords(text, regex)
    return passwords

if __name__=='__main__':
    regex = load_config('password_policy.json')

    print(check_password("03/22 08:51:06 INFO   :...read_physical_netif: index #4, Somepwd123*!  interface CTCD0 Hs51+m32-J5h has address 9.67.116.98, ifidx 4", regex))
    print(check_password("03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has address 9.37.65.139, ifidx 1", regex))
    print(check_password("03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has 1uX3@2^h1$hR address 9.37.65.139, VCNzdDEyMyFfQQ== ifidx 1", regex))
    print(check_password_list([
        "03/22 08:51:06 INFO   :...read_physical_netif: index #4, Somepwd123*!  interface CTCD0 Hs51+m32-J5h has address 9.67.116.98, ifidx 4",
        "03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has address 9.37.65.139, VCNzdDEyMyFfQQ== ifidx 1",
        "03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has 1uX3@2^h1$hR address 9.37.65.139, VCNzdDEyMyFfQQ== ifidx 1"
    ], regex))


