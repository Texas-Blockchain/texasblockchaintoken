#use this to test cron, need to change 
from datetime import datetime
dirname = "/home/bitcoinnode/texasblockchaintoken/cron"
myFile = open(dirname + '/append.txt', 'a') 
myFile.write('\nAccessed on ' + str(datetime.now()))
