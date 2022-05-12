@app.route('/system_2_a/process_audio', methods=['POST'])
def system_2_a_process_audio():
	vv_set = request.form.get('vv_set')
	vv_notation = request.form.get('vv_notation')
	vv_s_audio = request.files['vv_s_audio']
	vv_e_audio = request.files['vv_e_audio']

	# Checking if the folder exists. If not recreate it.
	folder_names = os.listdir('static/system_2_a/')
	if vv_set not in folder_names:
		shutil.copytree('static/system_2_a/base_structure', 'static/system_2_a/{}'.format(vv_set))

	# Creating a url and saving both the files in the inst folder and creating a clip with other sounds for testing. 
	# Saving the starting sound.
	url_s = 'static/system_2_a/{}/inst_vv/{}_s.wav'.format(vv_set, vv_notation)
	vv_s_audio.save(url_s)

	url_e = 'static/system_2_a/{}/inst_vv/{}_e.wav'.format(vv_set, vv_notation)
	vv_e_audio.save(url_e)

	# Now we need to add some testing thing. Here are the testing words below -
	# kankak kaankak kinkik kunkuk kenkek konkok

	sv_list = ['a.wav', 'a_f.wav', 'aa.wav', 'aa_f.wav', 'i.wav', 'i_f.wav', 'u.wav', 'u_f.wav', 'e.wav', 'e_f.wav', 'o.wav', 'o_f.wav']

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
