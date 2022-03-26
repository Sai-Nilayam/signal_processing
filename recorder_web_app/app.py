from flask import Flask, render_template, request
import json
import librosa
import numpy as np
import soundfile as sf
import os

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/test')
def test():
	return render_template('test.html')

# For system_1.
@app.route('/system_1/get_unique_words', methods=['POST'])
def get_unique_words():
	voice = request.form.get("voice")
	all_texts = request.form.get("all_texts")

	# Now we have the voice and the all_texts.
	# Now here we need to do the processigs.

	# First we are going to clean the data i.e to remove all the punctuations 
	# and convert all the characters to lowercase.
	symbol_list = [
	    '`', '~', '!', '@', '$', '%', '^', '&', '*', '(', ')', '-', '=',
	    '[', '{', ']', '}', ';', ':', "'", '"', ',', '<', '>', '.', '/', '?', 
	    '\\', '|', '\n'
	]

	for symbol in symbol_list:
		all_texts = all_texts.replace(symbol, ' ')

	all_texts = all_texts.lower()

	# Now that we have all the cleaned texts, now we need to find all the
	# unique words.
	all_words = all_texts.split(' ')
	unique_words = set(all_words)
	unique_words_list = list(unique_words)
	
	# Now we need to save it to a text file in the form of a list but in text 
	# form so that we could execute these all when needed. 
	unique_words_str = ''
	for word in unique_words_list:
		unique_words_str = unique_words_str + ' ' + word.strip()
	unique_words_str = unique_words_str.strip()

	f = open('static/system_1/{}/inst_unique_words.txt'.format(voice), 'w')
	f.write(unique_words_str)
	f.close()

	# Now we need to prepare set of data that is needed to be returned.
	unique_word_count = len(unique_words_list)
	
	if unique_word_count%8 == 0:
		no_of_takes = unique_word_count // 8 - 1
	else:
		no_of_takes = (unique_word_count//8)

	estimated_recording_time = no_of_takes * 0.5

	# Preparing the json object
	response = {
		'unique_word_count': str(unique_word_count),
		'no_of_takes': str(no_of_takes),
		'estimated_recording_time': str(estimated_recording_time)
	}

	response_json = json.dumps(response)

	return response_json

# Now it's time to create an url to get take words. 
@app.route('/system_1/get_take_words', methods=['POST'])
def get_take_words():
	voice = request.form.get('voice')
	take_no = request.form.get('take_no')

	range_a = int(take_no) * 8 
	range_b = range_a + 8

	# Now we need to get all the unique words from the unique_words.txt file and
	# make a list out of that.
	f = open('static/system_1/{}/inst_unique_words.txt'.format(voice), 'r')
	content = f.read()
	f.close()

	unique_words_list = content.split(' ')

	take_words_list = unique_words_list[range_a : range_b]

	take_words_str = ' '.join(take_words_list)

	# Preparing the json object
	response = {
		'take_words': take_words_str
	}

	response_json = json.dumps(response)

	print(response_json)

	return response_json

# Here is the url to process the audio clip comming from the front end split it
# into word chunks and return all the audio chunks.
@app.route('/system_1/process_audio', methods=['POST'])
def process_audio():
	voice = request.form.get('voice')
	words = request.form.get('words')
	crop_amp_threshold = request.form.get('crop_amp_threshold')
	audio = request.files['audio']
	
	# Now that we have all the data we require now it's time to process the 
	# audio file, split it into 8 different words. If the split array count is
	# 8 then there will be further steps done. Else, Just return a response 
	# the Response that the audio processing failed. If success then returns
	# would be 8 audio chunk files and all the chunks would be previously saved 
	# in within inst folder of system_1.

	# First take the audio file and save it to the inst_words folder.
	audio.save('static/system_1/{}/audio_take_inst.mp3'.format(voice))

	# Now the next thing is that we would be importing that back to python 
	# environment and spit it using the librosa codes.
	ar, sr = librosa.load('static/system_1/{}/audio_take_inst.mp3'.format(voice))

	# Now it's time to split it.
	intervals = librosa.effects.split(ar, top_db=int(crop_amp_threshold))
				
	# As we need to have access to the take words.
	take_words_arr = words.split(' ')

	# Send failed message if the no of cropped words are not queals to 8.
	if len(intervals) != len(take_words_arr):
		# For internal testing.
		print(intervals)

		# We need to return a json here.
		# Preparing the json object
		response = {
			'processing_status': 'failed'
		}

		response_json = json.dumps(response)

		return response_json

	# Now that we have intervals we need to crop the audio files and save them
	# in the inst_word folder.

	for i in range(len(intervals)):
	    inst_interval = intervals[i]
	    inst_audio = ar[inst_interval[0] : inst_interval[1]]
	    inst_file_name = take_words_arr[i]
	    # Only use this when you are saving audio clips.
	    sf.write('static/system_1/{}/inst_words/{}.wav'.format(voice, i), inst_audio, sr, 'PCM_24')

	# Now what are the things we need to return. 
	# All we need to return a success message.
	# Preparing the json object
	response = {
		'processing_status': 'success'
	}

	response_json = json.dumps(response)

	return response_json

# Now we need to write a function to grab all the word clips from the inst_words
# folder and save them to the words folder with all the proper names. Wav format
# is okay to be used as in our case the wav files are very small as result of 
# being converted from the mp3 files by changing extensions.
@app.route('/system_1/done', methods=['POST'])
def done():
	voice = request.form.get('voice')
	words = request.form.get('words')

	# Now here the first thing is to get all the files from the inst_words 
	# folder.
	files = os.listdir('static/system_1/{}/inst_words'.format(voice))
	files.sort()

	# Create the words array
	words_arr = words.split(' ')

	for i in range(len(files)):
		inst_file_name = files[i]
		ar, sr = librosa.load('static/system_1/{}/inst_words/{}'.format(voice, inst_file_name))

		# Getting the real file name from the word arr.
		real_file_name = words_arr[i]
		sf.write('static/system_1/{}/words/{}.wav'.format(voice, real_file_name), ar, sr, 'PCM_24')

		# Removing the file from the inst_words folder.
		os.remove('static/system_1/{}/inst_words/{}'.format(voice, inst_file_name))

	return 'done'

# Now we need to create a funciton for Testing the TTS 1.
@app.route('/system_1/testing_play', methods=['POST'])
def testing_play():
	testing_voice = request.form.get('testing_voice')
	testing_words = request.form.get('testing_words')

	print(testing_voice)
	print(testing_words)

	# Now the first thing is to spllit all the words and put them all in an
	# array.
	testing_words_arr = testing_words.split(' ')
	print(testing_words_arr)

	# Now that we have all the words now what we need to do is that, we need to 
	# put all the words together and create a audio clip by taking the 
	# respective audio files from the words folder. 

	# Instantiating the final voice array. 
	final_voice = np.array([])

	# Trying for building up the final output voice. If a few words are not 
	# found then return a failed message.
	try:
		for word in testing_words_arr:
			# Getting the audio clip i.e the audio array from the words folder.
			inst_file_name = word + '.wav'
			inst_ar, inst_sr = librosa.load('static/system_1/{}/words/{}'.format(testing_voice, inst_file_name))
			final_voice = np.concatenate([final_voice, inst_ar])
	except:
		response = {
			'processing_status': 'failed'
		}

		response_json = json.dumps(response)

		return response_json

	# Finally saving the final voice as a wav file in testing_words folder.
	sf.write('static/system_1/{}/testing_words/{}'.format(testing_voice, 'final_output.wav'), final_voice, inst_sr, 'PCM_24')

	# Now what are the things we need to return. 
	# All we need to return a success message.
	# Preparing the json object
	response = {
		'processing_status': 'success'
	}

	response_json = json.dumps(response)

	return response_json



if __name__ == '__main__':
	# app.run(debug=True, port=8000)
	app.run(debug=True, host='0.0.0.0')