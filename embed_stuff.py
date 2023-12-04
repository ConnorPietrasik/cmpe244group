from threading import Thread
from time import sleep
import os
import lgpio
#import lib.lcd as lcd
import lib.tempsens as DHT

PWM_OUT = 12
DHT_PIN = 17

def spin_fan():
    t_dif = cur_temp - goal_temp

    # if (cur_temp > prev_temp - 0.5 and cur_temp < prev_temp + 0.5):
    #     return
    # if t_dif < 0:
    #     lgpio.tx_pwm(h, PWM_OUT, 0, 0)
    # elif t_dif < 2:
    #     lgpio.tx_pwm(h, PWM_OUT, 10000, 50)
    # elif t_dif < 4:
    #     lgpio.tx_pwm(h, PWM_OUT, 10000, 75)
    # else:
    #     lgpio.tx_pwm(h, PWM_OUT, 10000, 100) 

    #For LED testing
    if t_dif < 0:
        lgpio.tx_pwm(h, PWM_OUT, 0, 0)
    elif t_dif < 2:
        lgpio.tx_pwm(h, PWM_OUT, 1, 50)
    elif t_dif < 4:
        lgpio.tx_pwm(h, PWM_OUT, 2, 50)
    else:
        lgpio.tx_pwm(h, PWM_OUT, 10, 50) 

def display_lcd():
    print("display lcd here")

def do_stuff():
    global cur_temp

    while enable:
        avgTemp = 0
        #take average of 3 temp readings for accuracy
        # try:
        #     for i in range(3):
        #         while dht.readDHT11Once() == dht.DHTLIB_INVALID_VALUE:
        #             print("Invalid temp reading")
        #             sleep(1)
        #         avgTemp += dht.temperature
        #         sleep(0.1)
        # except RuntimeError:
        #     print("Temperature check failed")

        # #calculate average
        # cur_temp = int(avgTemp/3)
		
        #display_lcd()
        spin_fan()
        sleep(5)
        

def start():
    global enable, fan_thread
    enable = True
    fan_thread = Thread(target=do_stuff)
    fan_thread.start()

def stop():
    global enable, fan_thread
    enable = False
    fan_thread.join()
    lgpio.gpio_write(h, PWM_OUT, 0)
    lgpio.gpio_free(h, PWM_OUT)


def init_fan():
    global h
    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, PWM_OUT)

def init_dht():
    global dht
    dht = DHT.DHT(h, DHT_PIN)
    lgpio.gpio_claim_input(h, DHT_PIN)

def init():
    global doc_root, goal_temp, cur_temp, h
    doc_root = os.path.dirname(__file__)
    with open(doc_root + "/goal_temp.txt","r") as f:
        goal_temp = float(f.read())
    cur_temp = 30.1
    init_fan()
    init_dht()
    start()

if __name__ == "__main__":
    print("temp")