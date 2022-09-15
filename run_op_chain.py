# -*- coding: utf-8 -*-
#Short python script for the different phases of an operational chain
#IMPORT OF THE MODULS
from datetime import datetime
import os
import sys
#import download_data
#import model
import send_email_mailx
import configparser
import time

#DATE DEFINITIONS
if len(sys.argv) == 1:
    date = datetime.utcnow()
    date_time_str = date.strftime('%Y-%m-%d')
    dateBrief = datetime.strftime(date, "%Y%m%d")
else:
    date_time_str = sys.argv[1] + ' 00:00:00.000000'
    date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    dateBrief = datetime.strftime(date, "%Y%m%d")
print (date)
hour = 0
run_date = datetime(date.year, date.month, date.day, hour)

#Setting Environmental Variables
os.system("ulimit -s unlimited") #Set it to modify for example the resource limit of the current user.
config = configparser.ConfigParser()
# config.read(os.environ["HOME"]+'/cuba/config.ini')
config.read('./config.ini')
work = config.get('BASIC','WORK').format(USER=os.environ.get('USER'))
data = config.get('BASIC','DATA').format(USER=os.environ.get('USER'))
inDir = config.get('BASIC','inDir').format(WORK=work, bul_date=dateBrief)
tmpDir = config.get('BASIC','tmpDir').format(WORK=work, bul_date=dateBrief)
outDir = config.get('BASIC','outDir').format(WORK=work, bul_date=dateBrief)
logDir = config.get('BASIC','logDir').format(WORK=work, bul_date=dateBrief)
baseDir = config.get('BASIC','baseDir').format(HOME=os.environ.get('HOME'))
archiveDir = config.get('BASIC','archiveDir').format(DATA=data)
dirList=[inDir,tmpDir,outDir,logDir,archiveDir]
#Create all the directories
for directory in dirList:
    try:
        # Create the directory in the path
        os.makedirs(directory, exist_ok = True)
        print("Directory %s Created Successfully" % directory)
    except OSError as error:
        print("Directory %s Creation Failed" % directory)

#Go inside the scripts directory  
os.chdir(baseDir)

#print("Inizio elaborazione modello WRF-MNW "+str(datetime.utcnow()))
print("Starting of the chain at: "+str(datetime.utcnow()))

# sys.exit()
#DATA DOWNLOAD
try:
    print("Download Started!")
    #download_data.download(run_date,work_path)
    time.sleep(3)
except SystemExit as exc:
    if exc.code == 1:
        print("Errore nel download dei dati! Interrompo l'elaborazione! "+str(datetime.utcnow()))
        s = send_email_mailx.mailer("Download:Problems.","Errore:nel:download:dei dati.!Interrompo:l'elaborazione.!"+str(datetime.utcnow()))
        s.send()
        sys.exit()

#PRE-PROCESSING on the input files
try:
    print("Pre-Processing started!")
    #wrf.wps(run_date, work_path)
    time.sleep(2)
except SystemExit as exc:
    if exc.code == 2:
        print("Error in cutting of the files! Stopping the elaboration! "+str(datetime.utcnow()))
        s = send_email_mailx.mailer("Cutting:Problems.","Error:in:cutting:of:files!:Stopping:the:elaboration."+str(datetime.utcnow()))
    elif exc.code == 3:
        print("Error in renaming the variables! Stopping the elaboration! "+str(datetime.utcnow()))
        s = send_email_mailx.mailer("Renaming:variables:problems.","Error:in:renaming:of:some:variables!:Stopping:the:elaboration!"+str(datetime.utcnow()))
    s.send()
    sys.exit()
print("Pre-Processing DONE!")

#MODEL EXECUTION
try:
    print("Model run started!")
    #wrf.wrf(run_date, work_path)
    time.sleep(5)
except SystemExit as exc:
    print("Error in running the Model! Stopping the elaboration! "+str(datetime.utcnow()))
    s = send_email_mailx.mailer("Model:Problems.","Error:running:the:Model!:Stopping:the:elaboration."+str(datetime.utcnow()))
    s.send()
    sys.exit()
print("Model Execution DONE!")

#POSTPROCESSING EXECUTION
try:
    print("Post-Processing started!")
    #post.post(run_date, work_path)
    time.sleep(2)
except SystemExit as exc:
    if exc.code == 4:
        print("Error in post-processing of the files! Stopping the elaboration! "+str(datetime.utcnow()))
        s = send_email_mailx.mailer("Post-Processing:Problems.","Error:in:postprocessing:of:the:files!:Stopping:the:elaboration."+str(datetime.utcnow()))
    if exc.code == 5:
        print("Error in compression of the files! Stopping the elaboration! "+str(datetime.utcnow()))
        s = send_email_mailx.mailer("Compression:Problems.","Error:in:compression:of:the:files!:Stopping:the:elaboration."+str(datetime.utcnow()))
    s.send()
    sys.exit()
print("Post-Processing Execution DONE!")

#GRAPHICS EXECUTION
try:
    print("Images creation started!")
    #post.graphic(run_date, work_path)
except SystemExit as exc:
    print("Error in images creation! Stopping the elaboration! "+str(datetime.utcnow()))
    s = send_email_mailx.mailer("Images:Problems.","Error:in:images:creation!:Stopping:the:elaboration."+str(datetime.utcnow()))
    s.send()
    sys.exit()
print("Images creation DONE!")

#UPLOAD STARTS
try:
    print("Upload started!")
    #post.wind_map(work_path)
    time.sleep(3)
except SystemExit as exc:
    print("Error in uploading of the files! Stopping the elaboration! "+str(datetime.utcnow()))
    s = send_email_mailx.mailer("Upload:Problems.","Error:in:uploading:of:the:files!:Stopping:the:elaboration."+str(datetime.utcnow()))
    s.send()
    sys.exit()
print("Data accepted by upload server.")
print("Upload Execution DONE!")
