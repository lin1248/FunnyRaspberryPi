#!/usr/bin/env python
# encoding: utf-8

import re
import RPi.GPIO
import time
 
# 串行数据输入引脚连接的GPIO口
DS = 13
 
# 移位寄存器时钟控制引脚连接的GPIO口——上升沿有效
SHCP = 19
 
# 数据锁存器时钟控制引脚连接的GPIO口——上升沿有效
STCP = 26
#数码管com1
com1 =  18
#数码管com2
com2 =  23
#数码管com3
com3 =  24
#数码管com4
com4 =  25

com = {com1,com2,com3,com4}

RPi.GPIO.setmode(RPi.GPIO.BCM)
 
RPi.GPIO.setup(DS, RPi.GPIO.OUT)
RPi.GPIO.setup(STCP, RPi.GPIO.OUT)
RPi.GPIO.setup(SHCP, RPi.GPIO.OUT)
RPi.GPIO.setup(com1, RPi.GPIO.OUT)
RPi.GPIO.setup(com2, RPi.GPIO.OUT)
RPi.GPIO.setup(com3, RPi.GPIO.OUT)
RPi.GPIO.setup(com4, RPi.GPIO.OUT)


RPi.GPIO.output(STCP, False)
RPi.GPIO.output(SHCP, False)

def com_pullon():
    RPi.GPIO.output(com1, True)
    RPi.GPIO.output(com2, True)
    RPi.GPIO.output(com3, True)
    RPi.GPIO.output(com4, True)
    
def com_pulldown(n):
    if(n == 0):
        RPi.GPIO.output(com1, False)
    elif n==1:
        RPi.GPIO.output(com2, False)
    elif n==2:
        RPi.GPIO.output(com3, False)
    elif n==3:
        RPi.GPIO.output(com4, False)

def GetDate():
    return time.strftime("%Y:%m:%d",time.localtime(time.time()))


def GetNowTime():
    return time.strftime("%H:%M",time.localtime(time.time()))
 
# 通过串行数据引脚向74HC595的传送一位数据
def setBitData(data):
    # 准备好要传送的数据
    RPi.GPIO.output(DS, data)
    # 制造一次移位寄存器时钟引脚的上升沿（先拉低电平再拉高电平）
    # 74HC595会在这个上升沿将DS引脚上的数据存入移位寄存器D0
    # 同时D0原来的数据会顺移到D1，D1的数据位移到D2。。。D6的数据位移到D7
    # 而D7的数据已经没有地方储存了，这一位数据会被输出到引脚Q7S上
    RPi.GPIO.output(SHCP, False)
    RPi.GPIO.output(SHCP, True)
 
