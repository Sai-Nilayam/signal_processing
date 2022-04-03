import requests

# End point to the TTS system_1.
# url = 'http://127.0.0.1:8000/tts_1/'

data = {
    'voice': 'assuring_male_voice_0_1'
    'phrase': 'd m i finance me ap ka swagat hai.',   
}

response = requests.post(url, data=data)

print(response)
print(response.byte)