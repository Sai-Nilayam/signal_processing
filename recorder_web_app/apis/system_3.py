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

	# Making up the Vyanjana Varna lists.
	vv_1 = []
	vv_2 = []
	vv_3 = []

	# Getting all the Vyanjana Varnas form the Vyanja Varna set folder.
	files = os.listdir('static/system_2_a/{}/vv/'.format(vv_set))
	for file in files:
		inst_vv = file.split('_')[0]
		if len(inst_vv) == 3:
			vv_3.append(inst_vv)
		elif len(inst_vv) == 2:
			vv_2.append(inst_vv)
		else:
			vv_1.append(inst_vv)

	# Formatting the characters to pronunciable format. 
	formatted_ar = formatter(characters, vv_1, vv_2, vv_3)
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