import swn_function as sf
import re
import time
import subprocess

company = 'microsoft'

if company == 'jpmorgan': 
	files_to_process = ['jpmorgan.txt']
elif company == 'microsoft':
	files_to_process = ['microsoft1.txt','microsoft2.txt']
elif company == 'mcdonalds':
	files_to_process = ['mcdonalds1.txt','mcdonalds2.txt','mcdonalds3.txt']

for dataset in files_to_process:
	input_file = './../data/' + dataset
	output_file = './../output/' + dataset
	p = subprocess.Popen(['wc', '-l', input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	result, err = p.communicate()
	n_tweets_to_parse = result.split(' ')[0]

	f_out = open(output_file, 'a')
	#f_out.write('Time\tFollowers\tEmotiscore\tHashscore\tSwnscore\tTotalscore\n')

	count = 0.0

	with open(input_file, 'r') as f:
		start = time.time()
		for line in f.readlines():
			count += 1
			line = line.split('\t')

			try:
				timestamp = line[0]
				tweet = line[1]
				followers = 0 

				try: 
					followers = int(re.sub('[^0-9]','',line[2]))
				except:
					pass

				[emotiscore, hashscore, swnscore, totalscore] = sf.calculate_sentiment(tweet,followers)
				f_out.write(timestamp + '\t' + str(followers) + '\t' + str(emotiscore) + '\t' + str(hashscore) + '\t' + str(swnscore) + '\t' + str(totalscore) + '\n')
				
				if (count % 500) == 0:
					elapsed = time.time() - start
					print 'Tweets: ' + str(count) + '/' + n_tweets_to_parse + ' (' + str(round(100*count/int(n_tweets_to_parse),2)) + '%) - Time taken: ' + str(round(elapsed,2))
			except:
				pass

	f_out.close()