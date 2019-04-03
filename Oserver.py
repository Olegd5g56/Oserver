#!/usr/bin/env python3
import os
import sys
import time
import urllib.request
from subprocess import Popen, PIPE

root = str(os.path.expanduser('./'))
ngrok = ""

class Color:
  Red = '\033[91m'
  Green = '\033[92m'
  Yellow = '\033[93m'
  Blue = '\033[94m'
  Magenta = '\033[95m'
  Cyan = '\033[96m'
  White = '\033[97m'
  Grey = '\033[90m'
  BOLD = '\033[1m'
  ITALIC = '\033[3m'
  UNDERLINE = '\033[4m'
  END = '\033[0m'

def start():
   ngrokstart("http")
def stop():
   print("Уничтожение процесса ngrok")
   os.system("sudo killall "+ngrok)
   os.system("sudo rm ./screenlog.0")
def state():
   a=Popen("ps -C "+ngrok+" | grep "+ngrok, shell=True, stdin=PIPE, stdout=PIPE).stdout.read()
   if "ngrok" in str(a):printC("Активно",Color.Green)
   else:printC("Не активно",Color.Red)
def help():
   printC("start - Запустить",Color.Blue)
   printC("stop - Остановить",Color.Blue)
   printC("state - Узнать состояние",Color.Blue)
   printC("help - Подзкаски",Color.Blue)
def getArchitecture():
  a=Popen("dpkg --print-architecture", shell=True, stdin=PIPE, stdout=PIPE).stdout.read()
  if "armhf" in str(a): 
    ngrok="ngrokArm"
  else: 
    ngrok="ngrokX86"
  return ngrok
def ngrokstart(p):
  id = 0
  for el in conf("port"):
    os.system("sudo rm ./screenlog.0")
    thisPort = el.split(" ")

    protocol = thisPort[0]
    port = thisPort[1]
    authtoken = thisPort[2]
    script = thisPort[3]

    if(script != "none"):os.system("sudo sh "+script)
    os.system("echo 'authtoken: "+authtoken+"' > ~/.ngrok2/ngrok.yml")
    print("Запуск ngrok "+protocol+" "+port)
    os.system("sudo screen -d -m -L "+root+"ngrok/"+ngrok+" "+protocol+" "+port)
    print("Пауза 10 секунд")
    time.sleep(15)
    read(id)
    id=id+1
    
def read(id):
  print("Чтение screenlog.0 и выделение веб адреса")
  handle = open("./screenlog.0", "r")
  data = handle.read()
  data1 = data.split('Forwarding')

  if(len(data1) > 1):
   data2 = data1[1].split(' -> ')
   data3 = data2[0].split(' ')
   data4 = data3[len(data3)-1]
   handle.close()
   printC("Найден веб адрес:"+data4,Color.Green)
   urllib.request.urlopen(conf("host")+data4+"&id="+str(id))
   printC("Отправка на хостинг",Color.Green)
  else:
    printC("Ошыбка!Повторите попытку!",Color.Red)
    handle.close()
    
def printC(str,color):
  print(color+str+Color.END)

def readConf(str):
  try:
      data = open(root+"main.conf", "r").read().split("\n")
      rez=[]
      for element in data:
        param = element.split("|")
        if(param[0]==str and "#" not in element): rez.append(param[1])
      return rez

  except BaseException:
       printC("Нет файла конфигурации или он пуст!!!(main.conf)",Color.Red)
       exit()

def conf(str):
   param = readConf(str)

   if(str == "host"):
     return param[0]

   elif(str == "port"):
     return param

   else:exit()

#begin

if(len(sys.argv)>1): 
  param = sys.argv[1]
else: param = "null"

ngrok = getArchitecture()

if(param=="null" or param=="help"):
  help()
if(param=="start"):
  stop()
  start()
if(param=="stop"):
  stop()
if(param=="state"):
  state()

