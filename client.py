import time
import sys
import socket
import os


special_symbol = b'~~~~~~~~~~'

# Print iterations progress
#https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/30740258
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


def main():
    file_name = sys.argv[1] 
    host = sys.argv[2] 
    port = sys.argv[3] 

    sock= socket.socket()
    sock.connect((host, int(port)))
    sock.send(file_name.encode()+special_symbol)


    f = open(file_name, 'rb')
    statinfo = os.stat(file_name)
    print(statinfo.st_size)
    num_chunks = statinfo.st_size//1024 + 1
    printProgressBar(0, num_chunks, prefix = 'Progress:', suffix = 'Complete', length = 50)
    iteration = 0
    try:
        chunk = f.read(1024)
        while chunk:
            # print('readdata')
            sock.send(chunk)
            chunk = f.read(1024)
            iteration += 1
            printProgressBar(iteration, num_chunks, prefix = 'Progress:', suffix = 'Complete', length = 50)
    finally:
        sock.send(special_symbol)
        f.close()

    sock.close()



main()