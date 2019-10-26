#https://stackabuse.com/scheduling-jobs-with-python-crontab/
from crontab import CronTab

#Need to fill in these values
rootUsername = ""
pathToFolder = ""

cron = CronTab(user=rootUsername)

#Add jobs to the cron file
#@param command is the command to run on a given file e.g "python" or "node"
#@fileName is the file we want to add. Don't need to include directory info
def addNewJob(command, fileName):
    cron = CronTab(user=rootUsername)
    job = cron.new(command=command + " " + pathToFolder + "/" + fileName)

    #Need to adjust this depending on the file we're adding - Example usage:
    #job.minute.every(minutes)
    #job.hour.every(hours)
    #job.dow.on('SUN')
    #job.dow.on('SUN', 'FRI')
    job.minute.every(1)

    cron.write()

def viewAllJobs():
    for job in cron:
        print (job)

def emptyCronFile():
    cron.remove_all()

#Example calls:
#add a git pull - don't need to specify file name just folder
#addNewJob("git pull", "")

#add the qr mint
#addNewJob("python ", "qr_mint.py")

