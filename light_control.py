#from CameraTest import *
#from display_timer import *
import RPi.GPIO as gpio
import tm1637
import time

gpio.setmode(gpio.BCM)
tm= tm1637.TM1637(19,13)
light_1 = [14,15,18]    # Set at these GPIO positions
light_2 = [2,3,4]
light_3 = [17,27,22]
light_4 = [10,9,11]

light_1_prev = [False,False]
light_2_prev = [False,False]
light_3_prev = [False,False]
light_4_prev = [False,False]
lights = [light_1,light_2,light_3,light_4]

# interval
interval = 50
multiplier = 0.2

for i in lights:
    for j in i:
        gpio.setup(j,gpio.OUT)



def light_test(): 
    for i in lights:
        for j in i:
            tm.number(j)
            gpio.output(j,gpio.HIGH)
            time.sleep(5)
            gpio.output(j,gpio.LOW)
            time.sleep(0.05)

    
def light_on_red(max_index:int):
    for i in lights:
            if lights.index(i) != max_index:
                gpio.output(i[-1],gpio.LOW)
                gpio.output(i[1],gpio.LOW)
                time.sleep(0.5)
                gpio.output(i[0],gpio.HIGH)
            else:
                gpio.output(i[1],gpio.LOW)
                gpio.output(i[0],gpio.LOW)
                time.sleep(0.5)
                gpio.output(i[-1],gpio.HIGH)

def light_yellow(max_index:int):
    for i in lights:
        if lights.index(i) != max_index:
            gpio.output(i[0],gpio.LOW)
            time.sleep(0.5)
            gpio.output(i[1],gpio.HIGH)
        else:
            gpio.output(i[-1],gpio.LOW)
            time.sleep(0.5)
            gpio.output(i[1],gpio.HIGH)        

def light_off(max_index:int):   
        for i in lights:
            if lights.index(i) != max_index:
                gpio.output(i[1],gpio.LOW)
                time.sleep(0.5)
                gpio.output(i[0],gpio.HIGH)
            else:
                gpio.output(i[1],gpio.LOW)
                time.sleep(0.5)
                gpio.output(i[0],gpio.HIGH)
def light_control(duration:int):
    global interval
    global multiplier
    for i in lights:
        gpio.output(i[1],gpio.LOW)
        gpio.output(i[-1],gpio.LOW)
        gpio.output(i[0],gpio.HIGH)
    count = [20,4,1,15]#traffic_count([0,2],duration)
    max_value , max_index = max(count) , count.index(max(count))
    light_on_red(max_index)
    print(count)
    print(interval )
    #display_timer(interval)
    light_yellow(max_index)
    #display_timer(2.5)
    light_off(max_index)
    #display_timer(10)
    for i in lights:
        for j in i:
            gpio.output(j,gpio.LOW)

def control_test():
    max_value , max_index = 0,0
    for j in range(3):    
        for i in range(4):
            light_on_red(i)
            print(f'Light{i}')
            time.sleep(interval)
            light_yellow(i)
            time.sleep(2)
            light_off(i)
    print('complete')

tm.show('  10')
time.sleep(2.5)
tm.show('done')
time.sleep(2.5)
tm.write([0,0,0,0])
gpio.cleanup()
print('Cleaned Up')
