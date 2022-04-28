from flask import Flask, render_template, request
import json
import librosa
import numpy as np
import soundfile as sf
import os
import shutil
import datetime
import traceback
import audio2numpy as a2n
from pydub import AudioSegment
import getpass
import sys
import magic
import time
# import tensorflow as tf
from formatter import formatter

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
	
	if unique_word_count%4 == 0:
		no_of_takes = unique_word_count // 4 - 1
	else:
		no_of_takes = (unique_word_count//4)

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

	range_a = int(take_no) * 4 
	range_b = range_a + 4

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
	# The first step here is to remove the log.txt file and recreate it again with proper permissions.
	inst_file_name = 'log.txt'
	inst_url = 'static/{}'.format(inst_file_name)
	os.remove(inst_url)
	f = open(inst_url, 'w')
	f.close()
	# log
	f = open('static/log.txt', 'a'); f.write('\nlog.txt deleted and recreated for latest log write. \n'); f.close()

	# log
	f = open('static/log.txt', 'a'); f.write('user {} is running the python script. \n'.format(getpass.getuser())); f.close()
	f = open('static/log.txt', 'a'); f.write('python version: {}, python exe path: {}, librosa version: {} \n'.format(sys.version, sys.executable, librosa.__version__)); f.close()
	f = open('static/log.txt', 'a'); f.write('all paths: {} \n'.format(sys.path)); f.close()

	f = open('static/log.txt', 'a'); f.write('process_audio function logic started. \n'); f.close()

	voice = request.form.get('voice')
	words = request.form.get('words')
	crop_amp_threshold = request.form.get('crop_amp_threshold')
	analysis_time_gap = request.form.get('analysis_time_gap')
	audio = request.files['audio']
	# log
	f = open('static/log.txt', 'a'); f.write('data received at server. \n'); f.close()

	# Now that we have all the data we require now it's time to process the 
	# audio file, split it into 8 different words. If the split array count is
	# 8 then there will be further steps done. Else, Just return a response 
	# the Response that the audio processing failed. If success then returns
	# would be 8 audio chunk files and all the chunks would be previously saved 
	# in within inst folder of system_1.

	# First take the audio file and save it to the inst_words folder.
	audio.save('static/system_1/{}/audio_take_inst.wav'.format(voice))
	os.chmod('static/system_1/{}/audio_take_inst.wav'.format(voice), 0o777)
	# log
	f = open('static/log.txt', 'a'); f.write('audio_take_inst.wav saved with 777 permisson. \n'); f.close()

	# Finding the file type of the file audio_take_inst.wav.
	file_type = magic.from_file('static/system_1/{}/audio_take_inst.wav'.format(voice), mime=True)
	# log
	f = open('static/log.txt', 'a'); f.write('audio_take_inst.wav file format: {}. \n'.format(file_type)); f.close()

	# Now the next thing is that we would be importing that back to python 
	# environment and spit it using the librosa codes.
	try:
		# Using Librosa to load the mp3 file.
		ar, sr = librosa.load('static/system_1/{}/audio_take_inst.wav'.format(voice), sr=None)
		# Using a2n to load the mp3 file.
		# ar, sr = a2n.audio_from_file('static/system_1/{}/audio_take_inst.mp3'.format(voice))
		# Using pydub to load the mp3 file.
		# wav_file = AudioSegment.from_file('static/system_1/{}/audio_take_inst.wav'.format(voice))
		# ar = wav_file.get_array_of_samples()
		# ar = np.array(ar, dtype=float)
		# print(ar.shape)
		# print(ar)
		# log
		f = open('static/log.txt', 'a'); f.write('audio_take_inst imported to python env. \n'); f.close()
	except:
		f = open('static/log.txt', 'a'); traceback.print_exc(file=f); f.close()

	# Now it's time to split it.
	intervals = librosa.effects.split(ar, top_db=int(crop_amp_threshold), frame_length=int(int(analysis_time_gap)*0.001*int(sr)))
	# log
	f = open('static/log.txt', 'a'); f.write('audio splitting process done. \n'); f.close()
				
	# As we need to have access to the take words.
	take_words_arr = words.split(' ')
	# log
	f = open('static/log.txt', 'a'); f.write('words splitted into array. \n'); f.close()

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
		# log
		f = open('static/log.txt', 'a'); f.write('failed response sent from server. \n'); f.close()

		return response_json

	# Before saving the new final_output we need to delete the previous one.
	# Here for simplicity we are going to delete the entire folder and save the new file in 
	# proper direcotry structure.
	# Removing the folder testing_words and recreate it.
	inst_folder_name = 'inst_words'
	inst_url = 'static/system_1/{}/{}'.format(voice, inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)

	# log
	f = open('static/log.txt', 'a'); f.write('inst word folder deleted entirely and recreated with 777 permisson. \n'); f.close()

	# Now that we have intervals we need to crop the audio files and save them
	# in the inst_word folder.
	for i in range(len(intervals)):
	    inst_interval = intervals[i]
	    inst_audio = ar[inst_interval[0] : inst_interval[1]]
	    inst_file_name = take_words_arr[i]
	    # Only use this when you are saving audio clips.
	    sf.write('static/system_1/{}/inst_words/{}_{}.wav'.format(voice, i, str(datetime.datetime.now())) , inst_audio, sr, 'PCM_24')
	# log
	f = open('static/log.txt', 'a'); f.write('all cropped clips save in inst_words folder. \n'); f.close()

	# Now what are the things we need to return. 
	# All we need to return a success message.
	# Preparing the json object
	response = {
		'processing_status': 'success'
	}

	response_json = json.dumps(response)
	# log
	f = open('static/log.txt', 'a'); f.write('success response sent from server. \n'); f.close()

	return response_json

# Here will be the clip url sending endpoint.
@app.route('/system_1/send_clip_url', methods=['POST'])
def send_clip_url():
	voice = request.form.get('voice')
	clip_no = request.form.get('clip_no')

	# Listing all the files in inst_words folder.
	files = os.listdir('static/system_1/{}/inst_words/'.format(voice))
	files.sort()

	# # Failed Response (not available) if the clip number is greater than the number of files present in the inst_word folder.
	if not (int(clip_no) < (len(files))):
		# Preparing the json object
		response = {
			'file_url': 'not_available',
		}

		response_json = json.dumps(response)

		return response_json

	# Making up the clip url.
	clip_url = '/static/system_1/{}/inst_words/{}'.format(voice, str(files[int(clip_no)]))
	print(clip_no)

	# Preparing the json object
	response = {
		'file_url': clip_url,
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
		ar, sr = librosa.load('static/system_1/{}/inst_words/{}'.format(voice, inst_file_name), sr=None)

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
			inst_ar, inst_sr = librosa.load('static/system_1/{}/words/{}'.format(testing_voice, inst_file_name), sr=None)
			final_voice = np.concatenate([final_voice, inst_ar])
	except:
		response = {
			'processing_status': 'failed'
		}

		response_json = json.dumps(response)

		return response_json

	# Before saving the new final_output we need to delete the previous one.
	# Here for simplicity we are going to delete the entire folder and save the new file in 
	# proper direcotry structure.
	# Removing the folder testing_words and recreate it.
	inst_folder_name = 'testing_words'
	inst_url = 'static/system_1/{}/{}'.format(testing_voice, inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)

	# Finally saving the final voice as a wav file in testing_words folder.
	final_output_name = 'final_output' + '_' + str(datetime.datetime.now()) + '.wav'
	sf.write('static/system_1/{}/testing_words/{}'.format(testing_voice, final_output_name), final_voice, inst_sr, 'PCM_24')

	# Now what are the things we need to return. 
	# All we need to return a success message.
	# Preparing the json object
	response = {
		'processing_status': 'success',
	}

	response_json = json.dumps(response)

	return response_json

@app.route('/system_1/get_final_output_url', methods=['POST'])
def get_final_output():
	testing_voice = request.form.get('testing_voice')

	# List all the files in the testing_words folder.
	files = os.listdir('static/system_1/{}/testing_words'.format(testing_voice))
	clip_url = '/static/system_1/{}/testing_words/'.format(testing_voice) + str(files[0])

	# Preparing the json object
	response = {
		'file_url': clip_url,
	}

	response_json = json.dumps(response)

	return response_json

# Now here we are writing a function for resetting the backend i.e to delete all
# the data in the backend due to app use. This include clearing the 
# inst_unique_words.txt, unique_words.txt, audio_take_inst.mp3, inst_words 
# folder and words folder. This function does not require any information from 
# the frontend.
@app.route('/system_1/reset_backend', methods=['POST'])
def reset_backend():
	voices_list = ['voice_0_0', 'voice_0_1', 'voice_1_0', 'voice_1_1']

	for voice in voices_list:
		print(voice)

		# Removing the inst_unique_words.txt file.
		inst_file_name = 'inst_unique_words.txt'
		inst_url = 'static/system_1/{}/{}'.format(voice, inst_file_name)
		os.remove(inst_url)
		f = open(inst_url, 'w')
		f.close()

		# Removing unique_words.txt
		inst_file_name = 'unique_words.txt'
		inst_url = 'static/system_1/{}/{}'.format(voice, inst_file_name)
		os.remove(inst_url)
		f = open(inst_url, 'w')
		f.close()


		# Removing audio_take_inst.wav and recreate it.
		inst_file_name = 'audio_take_inst.wav'
		inst_url = 'static/system_1/{}/{}'.format(voice, inst_file_name)
		os.remove(inst_url)
		f = open(inst_url, 'w')
		f.close()

		# Removing audio_take_inst.mp3 and recreate it.
		inst_file_name = 'audio_take_inst.mp3'
		inst_url = 'static/system_1/{}/{}'.format(voice, inst_file_name)
		os.remove(inst_url)
		f = open(inst_url, 'w')
		f.close()

		# Removing the folder inst_words and recreate it here there.
		inst_folder_name = 'inst_words'
		inst_url = 'static/system_1/{}/{}'.format(voice, inst_folder_name)
		shutil.rmtree(inst_url)
		os.mkdir(inst_url)
		os.chmod(inst_url, 0o777)

		# Removing the folder words and recreate it.
		inst_folder_name = 'words'
		inst_url = 'static/system_1/{}/{}'.format(voice, inst_folder_name)
		shutil.rmtree(inst_url)
		os.mkdir(inst_url)
		os.chmod(inst_url, 0o777)

		# Removing the folder testing_words and recreate it.
		inst_folder_name = 'testing_words'
		inst_url = 'static/system_1/{}/{}'.format(voice, inst_folder_name)
		shutil.rmtree(inst_url)
		os.mkdir(inst_url)
		os.chmod(inst_url, 0o777)

	# Sending a success message to the frontend as json.
	response = {
		'processing_status': 'success'
	}

	response_json = json.dumps(response)

	return response_json

# From here we would be working on writing backend APIs for the system 2 i.e Name Entinty pronunciation.
@app.route('/system_2/process_audio', methods=['POST'])
def system_2_process_audio():
	# Now here we need to write all the backend logics.
	characters = request.form.get('characters')
	crop_amp_threshold = request.form.get('crop_amp_threshold')
	analysis_time_gap = request.form.get('analysis_time_gap')
	fine_analysis_time_gap = request.form.get('fine_analysis_time_gap')
	audio = request.files['audio']

	# Now the next thing to do is to save the file at the right location.
	audio.save('static/system_2/audio_take_inst.wav')	

	# Importing the audio file to the Python's env.
	ar, sr = librosa.load('static/system_2/audio_take_inst.wav', sr=None)
	print(sr)

	# Detecting the first_index.
	ar_inst, sr_inst = librosa.load('static/system_2/audio_take_inst.wav', sr=None, duration=8.0)
	intervals_inst = librosa.effects.split(ar_inst, top_db=int(crop_amp_threshold), frame_length=int(int(analysis_time_gap)*0.001*int(sr_inst)))
	first_index = intervals_inst[0][0] - (0.2*sr_inst)

	start_index =  int(first_index)
	end_index = int(intervals_inst[0][1] + (0.2*sr_inst))
	chunk_gap = end_index - start_index

	# Gap to jump for next character chunk.
	metronome_gap = 2 * sr_inst

	# Now it's time to process the main audio and save all the small character sounds in inst_character sound folder.
	# Preparing the character chunk array.
	character_chunks = [
		'k_s', 'k_e', 'kh_s', 'kh_e', 'g_s', 'g_e', 'gh_s', 'gh_e',
		'ch_s', 'ch_e', 'chh_s', 'chh_e', 'j_s', 'j_e', 'jh_s', 'jh_e',
		't_s', 't_e', 'th_s', 'th_e', 'd_s', 'd_e', 'dh_s', 'dh_e', 'n_s', 'n_e',
		'p_s', 'p_e', 'ph_s', 'ph_e', 'b_s', 'b_e', 'bh_s', 'bh_e', 'm_s', 'm_e',
		'y_s', 'y_e', 'r_s', 'r_e', 'l_s', 'l_e', 'w_s', 'w_e', 'sh_s', 'sh_e', 's_s', 's_e', 'h_s', 'h_e'
	]

	# Now splitting the main array but as per the metronome.
	length = len(character_chunks) // 2
	print(length)

	for i in range(length):
		start_index_inst = start_index + (i*metronome_gap)
		end_index_inst = start_index_inst + chunk_gap

		audio_chunk_inst = ar[start_index_inst : end_index_inst]
		
		intervals_inst = librosa.effects.split(audio_chunk_inst, top_db=int(crop_amp_threshold), frame_length=int(int(fine_analysis_time_gap)*0.001*int(sr)))
		inst_stripped_chunk = audio_chunk_inst[intervals_inst[0][0]:intervals_inst[0][1]]
		
		# For writing the inst_stripped_chunk.
		sf.write('static/system_2/inst_character_chunks/{}.wav'.format(character_chunks[2*i].split('_')[0]), inst_stripped_chunk, int(sr*1.0), 'PCM_24')

		# Splitting the stripped audio chunk from middle. Here we are finding the midpoint.
		inst_mid_point = len(inst_stripped_chunk) // 2

		# Creating and saving the starting sound.
		starting_sound = inst_stripped_chunk[ : inst_mid_point]
		sf.write('static/system_2/inst_character_sounds/{}.wav'.format(character_chunks[2*i]), starting_sound, int(sr*1.0), 'PCM_24')

		# Creating and saving the ending sound.
		ending_sound = inst_stripped_chunk[inst_mid_point : ]
		sf.write('static/system_2/inst_character_sounds/{}.wav'.format(character_chunks[(2*i) + 1]), ending_sound, int(sr*1.0), 'PCM_24')

	# Now we need to return the concatinated Vyanjana Varnsa sounds with Swaravarnas to show if everything has done properly or not.
	# Creating the chunks.
	swaravarna_sounds = ['a', 'aa', 'i', 'u', 'e', 'o']

	# Creating the clip.
	final_clip = np.array([])

	for i in range(length):
		inst_s = character_chunks[2*i]
		inst_e = character_chunks[(2*i) + 1]

		for j in range(len(swaravarna_sounds)):
			inst_swaravarna = swaravarna_sounds[j]
			# Now creating the sound clip chunk.
			inst_s_ar, inst_sr = librosa.load('static/system_2/inst_character_sounds/{}.wav'.format(inst_s), sr=None)
			final_clip = np.concatenate([final_clip, inst_s_ar])
			inst_sv_ar, inst_sr = librosa.load('static/system_2/swaravarna_sounds/{}.wav'.format(inst_swaravarna), sr=None)
			final_clip = np.concatenate([final_clip, inst_sv_ar])
			inst_e_ar, inst_sr = librosa.load('static/system_2/inst_character_sounds/{}.wav'.format(inst_e), sr=None)
			# final_clip = np.concatenate([final_clip, inst_e_ar])
			# Then we need to add half second gap some gap.
			final_clip = np.concatenate([final_clip, [0 for i in range(sr//2)]])

	# Now we need to save the final clip audio in the backend with some data time attached to it. 
	final_output_name = 'final_clip' + '_' + str(datetime.datetime.now()) + '.wav'
	sf.write('static/system_2/final_clip/{}'.format(final_output_name), final_clip, sr, 'PCM_24')

	file_url = '/static/system_2/final_clip/{}'.format(final_output_name)

	response = {
		'processing_status': 'success',
		'clip_url': file_url
	}

	response_json = json.dumps(response)

	return response_json

@app.route('/system_2/done', methods=['POST'])
def system_2_done():
	files = os.listdir('static/system_2/inst_character_sounds/')

	for file in files:
		shutil.move('static/system_2/inst_character_sounds/{}'.format(file), 'static/system_2/character_sounds/{}'.format(file))

	return 'done';

@app.route('/system_2/reset_backend', methods=['POST'])
def system_2_reset_backend():
	# Removing the audio_take_inst.wav file.
	inst_file_name = 'audio_take_inst.wav'
	inst_url = 'static/system_2/{}'.format(inst_file_name)
	os.remove(inst_url)
	f = open(inst_url, 'w')
	f.close()

	# Removing the folder character_sounds and recreate it here there.
	inst_folder_name = 'character_sounds'
	inst_url = 'static/system_2/{}'.format(inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)

	# Removing the folder final_clip and recreate it here there.
	inst_folder_name = 'final_clip'
	inst_url = 'static/system_2/{}'.format(inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)

	# Removing the folder inst_character_chunks and recreate it here there.
	inst_folder_name = 'inst_character_chunks'
	inst_url = 'static/system_2/{}'.format(inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)

	# Removing the folder inst_character_sounds and recreate it here there.
	inst_folder_name = 'character_sounds'
	inst_url = 'static/system_2/{}'.format(inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)
	
	# Sending a success message to the frontend as json.
	response = {
		'processing_status': 'success'
	}

	response_json = json.dumps(response)

	return response_json

# So here we will be writing the functions for systme 2 alternate module.
@app.route('/system_2_a/process_audio', methods=['POST'])
def system_2_a_process_audio():
	vv_set = request.form.get('vv_set')
	vv_notation = request.form.get('vv_notation')
	vv_s_audio = request.files['vv_s_audio']
	vv_e_audio = request.files['vv_e_audio']

	# Creating a url and saving both the files in the inst folder and creating a clip with other sounds for testing. 
	# Saving the starting sound.
	url_s = 'static/system_2_a/{}/inst_vv/{}_s.wav'.format(vv_set, vv_notation)
	vv_s_audio.save(url_s)

	url_e = 'static/system_2_a/{}/inst_vv/{}_e.wav'.format(vv_set, vv_notation)
	vv_e_audio.save(url_e)

	# Now we need to add some testing thing. Here are the testing words below -
	# kankak kaankak kinkik kunkuk kenkek konkok

	sv_list = ['a.wav', 'aa.wav', 'i.wav', 'u.wav', 'e.wav', 'o.wav']

	test_clip = np.array([])

	for sv in sv_list:
		inst_vv_s_ar, sr = librosa.load(url_s, sr=48000)
		inst_vv_e_ar, sr = librosa.load(url_e, sr=48000)
		inst_sv_ar, sr = librosa.load('static/system_2_a/{}/test_chunks/{}'.format(vv_set, sv), sr=48000)
		inst_n_e_ar, sr = librosa.load('static/system_2_a/{}/test_chunks/{}'.format(vv_set, 'n_e.wav'), sr=48000)
		inst_t_s_ar, sr = librosa.load('static/system_2_a/{}/test_chunks/{}'.format(vv_set, 't_s.wav'), sr=48000) 
		gap_ar = [0 for i in range(48000)]
		# Creating the final test clip.
		test_clip = np.concatenate([test_clip, inst_vv_s_ar, inst_sv_ar, inst_n_e_ar, inst_vv_s_ar, inst_sv_ar, inst_vv_e_ar, inst_t_s_ar, inst_sv_ar, inst_vv_e_ar, gap_ar])

	# Before writing anything we need to delete the folder and recreate it. 
	# Removing the folder inst_character_sounds and recreate it here there.
	inst_folder_name = 'inst_test_clip'
	inst_url = 'static/system_2_a/{}/{}'.format(vv_set, inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)

	test_clip_name = 'test_clip' + '_' + str(datetime.datetime.now()) + '.wav'
	sf.write('static/system_2_a/{}/inst_test_clip/{}'.format(vv_set, test_clip_name), test_clip, 48000, 'PCM_24')

	file_url = '/static/system_2_a/{}/inst_test_clip/{}'.format(vv_set, test_clip_name)
	# Sending a success message to the frontend as json.
	response = {
		'processing_status': 'success',
		'file_url': file_url
	}

	response_json = json.dumps(response)

	return response_json

@app.route('/system_2_a/done', methods=['POST'])
def system_2_a_done():
	vv_set = request.form.get('vv_set')

	files = os.listdir('static/system_2_a/{}/inst_vv/'.format(vv_set))

	for file in files:
		shutil.move('static/system_2_a/{}/inst_vv/{}'.format(vv_set, file), 'static/system_2_a/{}/vv/{}'.format(vv_set, file))

	return 'done'

@app.route('/system_2_a/testing_play', methods=['POST'])
def system_2_a_testing_play():
	vv_set = request.form.get('vv_set')
	characters = request.form.get('characters')

	print(vv_set, characters)

	# Formatting the characters to pronunciable format. 
	formatted_ar = formatter(characters)
	print('\n' + characters)
	print(formatted_ar)

	all_sv_sounds = [
		'a_s', 'a_m', 'a_e', 'aa_s', 'aa_m', 'aa_e', 'i_s', 'i_m', 'i_e',
		'u_s', 'u_m', 'u_e', 'e_s', 'e_m', 'e_e', 'o_s', 'o_m', 'o_e'
	]

	final_pronunciation = np.array([])

	# Now we need to concatenate the character sounds
	# But here we will try this and say failed if something goes wrong. 
	try:
		for i in range(len(formatted_ar)):
			inst_character = formatted_ar[i]

			# check if it's SV or VV.
			if inst_character in all_sv_sounds:
				if inst_character[0:2] == 'aa':
					inst_character = 'aa';
				else:
					inst_character = inst_character[0]

				inst_ar, inst_sr = librosa.load('static/system_2_a/{}/test_chunks/{}.wav'.format(vv_set, inst_character), sr=48000)
				final_pronunciation = np.concatenate([final_pronunciation, inst_ar])
			else:
				inst_ar, inst_sr = librosa.load('static/system_2_a/{}/vv/{}.wav'.format(vv_set, inst_character), sr=48000)
				final_pronunciation = np.concatenate([final_pronunciation, inst_ar])
	except:
		response = {
			'processing_status': 'failed',
		}

		response_json = json.dumps(response)

		return response_json

	# Now before putting the test characters in the folder we need to delete it and recreate it. 
	# Removing the folder testing_words and recreate it.
	inst_folder_name = 'testing_characters'
	inst_url = 'static/system_2_a/{}/{}'.format(vv_set, inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)

	# Creating the time attached name.
	file_name = 'testing_characters' + '_' + str(datetime.datetime.now()) + '.wav'
	# Saving the final pronuciation.
	sf.write('static/system_2_a/{}/testing_characters/{}'.format(vv_set, file_name), final_pronunciation, 48000, 'PCM_24')

	file_url = '/static/system_2_a/{}/testing_characters/{}'.format(vv_set, file_name)

	response = {
		'processing_status': 'success',
		'file_url': file_url,
	}

	response_json = json.dumps(response)

	return response_json

# From here we will start writing functions for System 3.
@app.route('/system_3/process_audio', methods=['POST'])
def system_3_process_audio():
	# Now here we need to write all the backend logics.
	voice = request.form.get('voice')
	characters = request.form.get('characters')
	crop_amp_threshold = request.form.get('crop_amp_threshold')
	analysis_time_gap = request.form.get('analysis_time_gap')
	fine_analysis_time_gap = request.form.get('fine_analysis_time_gap')
	audio = request.files['audio']

	# Now the next thing to do is to save the file at the right location.
	audio.save('static/system_3/{}/audio_take_inst.wav'.format(voice))	

	# Importing the audio file to the Python's env.
	ar, sr = librosa.load('static/system_3/{}/audio_take_inst.wav'.format(voice), sr=None)
	print(sr)

	# Now it's time to split the audio.
	intervals = librosa.effects.split(ar, top_db=int(crop_amp_threshold), frame_length=int(int(analysis_time_gap)*0.001*int(sr)))

	if len(intervals) != 3:
		response = {
		'processing_status': 'failed'
		}

		response_json = json.dumps(response)

		return response_json

	# Now before doing anykind of saving we need to delete that folder and recreate it again. 
	# Removing the folder testing_words and recreate it.
	inst_folder_name = 'inst_sv'
	inst_url = 'static/system_3/{}/{}'.format(voice, inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)
	
	# First take the characters and find for what character.
	for i in range(3):
		inst_character_sound = ar[intervals[i][0] : intervals[i][1]]

		# Applying fine cropping.
		inst_intervals = librosa.effects.split(inst_character_sound, top_db=int(crop_amp_threshold), frame_length=int(int(fine_analysis_time_gap)*0.001*int(sr)))
		inst_character_sound = inst_character_sound[inst_intervals[0][0] : inst_intervals[0][1]]

		inst_name = str(i) + '_' + str(datetime.datetime.now()) + '.wav'
		sf.write('static/system_3/{}/inst_sv/{}'.format(voice, inst_name), inst_character_sound, sr, 'PCM_24')

	# Sending a success message to the frontend as json. We could also send an failed message from here.
	# But that is not required from here.
	response = {
		'processing_status': 'success'
	}

	response_json = json.dumps(response)

	return response_json

# Here will be the clip url sending endpoint.
@app.route('/system_3/send_clip_url', methods=['POST'])
def system_3_send_clip_url():
	voice = request.form.get('voice')
	clip_no = request.form.get('clip_no')

	# Listing all the files in inst_words folder.
	files = os.listdir('static/system_3/{}/inst_sv/'.format(voice))
	files.sort()

	# # Failed Response (not available) if the clip number is greater than the number of files present in the inst_word folder.
	if not (int(clip_no) < (len(files))):
		# Preparing the json object
		response = {
			'file_url': 'not_available',
		}

		response_json = json.dumps(response)

		return response_json

	# Making up the clip url.
	clip_url = '/static/system_3/{}/inst_sv/{}'.format(voice, str(files[int(clip_no)]))
	print(clip_no)

	# Preparing the json object
	response = {
		'file_url': clip_url,
	}

	response_json = json.dumps(response)

	return response_json

@app.route('/system_3/done', methods=['POST'])
def system_3_done():
	voice = request.form.get('voice')
	characters = request.form.get('characters')

	if characters[0:2] == 'aa':
		character = 'aa'
	else:
		character = characters[0]
		
	suffix_list = ['_s', '_m', '_e']

	files = os.listdir('static/system_3/{}/inst_sv/'.format(voice))
	files.sort()

	for i in range(len(files)):
		ar, sr = librosa.load('static/system_3/{}/inst_sv/{}'.format(voice, files[i]), sr=None)
		inst_name = character + suffix_list[i] + '.wav'
		sf.write('static/system_3/{}/sv/{}'.format(voice, inst_name), ar, sr, 'PCM_24')

	# Removing the folder testing_words and recreate it.
	inst_folder_name = 'inst_sv'
	inst_url = 'static/system_3/{}/{}'.format(voice, inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)

	return 'done'

@app.route('/system_3/testing_play', methods=['POST'])
def system_3_testing_play():
	vv_set = request.form.get('vv_set')
	voice = request.form.get('testing_voice')
	characters = request.form.get('testing_characters')

	# Formatting the characters to pronunciable format. 
	formatted_ar = formatter(characters)
	print('\n' + characters)
	print(formatted_ar)

	all_sv_sounds = [
		'a_s', 'a_m', 'a_e', 'aa_s', 'aa_m', 'aa_e', 'i_s', 'i_m', 'i_e',
		'u_s', 'u_m', 'u_e', 'e_s', 'e_m', 'e_e', 'o_s', 'o_m', 'o_e'
	]

	final_pronunciation = np.array([])

	# Now we need to concatenate the character sounds
	# But here we will try this and say failed if something goes wrong. 
	try:
		for i in range(len(formatted_ar)):
			inst_character = formatted_ar[i]

			# check if it's SV or VV.
			if inst_character in all_sv_sounds:
				inst_ar, inst_sr = librosa.load('static/system_3/{}/sv/{}.wav'.format(voice, inst_character), sr=48000)
				final_pronunciation = np.concatenate([final_pronunciation, inst_ar])
			else:
				inst_ar, inst_sr = librosa.load('static/system_2_a/{}/vv/{}.wav'.format(vv_set, inst_character), sr=48000)
				print('test')
				final_pronunciation = np.concatenate([final_pronunciation, inst_ar])
	except:
		response = {
			'processing_status': 'failed',
		}

		response_json = json.dumps(response)

		return response_json

	# Now before putting the test characters in the folder we need to delete it and recreate it. 
	# Removing the folder testing_words and recreate it.
	inst_folder_name = 'testing_characters'
	inst_url = 'static/system_3/{}/{}'.format(voice, inst_folder_name)
	shutil.rmtree(inst_url)
	os.mkdir(inst_url)
	os.chmod(inst_url, 0o777)

	# Creating the time attached name.
	file_name = 'testing_characters' + '_' + str(datetime.datetime.now()) + '.wav'
	# Saving the final pronuciation.
	sf.write('static/system_3/{}/testing_characters/{}'.format(voice, file_name), final_pronunciation, inst_sr, 'PCM_24')

	response = {
		'processing_status': 'success',
	}

	response_json = json.dumps(response)

	return response_json

@app.route('/system_3/get_final_output_url', methods=['POST'])
def system_3_get_final_output():
	print('test')
	testing_voice = request.form.get('testing_voice')

	# List all the files in the testing_words folder.
	files = os.listdir('static/system_3/{}/testing_characters'.format(testing_voice))
	clip_url = '/static/system_3/{}/testing_characters/'.format(testing_voice) + str(files[0])

	# Preparing the json object
	response = {
		'file_url': clip_url,
	}

	response_json = json.dumps(response)

	return response_json

@app.route('/system_3/reset_backend', methods=['POST'])
def system_3_reset_backend():
	voices_list = ['voice_0_0', 'voice_0_1', 'voice_1_0', 'voice_1_1']

	for voice in voices_list:
		# Removing the audio_take_inst.wav file.
		inst_file_name = 'audio_take_inst.wav'
		inst_url = 'static/system_3/{}/{}'.format(voice, inst_file_name)
		os.remove(inst_url)
		f = open(inst_url, 'w')
		f.close()

		# Removing the folder character_sounds and recreate it here there.
		inst_folder_name = 'inst_sv'
		inst_url = 'static/system_3/{}/{}'.format(voice, inst_folder_name)
		shutil.rmtree(inst_url)
		os.mkdir(inst_url)
		os.chmod(inst_url, 0o777)

		# Removing the folder final_clip and recreate it here there.
		inst_folder_name = 'sv'
		inst_url = 'static/system_3/{}/{}'.format(voice, inst_folder_name)
		shutil.rmtree(inst_url)
		os.mkdir(inst_url)
		os.chmod(inst_url, 0o777)

		# Removing the folder inst_character_chunks and recreate it here there.
		inst_folder_name = 'testing_characters'
		inst_url = 'static/system_3/{}/{}'.format(voice, inst_folder_name)
		shutil.rmtree(inst_url)
		os.mkdir(inst_url)
		os.chmod(inst_url, 0o777)

	# Sending a success message to the frontend as json.
	response = {
		'processing_status': 'success'
	}

	response_json = json.dumps(response)

	return response_json

if __name__ == '__main__':
	# app.run(debug=True, port=8000)
	app.run(debug=True, host='0.0.0.0')
	# app.run(debug=True, host='127.0.0.1')