import json
import time

def find_emoticons(text):
	return ''

def find_hashtags(text):
	return ''

def find_brand(text):
	lower_tweet = text.lower()
	brand = ''

	if 'jpmorgan' in lower_tweet:
		brand = 'jpmorgan'
	elif 'microsoft' in lower_tweet:
		brand = 'microsoft'
	elif 'mcdonalds' in lower_tweet or 'mcdonald\'s' in lower_tweet or 'mcdonald' in lower_tweet:
		brand = 'mcdonalds'
	return brand

def process_tweet(text,f1,f2,f3,f4):
	try:
		raw_json = json.loads(text)
		delimiter = '\t'

		tweet_text = str(raw_json['text'].encode('utf-8'))
		tweet_text = tweet_text.replace('\n',' ')
		tweet_text = tweet_text.replace('\t',' ')
		brand = find_brand(tweet_text)

		#if brand == 'microsoft' or brand == 'jpmorgan' or brand == 'mcdonalds' or brand == '':
		time = str(raw_json['created_at'])
		followers = str(raw_json['user']['followers_count'])
		hashtags = find_hashtags(tweet_text)
		emoticons = find_emoticons(tweet_text)

		output = time + delimiter + tweet_text + delimiter + followers + '\n'

		if brand == 'microsoft': # Print to microsoft file
			f1.write(output)
		elif brand == 'jpmorgan': # Print to jpmorgan file
			f2.write(output)
		elif brand == 'mcdonalds': # Print to mcdonalds file
			f3.write(output)
		elif brand == '':
			f4.write(output)
	except:
		print 'Bad tweet'

if __name__ == '__main__':
	file_name = 'data/exampletweets_3.txt'
	breakpoint = '}{"created_at":'
	start = 0
	end = 0
	counter = 0

	input_file = open(file_name, 'r')
	microsoft_output = open("microsoft_output.txt", "a")
	jpmorgan_output = open("jpmorgan_output.txt", "a")
	mcdonalds_output = open("mcdonalds_output.txt", "a")
	everything_else_output = open("other_output.txt", "a")

	start_time = time.time()
	byte = input_file.read(1)
	current_string = byte
	while byte != "":
		byte = input_file.read(500)
		current_string = current_string + byte

		if current_string.count(breakpoint) == 1:
			start = current_string.rfind(breakpoint) + 1
		elif current_string.count(breakpoint) == 2:
			end = current_string.rfind(breakpoint) + 1

		if end > start:
			full_tweet = current_string[start:end]
			process_tweet(full_tweet,microsoft_output,jpmorgan_output,mcdonalds_output,everything_else_output)
			current_string = current_string[end:]
			start = end
			end = 0
			counter += 1
			if (counter % 10000 == 0):
				elapsed_time = time.time() - start_time
				print 'Number of tweets parsed ' + str(counter) + ' (' + str(elapsed_time) + ' seconds)'