# 指定数码管显示数字num(0-9)，第2个参数是显示不显示小数点（true/false）
# 由于我使用的数码管是共阳数码管，所以设置为低电平的段才会被点亮
# 如果你用的是共阴数码管，那么要将下面的True和False全部颠倒过来，或者统一在前面加上not
def showDigit(num, showDotPoint):
     
    if (num == 0) :     
        setBitData(False)  # G
        setBitData(True) # C
        setBitData(True) # D
        setBitData(True) # E
        setBitData(True) # B
        setBitData(True) # F
        setBitData(True) # A
        setBitData(showDotPoint) # DP
    elif (num == 1) :
        setBitData(False)
        setBitData(True)
        setBitData(False)
        setBitData(False)
        setBitData(True)
        setBitData(False)
        setBitData(False)
        setBitData(showDotPoint)
    elif (num == 2) :
        setBitData(True)
        setBitData(False)
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(False)
        setBitData(True)
        setBitData(showDotPoint)
    elif (num == 3) :
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(False)
        setBitData(True)
        setBitData(False)
        setBitData(True)
        setBitData(showDotPoint)
    elif (num == 4) :
        setBitData(True)
        setBitData(True)
        setBitData(False)
        setBitData(False)
        setBitData(True)
        setBitData(True)
        setBitData(False)
        setBitData(showDotPoint)
    elif (num == 5) :
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(False)
        setBitData(False)
        setBitData(True)
        setBitData(True)
        setBitData(showDotPoint)
    elif (num == 6) :
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(False)
        setBitData(True)
        setBitData(True)
        setBitData(showDotPoint)
    elif (num == 7) :
        setBitData(False)
        setBitData(True)
        setBitData(False)
        setBitData(False)
        setBitData(True)
        setBitData(False)
        setBitData(True)
        setBitData(showDotPoint)
    elif (num == 8) :
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(not showDotPoint)
    elif (num == 9) :
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(False)
        setBitData(True)
        setBitData(True)
        setBitData(True)
        setBitData(showDotPoint)
 
    # 移位寄存器的8位数据全部传输完毕后，制造一次锁存器时钟引脚的上升沿（先拉低电平再拉高电平）
    # 74HC595会在这个上升沿将移位寄存器里的8位数据复制到8位的锁存器中（锁存器里原来的数据将被替换）
    # 到这里为止，这8位数据还只是被保存在锁存器里，并没有输出到数码管上。
    # 决定锁存器里的数据是否输出是由“输出使能端口”OE决定的。当OE设置为低电平时，锁存器里数据才会被输出到Q0-Q7这8个输出引脚上。
    # 在我的硬件连接里，OE直接连接在了GND上，总是保持低电平，所以移位寄存器的数据一旦通过时钟上升沿进入锁存器，也就相当于输出到LED上了。
    RPi.GPIO.output(STCP, True)
    RPi.GPIO.output(STCP, False)
 
try:
    i = 0
    while True:
        #年
        year_str = GetDate()
        year = re.findall(r"\d+\.?\d*",year_str)[0]
        print(str(year))
        for x in range(4000):
            for y_num in year:
                for y in y_num:
                    if i>=4:
                        i = 0
                    com_pullon()
                    #print(str(y))
                    showDigit(int(y),False)
                    com_pulldown(i)
                    i = i+1
        today_str =re.findall(r"\d+\.?\d*",year_str)[1]+re.findall(r"\d+\.?\d*",year_str)[2]
        print(today_str)
        for x in range(4000):
            for t in today_str:
                if i>=4:
                    i = 0
                com_pullon()
                showDigit(int(t),False)
                com_pulldown(i)
                i = i+1
        # day_str = GetToday()
        # day = re.findall(r"\d+\.?\d*",year_str)
        # print("date")
        # print(str(day))
        # for x in range(4000):
            # for d_num in day:
                # for d in d_num:
                    # if i>=4:
                        # i = 0
                    # com_pullon()
                    # print(str(d))
                    # showDigit(int(d),False)
                    # com_pulldown(i)
                    # i = i+1
        time_str = GetNowTime()
        nums = re.findall(r"\d+\.?\d*",time_str)
        print(str(nums))
        for x in range(4000):
            for num in nums:
                for n in num:
                    if i>=4:
                        i = 0
                    com_pullon()
                    #print(str(n))
                    showDigit(int(n),False)
                    com_pulldown(i)
                    i = i+1
                    #time.sleep(0.1)
    # 测试代码
    # 从0显示到9，不显示小数点
    #for x in range(0,10):
    #    showDigit(x, False)
    #    time.sleep(0.2)
 
    # 再从0显示到9，显示小数点
    #for y in range(0,10):
    #    showDigit(y, True)
    #    time.sleep(0.2)
                     
except KeyboardInterrupt:
    pass
 
# 最后清理GPIO口
# 清理了IO是将所有使用中的IO口释放，并全部设置为输入模式
# 你会发现最后设置的数据在清理了IO口以后还会继续正常显示
# 这是因为数据一旦存入锁存器，除非断电或重置数据（MR口设置为低电平），
# 否则最后设置的数据会一直保留在74HC595芯片中。也就是被“锁存”了。
RPi.GPIO.cleanup()
