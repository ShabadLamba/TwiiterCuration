import tweepy
from pprint import pprint
import mandrill
import sys
from re import sub

def htmlGenerator(imageUrl,screen_name,userId,userName,date,text):
	
	output = '<div style="width: 570px;height: 50px;padding: 15px;background-color: #fff;border: 1px solid #ececec; border-bottom:0px">'
	output += '<a href=%s style="text-decoration: none;color: #222;font-family: helvetica neue;">' % ("http://twitter.com/" + screen_name + "/status/" + userId)
	output += '<div style="width: 100%;">\
						<div class="left" style="float: left;margin-right: 10px;">\
							<img src=' + "'" + imageUrl + "'"
	output += 'style="">\
						</div>\
						<div class="right">\
							<div class="header" style="">\
								<strong style="float: left;margin-right: 10px;font-weight: bold;font-size: 14px;">' + userName + '</strong>\
								<span style="float: left;margin-right: 10px;color: #8899a6;font-weight: normal;font-size: 13px;line-height: 1.4;">@' + screen_name + '</span>\
								<span style="float: left;margin-right: 10px;color: #8899a6;font-weight: normal;font-size: 13px;line-height: 1.4;">' + date + '</span>\
							</div>	\
							<br>\
							<div class="body" style="font-size: 14px; margin-top: 5px;">\
								<div>'\
									+ text +\
								'</div>\
							</div>\
						</div>\
					</div>\
				</a>\
			</div>'
	return output

def htmlHeaderGenerator(arg):
	output = '<div style="background-color:#f5f8fa; width: 600px; height: auto; padding: 20px;">\
	<div style="margin-left: auto; margin-right: auto; text-align: center;">\
		<a href="http://supergenieapp.com">\
			<img src="http://getgenieapp.com/images/logo.png" style="width: 100px;" />\
			<br>\
			<img src="http://getgenieapp.com/assets/img/websiteAssets/web1280x640/Header/font_1280x640.png" style="width: 150px;" /> \
		</a>\
	</div>\
	<br>\
	<div style="text-align: center; font-size: 28px; font-weight: 100; color: #444; font-family: Helvetica neue">'
	output += "#" + arg
	output +='</div>\
	<br>\
	<div style="width: auto; height: auto; border-bottom: 1px solid #ececec;">'
	return output

def htmlFooterGenerator():
	output = '</div>\
	<br>\
	<div style="text-align: center; font-size: 13px; color: #666; font-family: Helvetica neue">&copy; 2015 <a href="http://supergenieapp.com" style="text-decoration: none; color: #666;">SuperGenie</div>\
	</div>'
	return output

consumer_key = "t2rtHgnTtMT53DWAGVavr7RWm"
consumer_secret = "FrWYjoqBWMqXtgt9JujtTGm5DiR7edQ4DKn4pkm26deFomspA3"
access_token = "2534407633-q8jHtZxSG9o0tuKcwrNqC566v4t9fQmqckTm6E6"
access_token_secret = "RpmpRgVq1BdXYEZFA3S1nz5inqVKSrbhmLeZWMlUTvB7S"
mandrill_client = mandrill.Mandrill('vl6uH3MApPiKPQasHIZ7FA')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# try:
#     redirect_url = auth.get_authorization_url()
# except tweepy.TweepError:
#     print 'Error! Failed to get request token.'

# verifier = raw_input('Verifier:')
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

htmlString = ''

htmlString += htmlHeaderGenerator(str(sys.argv[1]))
listOfTopTweets = {}
listOffavoriteCount = []
count = 0
for i in range(1,30):
	public_tweets = api.search(str(sys.argv[1]), 'en',count=100,pages=i)
	
	
	for tweet in public_tweets:
	    # pprint(tweet.text)
	    # pprint(tweet,width = 1)
	    # break
	    try:
			if(tweet.retweeted_status):
				continue
	    except:
			flag = 1
			for key in listOfTopTweets:
				if tweet.id_str in listOfTopTweets[key][0]:
					flag = 0
				# else:
				# 	flag = 0
			if(flag):
				listOfTopTweets[count] = [htmlGenerator(str(tweet.user.profile_image_url),tweet.user.screen_name, tweet.id_str,tweet.user.name,str(str(tweet.created_at).split(' ')[0]),tweet.text),tweet.favorite_count]
				count += 1
			# output  + " "
	    # pprint(tweet._json['profile_image_url_https'])
	    # pprint(tweet._json['name'])

for key in listOfTopTweets:
	if listOfTopTweets[key][1] not in listOffavoriteCount:
		listOffavoriteCount.append(listOfTopTweets[key][1])

listOffavoriteCount.sort(reverse=True)
# listOffavoriteCount = listOffavoriteCount[0:10]

countOfTweets = 0
for favCount in listOffavoriteCount:
	for key in listOfTopTweets:
		# if countOfTweets<10:
		if listOfTopTweets[key][1] == favCount:
			htmlString += listOfTopTweets[key][0]
			listOfTopTweets[key] = [None,None]
			countOfTweets += 1
		# else:
		# 	break

# print listOffavoriteCount
# print listOfTopTweets
htmlString += htmlFooterGenerator()
print sub(r"[^\x00-\x7F]+","",htmlString)
# pprint(listOfTopTenTweets)
try:
    message = {
     'from_email': 'prabhjot@getgenieapp.com',
     'from_name': 'Competitor Analysis',
     'headers': {'Reply-To': 'noreply@getgenieapp.com'},
     'html': htmlString,
     'subject': 'Twitter Activity ' + sys.argv[1],
     'text': 'plain text not supported. Open html email.',
     'to': [{'email': 'prabhjot@getgenieapp.com',
             'name': 'prabhjot singh lamba',
             'type': 'to'}, 
             {'email': 'chaitanya@getgenieapp.com',
             'name': 'chaitanya pampana',
             'type': 'to'}, 
             {'email': 'satya@martmobi.com',
             'name': 'satya krishna ganni',
             'type': 'to'}],
     'view_content_link': None}
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
    '''
    [{'_id': 'abc123abc123abc123abc123abc123',
      'email': 'recipient.email@example.com',
      'reject_reason': 'hard-bounce',
      'status': 'sent'}]
    '''

except mandrill.Error, e:
    # Mandrill errors are thrown as exceptions
    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
    raise
