import model_stocks as stocks
import numpy as np

days = ['Mon Jan 13','Tue Jan 14','Wed Jan 15','Thu Jan 16','Fri Jan 17','Mon Jan 20','Tue Jan 21','Wed Jan 22','Thu Jan 23','Fri Jan 24','Mon Jan 27','Tue Jan 28','Wed Jan 29','Thu Jan 30','Fri Jan 31','Mon Feb 03','Tue Feb 04','Wed Feb 05', 'Thu Feb 06', 'Fri Feb 07','Mon Feb 10','Tue Feb 11','Wed Feb 12','Thu Feb 13','Fri Feb 14','Mon Feb 17','Tue Feb 18','Wed Feb 19','Thu Feb 20','Fri Feb 21','Mon Feb 24','Tue Feb 25','Wed Feb 26','Thu Feb 27','Fri Feb 28', 'Mon Mar 03', 'Tue Mar 04', 'Wed Mar 05', 'Thu Mar 06', 'Fri Mar 07']
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

# company: String = Name of the company
# raw_vector: 
# finance_datatype: Integer 2 = Stock price change, 1 = Percentage stock price change, 0 = Only direction
# finance_n: Integer >=0 Number of days of finance data to include
# sentiment_datatype: Boolean 1 = all sentiment featues, 0 = just end
# sentiment_n: Integer >=0 Number of days of sentiment data to include
# day: Boolean 1 = Include day of the week, 0 = do not
# target: Boolean 1 = Amount, 0 = Direction
# volume: boolean 1 = Yes, 0 = No
def create_feature_vector(company, raw_vector, finance_datatype, finance_n, sentiment_datatype, sentiment_n, day, target,volume):
		date = raw_vector[0]
		day_of_the_week = raw_vector[1]		

		if sentiment_n > 0:
			if sentiment_datatype == 1:
				feature_vector = raw_vector[2:len(raw_vector)-2]
			elif sentiment_datatype == 0:
				feature_vector = [raw_vector[len(raw_vector)-2]]
		else:
			feature_vector = []

		if volume == 1:
			feature_vector.append(raw_vector[len(raw_vector)-1])

		if company == 'jpmorgan': 
			stock_data = stocks.jpmorgan
		elif company == 'microsoft':
			stock_data = stocks.microsoft
		elif company == 'mcdonalds':
			stock_data = stocks.mcdonalds

		## Append day of the week
		if (day == 1):
			day_vector = [0.0]*len(weekdays)
			day_vector[weekdays.index(day_of_the_week)] = 1.0
			feature_vector.extend(day_vector)

		## Append financial data
		index_today = days.index(date)		
		if (finance_n > 0):			
			for i in range(0,finance_n):
				previous_stock = stock_data.get(days[index_today-i])
				if finance_datatype == 2: # Stock price change
					temp = previous_stock[1] - previous_stock[0]
					feature_vector.append(temp)
				elif finance_datatype == 1: # Percent stock change
					temp = 100*(previous_stock[1]/previous_stock[0])
					feature_vector.append(temp)
				elif finance_datatype == 0: # Direction
					temp = previous_stock[1] - previous_stock[0]
					if temp >= 0:						
						#feature_vector.append('up')
						feature_vector.append(1)
					else:
						#feature_vector.append('down')
						feature_vector.append(-1)

		## Append sentiments
		if (sentiment_n > 0):
			pass				

		# feature_vector.append(1)
		## Target		
		tomorrows_stock = stock_data.get(days[index_today+1])
		if target == 1: # Amount
			temp = 100*(tomorrows_stock[1]/tomorrows_stock[0])
		elif target == 0: # Direction
			temp = tomorrows_stock[1] - tomorrows_stock[0]
			if temp >= 0:						
				#temp = 'up'
				temp = 1.0
			else:
				#temp = 'down'
				temp = -1.0
		feature_vector.append(temp)

		return np.float_(feature_vector)

def create_feature_matrix(company, data, finance_datatype, finance_n, sentiment_datatype, sentiment_n, day, target, volume):
	matrix = []
	for line in data:
		temp = create_feature_vector(company, line, finance_datatype, finance_n, sentiment_datatype, sentiment_n, day, target, volume)
		if (len(matrix) == 0):
			matrix = np.array([temp])
		else:
			matrix = np.vstack((matrix,temp))

	return matrix

def feature_vector_meaning(company, finance_datatype, finance_n, sentiment_datatype, sentiment_n, day, target, volume):
	print ' _ _ _Settings_ _ _'
	print '  Company: `%s\'' % company

	if target == 0:
		p = "Direction of the stock price change"
	elif target == 1:
		p = "Percentage movement of the stock price"
	print '  Predicting: %s' % p

	if finance_n > 0:
		if finance_datatype == 2:
			fdt = "Real stock price change"
		elif finance_datatype == 1:
			fdt = "Percentage stock price change"
		elif finance_datatype == 0:
			fdt = "Direction of the stock price change"
		fd = "Using %d days of financial data" % finance_n
		print '  Financial Data: %s' % fd
		print '  Financial Datatype: %s' % fdt		
	else: 
		fd = "No financial features"
		print '  Financial Data: %s' % fd

	if sentiment_n == 0:			
		sd = "No sentiment features"
	elif sentiment_n > 0:
		sd = "Using %d days of sentiment data" % sentiment_n
		print '  Sentiment Data: %s' % sd		
		if sentiment_datatype == 1:
			sdt = "All values"
			print '  Sentiment Datatype: %s' % sdt
		elif sentiment_datatype == 0:
			sdt = "Just total score"
			print '  Sentiment Datatype: %s' % sdt

	if day == 1:
		df = "Using day of the week as a feature"
	elif day == 0:
		df = "No day of the week feature"

	if volume == 1:
		vf = "Using volume as a feature"
	elif volume == 0:
		vf = "No volume feature"

	print '  Day Feature: %s' % df
	print '  Volune Feature: %s' % vf

if __name__ == '__main__':
	raw_vector = 'Fri Feb 14	Fri	0.9	4.75	76.349	132.361464937	826.0'
	raw_vector = raw_vector.split('\t')

	print create_feature_vector('jpmorgan', raw_vector, 0, 0, 0, 0, 0, 0 ,0)