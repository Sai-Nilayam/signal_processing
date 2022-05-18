# For testing.
# print('test')

# Importing the mapping dict and executing it, so that it could be used anytime.
# Getting all the text codes from the python file.
f = open('static/system_5/dict.py', 'r')
text_code = f.read()
exec(text_code)
f.close()

# ----------------------------------------------------------------
# Caching all the Words
# Demo dict
# word_dict = {
# 	'test': {
# 		'this': [],
# 	},
# 	'test_2': {
# 		'this': [],
# 	}
# }

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

# Creating Word dicts.
word_dict = {}
folders = os.listdir('static/system_1/')
folders.remove('base_structure')

for folder in folders:
	word_dict[folder] = {}

for key in word_dict:
	files = os.listdir('static/system_1/{}/words/'.format(key))
	for file in files:
		ar, sr = librosa.load('static/system_1/{}/words/{}'.format(key, file), sr=48000)
		word_dict[key][file] = ar

# With this the Word dict is ready.
# print(word_dict)
# print(len(word_dict['test']))
# print(word_dict['test']['this.wav'])

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
	# use_word_concatenation = request.form.get('use_word_concatenation')
	# use_dict = request.form.get('use_dict')
	voice = request.form.get('voice')
	vv_set = request.form.get('vv_set')
	gap_between_words = request.form.get('gap_between_words')

	print(key, words, voice, vv_set, gap_between_words)

	# Test the key first.
	if key != 'test_key':
		return 'You have entered a wrong API key.'

	# Making the gap between words arr ready.
	gap_between_words = float(gap_between_words)
	gap_ar = np.array([0 for i in range(int(48000*gap_between_words))])

	# A few things to use the formatter script.
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

	# Now we need to split the words by ' ' space.
	words_ar = words.split(' ')

	# Creating an empty numpy array.
	final_speech = np.array([])

	print(list(word_dict[voice].keys()))

	for word in words_ar:
		if word+'.wav' in list(word_dict[voice].keys()):
			# Getting the word from Word Concatenation system.
			inst_word_ar = word_dict[voice][word+'.wav']
			final_speech = np.concatenate([final_speech, inst_word_ar])
			final_speech = np.concatenate([final_speech, gap_ar])
		else: 
			if word in list(map_dict.keys()):
				word = map_dict[word]
			
			# Now using the Vocal Tone and Style Transfer module to make the work.
			formatted_ar = formatter(word, vv_1, vv_2, vv_3)

			for character in formatted_ar:
				# check if it's SV or VV.
				if character in all_sv_sounds:
					# inst_ar, inst_sr = librosa.load('static/system_3/{}/sv/{}.wav'.format(voice, inst_character), sr=48000)
					# Accessing the chached array insted.
					inst_character_ar = sv_dict[voice][character + '.wav']
					final_speech = np.concatenate([final_speech, inst_character_ar])
				else:
					# inst_ar, inst_sr = librosa.load('static/system_2_a/{}/vv/{}.wav'.format(vv_set, inst_character), sr=48000)
					# Accessing the chached array insted.
					inst_character_ar = vv_dict[vv_set][character + '.wav']
					final_speech = np.concatenate([final_speech, inst_character_ar])

			# Putting the gap at the end of the word. 
			final_speech = np.concatenate([final_speech, gap_ar])

	# Saving the words_np_arr in wav form.
	# Creating the time attached name.
	file_name = 'final_speech' + '_' + str(datetime.datetime.now()) + '.wav'
	# Saving the final pronuciation.
	sf.write('static/system_5/wavs/{}'.format(file_name), final_speech, 48000, 'PCM_24')

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