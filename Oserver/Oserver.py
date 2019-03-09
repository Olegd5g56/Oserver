#!/usr/bin/env python3
import os
import sys
import time
import urllib.request
from subprocess import Popen, PIPE

root = str(os.path.expanduser('~/'))+"Oserver/"

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

def printC(str,color):
  print(color+str+Color.END)

def conf(str):
   try:
      data = open(root+"main.conf", "r").read().split("\n");
      if(data[0]==""):exit()
      if(str=="hosting"):return data[0]
   except BaseException:
       printC("Нет файла конфигурации или он пуст!!!(main.conf)",Color.Red)
       exit()

if(len(sys.argv)>1): param = sys.argv[1]
else: param = "null"


a=Popen("dpkg --print-architecture", shell=True, stdin=PIPE, stdout=PIPE).stdout.read()
if "armhf" in str(a): ngrok="ngrokArm"
else: ngrok="ngrokX86"


if(param=="null" or param=="help"):
    printC("start - Запустить",Color.Blue)
    printC("stop - Остановить",Color.Blue)
    printC("state - Узнать состояние",Color.Blue)
    printC("help - Подзкаски",Color.Blue)

if(param=="start"):
  print("Уничтожение процесса ngrok")
  os.system("sudo killall "+ngrok)
  print("Удаление screenlog.0")
  os.system("sudo rm ./screenlog.0")

  print("Перезапуск apache")
  a=Popen("ps -C apache2 | grep apache", shell=True, stdin=PIPE, stdout=PIPE).stdout.read()
  if "apache2" in str(a):printC("apache уже запущен!",Color.Green)
  else:
    printC("Запускаю apache!",Color.Green)
    os.system("sudo /etc/init.d/apache2 stop ; sudo /etc/init.d/apache2 start")

  print("Запуск ngrok с выводом в screenlog.0")

  os.system("sudo screen -d -m -L "+root+"ngrok/"+ngrok+" http 80")
  print("Пауза 10 секунд")
  time.sleep(11)

  print("Чтение screenlog.0 и выделение веб адреса")
  handle = open("./screenlog.0", "r")
  data = handle.read()
  data1 = data.split('Forwarding')

  if(len(data1) > 1):
   data2 = data1[1].split(' -> ')
   data3 = data2[0].split(' ')
   data4 = data3[len(data3)-1]
  else:
    printC("Ошыбка!Повторите попытку!",Color.Red)
    exit()

  handle.close()

  printC("Найден веб адрес:"+data4,Color.Green)

  urllib.request.urlopen(conf("hosting")+data4)
  printC("Отправка на хостинг",Color.Green)

if(param=="stop"):
   print("Щя все будет начальник")
   os.system("sudo killall "+ngrok)
   os.system("sudo rm ./screenlog.0")


if(param=="state"):
   a=Popen("ps -C "+ngrok+" | grep "+ngrok, shell=True, stdin=PIPE, stdout=PIPE).stdout.read()
   if "ngrok" in str(a):printC("Активно",Color.Green)
   else:printC("Не активно",Color.Red)
