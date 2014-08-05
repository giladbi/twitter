import numpy as np

if __name__ == "__main__":
	company = 'jpmorgan'

	if company == 'jpmorgan': 
		files_to_process = ['jpmorgan.txt']
		output_file = './../output/' + 'jpmorgan_daily.txt'
	elif company == 'microsoft':
		files_to_process = ['microsoft1.txt','microsoft2.txt']
		output_file = './../output/' + 'microsoft_daily.txt'
	elif company == 'mcdonalds':
		files_to_process = ['mcdonalds1.txt','mcdonalds2.txt','mcdonalds3.txt']
		output_file = './../output/' + 'mcdonalds_daily.txt'


	data = {} # Hashmap: Key = date, value = sentiment vector
	days = ['Mon Jan 13','Tue Jan 14','Wed Jan 15','Thu Jan 16','Fri Jan 17','Mon Jan 20','Tue Jan 21','Wed Jan 22','Thu Jan 23','Fri Jan 24','Mon Jan 27','Tue Jan 28','Wed Jan 29','Thu Jan 30','Fri Jan 31','Mon Feb 03','Tue Feb 04','Wed Feb 05', 'Thu Feb 06', 'Fri Feb 07','Mon Feb 10','Tue Feb 11','Wed Feb 12','Thu Feb 13','Fri Feb 14','Mon Feb 17','Tue Feb 18','Wed Feb 19','Thu Feb 20','Fri Feb 21','Mon Feb 24','Tue Feb 25','Wed Feb 26','Thu Feb 27','Fri Feb 28', 'Mon Mar 03']
	all_days = ['Mon Jan 13','Tue Jan 14','Wed Jan 15','Thu Jan 16','Fri Jan 17','Sat Jan 18','Sun Jan 19','Mon Jan 20','Tue Jan 21','Wed Jan 22','Thu Jan 23','Fri Jan 24','Sat Jan 25','Sun Jan 26','Mon Jan 27','Tue Jan 28','Wed Jan 29','Thu Jan 30','Fri Jan 31','Sat Feb 01','Sun Feb 02','Mon Feb 03','Tue Feb 04','Wed Feb 05', 'Thu Feb 06', 'Fri Feb 07','Sat Feb 08','Sun Feb 09','Mon Feb 10','Tue Feb 11','Wed Feb 12','Thu Feb 13','Fri Feb 14','Sat Feb 15','Sun Feb 16','Mon Feb 17','Tue Feb 18','Wed Feb 19','Thu Feb 20','Fri Feb 21','Sat Feb 22','Sun Feb 23','Mon Feb 24','Tue Feb 25','Wed Feb 26','Thu Feb 27','Fri Feb 28','Sat Mar 01','Sun Mar 02','Mon Mar 03']
	
	open(output_file,"w").close() # Clear any existing file
	output_file = open(output_file,'a') # Reopen it in append mode

	for dataset in files_to_process:
		input_file = './../output/' + dataset
		
		with open(input_file, 'r') as f:
			for line in f.readlines():
				line = line.split('\t')
				time = line[0]
				time = time[:10]

				if time[:3] == 'Sat':
					index = all_days.index(time)
					time = all_days[index-1]
				elif time[:3] == 'Sun':
					index = all_days.index(time)
					time = all_days[index-2]

				if time in data:
					senftiment_vector = data.get(time)
				else:
					print time
					sentiment_vector = [0.0]*5

				emotiscore = sentiment_vector[0] + float(line[2])
				hashscore = sentiment_vector[1] + float(line[3])
				swnscore = sentiment_vector[2] + float(line[4])
				totalscore = sentiment_vector[3] + float(line[5])
				volume = sentiment_vector[4] + 1

				sentiment_vector = [emotiscore, hashscore, swnscore, totalscore, volume]
				data[time] = sentiment_vector

	output_file.write('Time\tDay\tEmotiscore\tHashscore\tSwnscore\tTotalscore\tVolume\n')
	for day in days:
		specific_day = day[:3]

		# if company == 'jpmorgan': 
		# 	stock_data = stocks.jpmorgan.get(day)
		# elif company == 'microsoft':
		# 	stock_data = stocks.microsoft.get(day)
		# elif company == 'mcdonalds':
		# 	stock_data = stocks.mcdonalds.get(day)

		if day not in data:
			output_file.write(day + '\t' + specific_day + '\t0\t0\t0\t0\t0\n')
			# output_file.write(str(stock_data[0]) + '\t' + str(stock_data[1]) + '\n')
		else:
			vector = data.get(day)
			# vector.extend(stock_data)
			output_file.write(day + '\t' + specific_day + '\t')
			count = 0
			for value in vector:
				count += 1
				output_file.write(str(value))
				if count != 5:
					output_file.write('\t')
			if day != 'Mon March 03':
				output_file.write('\n')
	output_file.close()