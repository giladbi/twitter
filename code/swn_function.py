# -*- coding: cp1252 -*-
import nltk, enchant,re,math
from nltk.corpus import wordnet as wn
from sentiwordnet import SentiWordNetCorpusReader, SentiSynset

swn_filename = 'SentiWordNet_3.0.0_20130122.txt'
swn = SentiWordNetCorpusReader(swn_filename)

dictionary = enchant.Dict("en_US")
emotipatternhappy = re.compile("(:-\))|(:\))|(:o\))|(:])|( :3 )|(:c\))|(:>)|(=])|(8\))|(=\))|(:})|(:\^\))|(:'-\))|(:'\))")
emotipatternveryhappy = re.compile("(:-D)|( :D )|(8-D)|( 8D )|(x-D)|( xD )|(X-D)|( XD )|(=-D)|( =D )|(=-3)|( =3 )|(B\^D)|(:-\)\))|(:\)\))")
emotipatternsad = re.compile("(>:\[)|(:-\()|(:\()|(:-c)|( :c )|(:-<)|(:<)|(:-\[)|(:\[)|(:{)|(:'\()|(:'-\()")
emotipatternverysad = re.compile("(D:<)|( D: )|( D8 )|(D;)|(D=)|( DX )|(v\.v)|(D-':)|(:-\|\|)|(>:\()")

