# Twitch-bot
detect malicious urls in twitch chat and delete those messages using machine learning and NLP

unzip  rf300_4.zip

but your twitch account oauth token in line 11 of URLTG.py. you can get token from https://twitchapps.com/tokengen/ 

    def __init__(self):

        super().__init__(token='', prefix='?', initial_channels=['ankur23'])
        
        
## install required Library
    pip install -r requirements.txt

## run URLTG.py 
    python URLTG.py 
