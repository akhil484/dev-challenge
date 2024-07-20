from urllib.request import urlopen
import json
import base64
import requests
import time
from struct import *



morse_code_dict = {
    '.-': 'A',
    '-...': 'B',
    '-.-.': 'C',
    '-..': 'D',
    '.': 'E',
    '..-.': 'F',
    '--.': 'G',
    '....': 'H',
    '..': 'I',
    '.---': 'J',
    '-.-': 'K',
    '.-..': 'L',
    '--': 'M',
    '-.': 'N',
    '---': 'O',
    '.--.': 'P',
    '--.-': 'Q',
    '.-.': 'R',
    '...': 'S',
    '-': 'T',
    '..-': 'U',
    '...-': 'V',
    '.--': 'W',
    '-..-': 'X',
    '-.--': 'Y',
    '--..': 'Z',
    '-----': '0',
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9'
    }

def gt(code):
	
	i=0
	j=len(code)
	
	decrypted_code = ''
	while i<len(code):
		if code[i:j] in morse_code_dict:
			
			decrypted_code = decrypted_code + morse_code_dict[code[i:j]]
			i=j
			j=len(code)
		else:
			
			j=j-1

	return decrypted_code


def get_code(code_list):
	code_string = ''
	for i in code_list:
		code_string=code_string+i
	length = len(code_string)
	three_arrow = -1
	for i in range(length-1,-1,-1):
		if(code_string[i]!='.' and code_string[i]!='-'):
			three_arrow = i
			break
	
	num = gt(code_string[0:three_arrow-2])
	num_int = 0
	
	
	str1 = gt(code_string[three_arrow+1:length])
	return int(num), str1



def hit_endpoint():
	
	#Get the data from URL

	cookies = {
	    'connect.sid': '<browser_cookie>'
	}
	response = requests.get('https://exam.ankush.wiki/assignments', cookies=cookies)

	print(response.text)

	response = response.json()
	parts_number = response['numParts']
	#chain = {}
	chain = ['a']*parts_number
	chaincode = ''
	nums = []
	for p in range(1,parts_number+1):
		url = 'https://exam.ankush.wiki/data?part=%s'%(p)
		response = requests.get(url, cookies=cookies)
		print(response.json())
		num, str1 = get_code(response.json()['data'])
		chain[num-1] = str1
		nums.append(num)
		time.sleep(2.5)
	
	
	chaincode = ''.join(chain)

	response= requests.post('https://exam.ankush.wiki/answers', json={'chaincode':chaincode}, cookies=cookies)
	print(response.status_code)
	print(response.text)


if __name__ == '__main__':
    hit_endpoint()
