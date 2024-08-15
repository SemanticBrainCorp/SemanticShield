import math
from pprint import pprint
import re

BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
HEX_CHARS = "1234567890abcdefABCDEF"
threshold = 20
b64_minimum = 4.5
hex_minimum = 3.0
recurse = False
filename = None
verbose = False


ENTROPY_PATTERNS_TO_FLAG = [
	# AWS access keys (which often have secret keys listed with them)
	re.compile('AKIA'),
	# URLs with username/password combos
	re.compile('^[a-z]+://.*:.*@'),
	# PEM encoded PKCS8 private keys
	re.compile('BEGIN.*PRIVATE KEY'),
	# Slack webhook
	re.compile(r'https://hooks.slack.com/services/T\w{8}/B\w{8}/\w{24}')
]

PATTERNS_TO_IGNORE = [
]

ENTROPY_PATTERNS_TO_DISCOUNT = [
	# public key
	#re.compile(r'/BEGIN.*PUBLIC KEY/'),
	re.compile(r"-----BEGIN(.{1,5})PUBLIC KEY-----(.*?)-----END(.{1,5})PUBLIC KEY-----", re.MULTILINE | re.DOTALL),
	# secrets don't contain domain names
	# Example: example.org
	re.compile(r'^([a-z0-9\-]+\.)+(com|net|me|org|edu)$'),
	# secrets don't have host names
	# Example: my-cool-hostname
	re.compile(r'^[a-z]*(-[a-z]*)*$'),
	# secrets don't look like python imports
	# Example import a.b.Hello_World1
	re.compile(r'^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+$'),
	# secrets don't look like python variable names
	# Example: my_fun_variable_name1
	re.compile(r'^_?_?[a-zA-Z0-9]+(_[a-zA-Z0-9]+)+$'),
	# secrets don't have absolute paths
	# Example /a/b/1-B_z.txt
	re.compile(r'^/[a-zA-Z0-9\-_/\.]+$'),
	# secrets don't have relative paths
	# Example a/b/1-B_z.txt
	re.compile(r'^[a-zA-Z0-9\-_/\.]+/$'),
	# secrets don't have flask routes
	# Example: /v1/<path:path> or /v1/user/<id>/group
	re.compile(r'<([a-z_]+:[a-z_]+|[a-z_]+)>/'),
	re.compile(r'/<([a-z_]+:[a-z_]+|[a-z_]+)>'),
	# secrets don't look like urls with args
	# Example: /a/b/c?hello=world&test=me
	re.compile(r'/[a-zA-Z\-_\.]+(/[a-zA-Z\-_\.])*\?[a-zA-Z\-_\.=&]$'),
	# secrets don't email addresses
	# Example: test+spam@example.com
	re.compile(r'[a-zA-Z0-9_\-\+]+@[a-zA-Z0-9\-]+\.(com|net|me|edu)'),
	# secrets don't look like constants
	# Example: EXAMPLE_CONSTANT
	re.compile(r'^[A-Z]*(_[A-Z]*)*$'),
	# secrets don't look like session dict keys
	# Example: XSRF-TOKEN
	re.compile(r'^[A-Z]*(-[A-Z]*)*$'),
	# secrets don't look like URIs
	# Example: https://example.org
	re.compile(r'^[a-z]+://'),
	# secrets don't look like format strings
	# Example: {10!s}
	# TODO: consider false negatives
	re.compile(r'\{\d{0,2}\}'),
	# Example: {my_Var}
	# TODO: consider false negatives
	re.compile(r'\{_?_?[a-zA-Z]{1,10}[a-zA-Z0-9_]{0,10}\}'),
	# secrets don't look like headers,
	# Example: X-Forwarded-For
	re.compile(r'^[A-Z][a-z]*(-[A-Z][a-z]*)*$'),
	# secrets don't look like date formats
	# Example: %Y%m%dT%H%M%SZ
	re.compile(r'^(%[a-zA-Z\-]+)+$'),
	# Example: 2012-10-17T00:00:00Z
	re.compile(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ'),
	# Example: 2021-08-22
	re.compile(r'\d\d\d\d-\d\d-\d\d'),
	# secrets don't look like phone numbers
	# Example: +15555555555
	re.compile(r'\d\d\d\d\d\d\d\d\d\d$'),
	# secrets don't look cli arguments
	# Example: --test_me-please
	re.compile(r'^--[a-zA-Z0-9\-_]$'),
	# key-lookups
	# Example: my_var:b:c
	re.compile(r'^[a-zA-Z0-9_\-]+(:[a-zA-Z0-9_\-])+$'),
]


def get_strings_of_set(word, char_set):
	""" 
	return all strings in word with length > threshold that contain only characters in char_set (from trufflehog)
	"""
	
	count = 0
	letters = ""
	strings = []
	for char in word:
		if char in char_set:
			letters += char
			count += 1
		else:
			if count > threshold:
				strings.append(letters)
			letters = ""
			count = 0
	if count > threshold:
		strings.append(letters)
	return strings

def shannon_entropy(data, iterator):
	"""
	return the shannon entropy value for a given string (borrowed from trufflehog)
	Borrowed from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
	"""
	if not data:
		return 0
	entropy = 0
	for x in iterator:
		p_x = float(data.count(x))/len(data)
		if p_x > 0:
			entropy += - p_x*math.log(p_x, 2)
	return entropy

def result_object(string, score, kind):
	return {
		'string': string,
		'score': score,
		'kind': kind
	}

def find_in_line(line):
	strings_found = []
	for word in line.split():
		base64_strings = get_strings_of_set(word, BASE64_CHARS)
		hex_strings = get_strings_of_set(word, HEX_CHARS)
		for string in base64_strings:
			b64_entropy = shannon_entropy(string, BASE64_CHARS)
			if b64_entropy > b64_minimum:
				strings_found.append(result_object(string, b64_entropy, 'b64'))
		for string in hex_strings:
			hex_entropy = shannon_entropy(string, HEX_CHARS)
			if hex_entropy > hex_minimum:
				strings_found.append(result_object(string, hex_entropy, 'hex'))
	return strings_found


def scan_for_patterns(string, pattern_list):
	matches = []
	for pattern in pattern_list:
		if pattern.search(string):
			matches.append(pattern.pattern)
	return matches

def filter_acceptable(full_text):
    for pattern in ENTROPY_PATTERNS_TO_DISCOUNT:
        full_text = pattern.sub( '', full_text)
    return full_text

def check_detail(full_text: str):
    cleaned_text = filter_acceptable(full_text)
    texts = cleaned_text.split('\n')
    scan = []
    result = []
    for text in texts:
        r1 = find_in_line(text)
        result.extend(r1)
        s1 = scan_for_patterns(text, ENTROPY_PATTERNS_TO_FLAG)
        scan.extend(s1)
    return result, scan

def check(full_text: str):
    result, scan = check_detail(full_text)
    if len(result) > 0 or len(scan) > 0:
        return True
    else:
        return False
	
if __name__ == "__main__":
    texts = [
        "03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has address 9.37.65.139, ifidx 1",
        "03/22 08:51:06 INFO   :...read_physical_netif: index #4, Somepwd123*!  interface CTCD0 Hs51+m32-J5h has address 9.67.116.98, ifidx 4",
        "03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has 1uX3@2^h1$hR address 9.37.65.139, VCNzdDEyMyFfQQ== ifidx 1",
        """deploy:
            user: aaronloo
            password:
                secure: thequickbrownfoxjumpsoverthelazydog
            on:
                repo: Yelp/detect-secrets
        """,
        """
            [some section]
            secrets_for_no_one_to_find =
                hunter2
                password123
                BEEF0123456789a
        """,
        """
            red_herring = 'DEADBEEF'
            id = 'YW1pYWx3YXlzZ2VuZXJhdGluZ3BheWxvYWRzd2hlbmltaHVuZ3J5b3JhbWlhbHdheXNodW5ncnk'

            base64_secret = 'c2VjcmV0IG1lc3NhZ2Ugc28geW91J2xsIG5ldmVyIGd1ZXNzIG15IHBhc3N3b3Jk'
            hex_secret = '8b1118b376c313ed420e5133ba91307817ed52c2'
            basic_auth = 'http://username:whywouldyouusehttpforpasswords@example.com'

            aws_access_key = 'AKIAIOSFODNN7EXAMPLE'
            aws_secret_access_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        """,
        "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        """-----BEGIN RSA PRIVATE KEY-----
    MIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu
    KUpRKfFLfRYC9AIKjbJTWit+CqvjWYzvQwECAwEAAQJAIJLixBy2qpFoS4DSmoEm
    o3qGy0t6z09AIJtH+5OeRV1be+N4cDYJKffGzDa88vQENZiRm0GRq6a+HPGQMd2k
    TQIhAKMSvzIBnni7ot/OSie2TmJLY4SwTQAevXysE2RbFDYdAiEBCUEaRQnMnbp7
    9mxDXDf6AU0cN/RPBjb9qSHDcWZHGzUCIG2Es59z8ugGrDY+pxLQnwfotadxd+Uy
    v/Ow5T0q5gIJAiEAyS4RaI9YG8EWx/2w0T67ZUVAw8eOMB6BIUg0Xcu+3okCIBOs
    /5OiPgoTdSy7bcF9IGpSE8ZgGKzgYQVZeN97YE00
    -----END RSA PRIVATE KEY-----""",
        'http://user:password@domain.com/',
        """-----BEGIN RSA PUBLIC KEY-----
    MEgCQQCo9+BpMRYQ/dL3DS2CyJxRF+j6ctbT3/Qp84+KeFhnii7NT7fELilKUSnx
    S30WAvQCCo2yU1orfgqr41mM70MBAgMBAAE=
    -----END RSA PUBLIC KEY-----""",
    ]


    full_text = ''
    for text in texts:
        full_text = full_text + text + '\n'
    full_text = 'http://user:password@domain.com/'
    result_list, scan = check_detail(full_text)
    result = check(full_text)
    if result:
        print('FAIL')
    else:
        print('SUCCESS')
    print('done')