def calculate_sentiment(tweet,followers):

	#### Emoticon ####
	emotipos = 0.3 * len(emotipatternhappy.findall(tweet))
	emotipos = emotipos + 0.5 * len(emotipatternveryhappy.findall(tweet))
	emotineg = 0.3 * len(emotipatternsad.findall(tweet))
	emotineg = emotineg + 0.5 * len(emotipatternverysad.findall(tweet))

	emotiscore = emotipos - emotineg
	if emotiscore > 1:
	    emotiscore = 1
	if emotiscore < -1:
	    emotiscore = -1

	#### Hash Score & SWN Score ####
	#remove punctuation as this will mess up pos tagging
	tweet = re.sub('[\$\£\+\'(..)(...)\?!\(\)\[\]":;-]\&','',tweet)
	tweet = re.sub('[\?!]','.',tweet)
	tweet = re.sub('[\(\)\[\]":;]',',',tweet)
	tweet = re.sub('[\.\,]',' ',tweet)
	tweet = re.sub('-',' ',tweet)

	#remove web addresses, @replies and RTs as this will mess up pos tagging
	tokenized_query = nltk.word_tokenize(tweet)
	for token in tokenized_query:
	    if isinstance(token, unicode):
	        tokenized_query.remove(token) #because our dictionary can't handle unicode
	    elif re.findall('http',token) or re.findall('@',token):
	        tokenized_query.remove(token) #remove stuff that is not words
	    else:
	        try:
	            if not dictionary.check(token) and not (token == '#'):
	                try:
	                    tokenized_query.remove(token)
	                except:
	                    pass
	        except:
	            pass

	#have to divide into pos tags in order to get the right wordnet sense of each word
	tagged_query = nltk.pos_tag(tokenized_query)

	hashpos = 0 #these are the positive and negative scores for each word
	hashneg = 0 #hash_ is scores for hashtags

	swnpos = 0  #swn_ is scores for normal words
	swnneg = 0
	is_hashtag = False
	for (word,tag) in tagged_query:
	    sentiwordnet_scores = "" #these will hold the scores objects returned by SentiWordNet
	    hashtag_swn_scores = ""  #containing a pos, neg, and objective (not used) score
	    multiplier = False
	    
	    if word == '#': 
	        is_hashtag = True #tokenizer splits hash symbols out from their words, so we record the fact that the next word is a hashtag
	        
	    elif len(word)<3:
	        is_hashtag = False #in case we need to reset
	    else:
	        if tag in ['NN','NNS','NNP']:
	            #if hashtag, get hashtag score
	            if is_hashtag:
	                try:
	                    hashtag_swn_scores = swn.senti_synset(wn.synsets(word, wn.NOUN)[0].name)
	                except:
	                    try:
	                        hashtag_swn_scores = swn.senti_synset(wn.morphy(word, wn.NOUN)[0].name)
	                    except:
	                        pass
	                is_hashtag = False #reset
	            
	        #if there are repeated characters or the word is all caps ('intensifiers'), multiplier effect
	        #note we don't check for intensifiers on hashtags because they don't really add extra meaning to hashtags
	            else:
	                if re.findall(r'(.)\1{3,}',word) or (not re.findall('[a-z]',word)):
	                    multiplier = True
	                try:
	                    sentiwordnet_scores = swn.senti_synset(wn.synsets(word, wn.NOUN)[0].name)
	                except:
	                    try:
	                        sentiwordnet_scores = swn.senti_synset(wn.morphy(word, wn.NOUN)[0].name)
	                    except:
	                        pass
	        elif tag == 'JJ':
	            if is_hashtag:
	                try:
	                    hashtag_swn_scores = swn.senti_synset(wn.synsets(word, wn.ADJ)[0].name)
	                except:
	                    try:
	                        hashtag_swn_scores = swn.senti_synset(wn.morphy(word, wn.ADJ)[0].name)
	                    except:
	                        pass
	                is_hashtag = False
	                    
	            else:
	                if re.findall(r'(.)\1{3,}',word) or not re.findall('[a-z]',word):
	                    multiplier = True
	                try:
	                    sentiwordnet_scores = swn.senti_synset(wn.synsets(word, wn.ADJ)[0].name)
	                except:
	                    try:
	                        sentiwordnet_scores = swn.senti_synset(wn.morphy(word, wn.ADJ)[0].name)
	                    except:
	                        donothing = True
	        elif tag in ['VBP','VBZ','VBG','VBP','VB','VBD']:
	            if is_hashtag:
	                try:
	                    hashtag_swn_scores = swn.senti_synset(wn.synsets(word, wn.VERB)[0].name)
	                except:
	                    try:
	                        hashtag_swn_scores = swn.senti_synset(wn.morphy(word, wn.VERB)[0].name)
	                    except:
	                        pass
	                is_hashtag = False
	                    
	            else:
	                if re.findall(r'(.)\1{3,}',word) or not re.findall('[a-z]',word):
	                    multiplier = True
	                try:
	                    sentiwordnet_scores = swn.senti_synset(wn.synsets(word, wn.VERB)[0].name)
	                except:
	                    try:
	                        sentiwordnet_scores = swn.senti_synset(wn.morphy(word, wn.VERB)[0].name)
	                    except:
	                        pass

	        if (hashtag_swn_scores != "") and (hashtag_swn_scores is not None) and (hashtag_swn_scores.pos_score >0.1 or hashtag_swn_scores.neg_score >0.1):
	            hashpos = hashpos + hashtag_swn_scores.pos_score
	            hashneg = hashneg + hashtag_swn_scores.neg_score

	        elif (sentiwordnet_scores != "") and (sentiwordnet_scores is not None) and (sentiwordnet_scores.pos_score >0.1 or sentiwordnet_scores.neg_score >0.1):
	        
	            if multiplier:
	                sentiwordnet_scores.pos_score = sentiwordnet_scores.pos_score * 2
	                if sentiwordnet_scores.pos_score > 1:#cap to 1
	                    sentiwordnet_scores.pos_score = 1
	                sentiwordnet_scores.neg_score = sentiwordnet_scores.neg_score * 2
	                if sentiwordnet_scores.neg_score > 1:
	                    sentiwordnet_scores.neg_score = 1
	        
	            swnpos = swnpos + sentiwordnet_scores.pos_score
	            swnneg = swnneg + sentiwordnet_scores.neg_score    

	hashscore = hashpos - hashneg
	if hashscore > 1:
	    hashscore = 1
	if hashscore < -1:
	    hashscore = -1

	swnscore = swnpos - swnneg
	if swnscore > 1:
	    swnscore = 1
	if swnscore < -1:
	    swnscore = -1

	totalscore = math.log(int(followers)+1)*((swnscore + hashscore + emotiscore)/3)
	if totalscore > 1:
	    totalscore = 1
	if totalscore < -1:
	    totalscore = -1

	return [emotiscore, hashscore, swnscore, totalscore]