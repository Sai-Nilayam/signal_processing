# For testing.
# print('test')

# Different things needed to be cached during the TTS processing.
# 1. The Mapping Dict.
# 2. All the Swaravarna sounds and Vyanjana Varna sounds of all voices and vv_sets. 

# Caching the Mapping dict.
# Importing the mapping dict and executing it, so that it could be used anytime.
# Getting all the text codes from the python file.
f = open('static/system_5/dict.py', 'r')
text_code = f.read()
exec(text_code)
f.close()

# ----------------------------------------------------------------
# Caching all the Swaravarna and Vyanjanavarna sounds.
# Demo dicts.
# sv_dict = {
# 	'test': {
# 		'a_s': [],
# 	},
# 	'test_2': {
# 		'a_s': [],
# 	}
# }

# vv_dict = {
# 	'test': {
# 		'k_s': [],
# 	},
# 	'test_2': {
# 		'k_s': [],
# 	}
# }

# Creating Swaravarna dicts.
sv_dict = {}
# Puttig the main keys.
# Listing out all the folders in 'system_3/'
folders = os.listdir('static/system_3/')
# Removing the base_structure folder.
folders.remove('base_structure')

for folder in folders:
	sv_dict[folder] = {}

# Now for each key (folder) in sv_dict we need to add all the swaravarna sounds in it.
for key in sv_dict:
	# Now importing all the the swaravarna sounds as np arr from that folder and save them inside that 2nd level dict as another dict.
	# Importing all the file names inside the folder. 
	files = os.listdir('static/system_3/{}/sv/'.format(key))
	for file in files:
		ar, sr = librosa.load('static/system_3/{}/sv/{}'.format(key, file), sr=48000)
		sv_dict[key][file] = ar

# With this the Swaravarna dict is ready.
# print(sv_dict)
# print(len(sv_dict['test']))
# print(sv_dict['test']['a_s.wav'])

# Creating Vyanjanavarna dicts.
vv_dict = {}
# Puttig the main keys.
# Listing out all the folders in 'system_3/'
folders = os.listdir('static/system_2_a/')
# Removing the base_structure folder.
folders.remove('base_structure')

for folder in folders:
	vv_dict[folder] = {}

# Now for each key (folder) in sv_dict we need to add all the swaravarna sounds in it.
for key in vv_dict:
	# Now importing all the the swaravarna sounds as np arr from that folder and save them inside that 2nd level dict as another dict.
	# Importing all the file names inside the folder. 
	files = os.listdir('static/system_2_a/{}/vv/'.format(key))
	for file in files:
		ar, sr = librosa.load('static/system_2_a/{}/vv/{}'.format(key, file), sr=48000)
		vv_dict[key][file] = ar

# With this the Vyanjanavarna dict is ready.
# print(vv_dict)
# print(len(vv_dict['test']))
# print(vv_dict['test']['r_s.wav'])

# ----------------------------------------------------------------

# Now we are going to write the public TTS APIs here.
@app.route('/system_5/tts', methods=['POST'])
def system_5_tts():
	tik = time.time()

	key = request.form.get('key')
	words = request.form.get('words')
	vv_set = request.form.get('vv_set')
	voice = request.form.get('voice')
	gap_between_words = request.form.get('gap_between_words')

	print(words, voice, gap_between_words)

	if key != 'test_key':
		return 'You have entered a wrong API key.'

	# Now we need to split the words by ' ' space.
	words_arr = words.split(' ')
	# Converting each words to it's dict form.
	words_dict_arr = []

	for word in words_arr:
		inst_dict_word = word_dict[word]
		words_dict_arr.append(inst_dict_word)

	print(words_dict_arr)

	# ----------------------------------------------------------------
	# Now it's time to create the np word arr
	words_np_arr = np.array([])
	
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

	all_sv_sounds = [
		'a_s', 'a_m', 'a_e', 'aa_s', 'aa_m', 'aa_e', 'i_s', 'i_m', 'i_e',
		'u_s', 'u_m', 'u_e', 'e_s', 'e_m', 'e_e', 'o_s', 'o_m', 'o_e'
	]

	for word in words_dict_arr:
		final_pronunciation = np.array([])

		formatted_ar = formatter(word, vv_1, vv_2, vv_3)

		# Create the sound array of the word
		for i in range(len(formatted_ar)):
			inst_character = formatted_ar[i]

			# check if it's SV or VV.
			if inst_character in all_sv_sounds:
				# inst_ar, inst_sr = librosa.load('static/system_3/{}/sv/{}.wav'.format(voice, inst_character), sr=48000)
				# Accessing the chached array insted.
				inst_ar = sv_dict[voice][inst_character + '.wav']
				final_pronunciation = np.concatenate([final_pronunciation, inst_ar])
			else:
				# inst_ar, inst_sr = librosa.load('static/system_2_a/{}/vv/{}.wav'.format(vv_set, inst_character), sr=48000)
				inst_ar = vv_dict[vv_set][inst_character + '.wav']
				final_pronunciation = np.concatenate([final_pronunciation, inst_ar])

		gap_between_words = float(gap_between_words)
		gap_arr = [0 for i in range(int(48000*gap_between_words))]
		words_np_arr = np.concatenate([words_np_arr, final_pronunciation, gap_arr])

	# Saving the words_np_arr in wav form.
	# Creating the time attached name.
	file_name = 'testing_characters' + '_' + str(datetime.datetime.now()) + '.wav'
	# Saving the final pronuciation.
	sf.write('static/system_5/wavs/{}'.format(file_name), words_np_arr, 48000, 'PCM_24')

	tok = time.time()

	time_taken = tok - tik

	# Now we need to return the path to the voie clip as well as the time taken for the process in seconds.
	file_url = '/static/system_5/wavs/{}'.format(file_name)
	time_taken = str(time_taken)

	response = {
		'file_url': file_url,
		'time_taken': time_taken
	}

	response_json = json.dumps(response)

	return response_json