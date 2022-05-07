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