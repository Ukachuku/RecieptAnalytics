#script to run the ocr for Ralph's reciepts
import subprocess

#define command and arguments
command='Rscript'
path2script='/home/pi/Downloads/RecieptAnalytics/Ralphs/RalphOCR.R'

#build subprocess command
cmd=[command, path2script]

x = subprocess.check_output(cmd, universal_newlines=True)
