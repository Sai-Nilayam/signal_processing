def formatter(name):
	# Let's do a different approach.
	vv_1 = ['k', 'g', 'j', 't', 'd', 'n', 'p', 'b', 'm', 'y', 'r', 'l', 'w', 's', 'h']
	vv_2 = ['kh', 'gh', 'ch', 'jh', 'th', 'dh', 'ph', 'bh', 'sh']
	vv_3 = ['chh', ] 

	name_list = list(name)
	print(name_list)

	vvs = []

	skip_indices = []

	for i in range(len(name_list)):
		if i in skip_indices:
			continue

		try:
			inst_1_char = name_list[i]
			inst_2_char = name_list[i+1]
			inst_3_char = name_list[i+2]

			if inst_1_char+inst_2_char+inst_3_char in vv_3:
				vvs.append(inst_1_char+inst_2_char+inst_3_char)
				vvs.append(i)
				skip_indices.append(i+1)
				skip_indices.append(i+2)
			elif inst_1_char+inst_2_char in vv_2:
				vvs.append(inst_1_char+inst_2_char)
				vvs.append(i)
				skip_indices.append(i+1)
			elif inst_1_char in vv_1:
				vvs.append(inst_1_char)
				vvs.append(i)
		except:
			try:
				inst_1_char = name_list[i]
				inst_2_char = name_list[i+1]

				if inst_1_char+inst_2_char in vv_2:
					vvs.append(inst_1_char+inst_2_char)
					vvs.append(i)
					skip_indices.append(i+1)
				elif inst_1_char in vv_1:
					vvs.append(inst_1_char)
					vvs.append(i)
			except:
				inst_1_char = name_list[i]
				if inst_1_char in vv_1:
					vvs.append(inst_1_char)
					vvs.append(i)

	print(vvs)

	# Using the same technique to findout all the swaravarna sounds.
	sv_2 = ['aa']
	sv_1 = ['a', 'i', 'u', 'e', 'o']

	svs = []

	skip_indices = []

	for i in range(len(name_list)):
		if i in skip_indices:
			continue

		try:
			inst_1_char = name_list[i]
			inst_2_char = name_list[i+1]

			if inst_1_char+inst_2_char in sv_2:
				svs.append(inst_1_char+inst_2_char)
				svs.append(i)
				skip_indices.append(i+1)
			elif inst_1_char in sv_1:
				svs.append(inst_1_char)
				svs.append(i)
		except:
			inst_1_char = name_list[i]
			if inst_1_char in sv_1:
				svs.append(inst_1_char)
				svs.append(i)

	print(svs)

	# combining both the arrays with proper indexing.
	combined_arr = []

	for ele in vvs:
		combined_arr.append(ele)

	for ele in svs:
		combined_arr.append(ele)

	print(combined_arr)

	acc_dict = {}
	sorting_arr = []

	# Creating the paired arries.
	for i in range(0, len(combined_arr), 2):
		# inst_ar = [combined_arr[i+1], combined_arr[i]]
		# acc_ar.append(inst_ar)
		acc_dict[combined_arr[i+1]] = combined_arr[i]
		sorting_arr.append(combined_arr[i+1])


	print(acc_dict)

	sorting_arr.sort()
	print(sorting_arr)

	formatted_ar = []
	# Sorting the values.
	for ele in sorting_arr:
		formatted_ar.append(acc_dict[ele])

	print(formatted_ar)

	# Now once we have this formatted array. Now the job is to write the funciton for detecting the starting end vv and 
	# starting middle and ending sv.

	# First doing that for VV.
	for i in range(len(formatted_ar)):
		inst_v = formatted_ar[i]
		# Before that check if it's a VV.
		if inst_v in vvs:
			# If i is the last index then v_e.
			if i == len(formatted_ar)-1:
				formatted_ar[i] = formatted_ar[i] + '_e'
				continue

			# If the next Varna is a VV then put it v_e.
			try:
				inst_2_v = formatted_ar[i+1]
				if inst_2_v in vvs:
					formatted_ar[i] = formatted_ar[i] + '_e'
					continue
			except:
				pass

			formatted_ar[i] = formatted_ar[i] + '_s'

	print(formatted_ar)

	# So far the funciton of Name entinty pronunctiation is over.

	first_sv = True

	# Now it's time to put _s _m and _e sounds on Swaravarnas.
	for i in range(len(formatted_ar)):
		inst_s = formatted_ar[i]

		# Check if it's a SV.
		if inst_s in svs:
			# Check if it's first sv then make is '_s'.
			if first_sv == True:
				formatted_ar[i] = formatted_ar[i] + '_s'
				first_sv = False
				continue

			if i == len(formatted_ar)-1:
				formatted_ar[i] = formatted_ar[i] + '_m'
				continue

			if i == len(formatted_ar)-2:
				formatted_ar[i] = formatted_ar[i] + '_e'
				continue

			formatted_ar[i] = formatted_ar[i] + '_m'

	print(formatted_ar)

	# Finally returning the formatted ar.
	return formatted_ar

if __name__ == '__main__':
	name = 'ankush'
	formatted_ar = formatter(name)
	print('\n', name)
	print(formatted_ar)
