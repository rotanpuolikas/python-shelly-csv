import urllib.request
import json
import time
import os

# SHELLY IP
shelly_ip = '192.168.1.173'
bigfile = 'data.csv'
interval = 1

def checkfile():
    if not os.path.isfile(f'./{bigfile}'):
        print(f'creating file ./{bigfile}')
        outToFile('unixtime;apower\n')
    else:
        print(f'appending to ./{bigfile}')

def requestData():
    try:
        with urllib.request.urlopen(f'http://{shelly_ip}/rpc/Shelly.GetStatus') as url:
            data = json.load(url)
            return data
    except:
        print('error connecting to shelly plug')
        return None

def outToFile(line):
    with open(f'./{bigfile}', 'a') as file:
        file.write(line)

def formOutputLine(data):
    line = ''
    line += str(data['sys']['unixtime']) + ';'
    line += str(data['switch:0']['apower'])

    line += '\n'
    return line

def main():
    print('alr lets go')
    print('ctrl + c to exit')
    checkfile()
    while True:
        data = requestData()
        line = formOutputLine(data)
        if line != None:
            outToFile(line)
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\ngraceful exit maybe\n')
        exit()
    except Exception as e:
        print(f'\nEXCEPTION: {e}\n')
