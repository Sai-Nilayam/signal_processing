# For testing.
# print('test')

import requests
import json

localhost_name = 'http://127.0.0.1:5000'
remotehost_name = 'https://dev.simpragma.com'

host_name = localhost_name

# ----------------------------------------------------------------
# Getting the path to the generated wav file from the words. 
url = host_name + '/system_5/tts'

data = {
    # The API Key.
    'key': 'test_key',
    # The sentence to be converted from Text to Speech.
    'words': 'ankush this call may be recorded for quality and training purpose',
    # Vyanjana Varna Set.
    'vv_set': 'test',
    # The Tone and Style in which we need the Speech to be in. 
    'voice': 'test',
    # Gap between each words, to make the voice clip sound faster or slower. 
    'gap_between_words': '0.1'
}

response = requests.post(url, data=data)

# print(response)
print(response.text)

# Creating the dict form the response text.
response_dict = json.loads(response.text)
# Retriving the data.
file_url = response_dict['file_url']
time_taken = response_dict['time_taken']

print(file_url)
print(time_taken)
# print(response.content)

# ----------------------------------------------------------------
# Getting the file itself by making a get request to the url.
# We need to add the server name or the ip adress of the server at the beginning of the file_url.
url = host_name + file_url

response = requests.get(url)

# print(response)
# print(response.text)

# Saving the returned file in Local Mahcine.
f = open('returned_wav_file.{}'.format('wav'), 'wb')
f.write(response.content)
f.close()

print('File saved in the folder with name returned_wav_file.wav.')