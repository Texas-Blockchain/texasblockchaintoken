from datetime import datetime
myFile = open('/Users/jacksharkey/Documents/Programming/Texas/Blockchain/cron/append.txt', 'a') 
myFile.write('\nAccessed on ' + str(datetime.now()))