from threading import Thread
from time import sleep
import os
import lgpio
from lib.lcd import LCD
import lib.tempsens as DHT

PWM_OUT = 12
DHT_PIN = 17

def spin_fan():
    t_dif = cur_temp - goal_temp

    # if (cur_temp > prev_temp - 0.5 and cur_temp < prev_temp + 0.5):
    #     return
    # if t_dif < 0:
    #     lgpio.tx_pwm(h_pwm, PWM_OUT, 0, 0)
    # elif t_dif < 2:
    #     lgpio.tx_pwm(h_pwm, PWM_OUT, 10000, 50)
    # elif t_dif < 4:
    #     lgpio.tx_pwm(h_pwm, PWM_OUT, 10000, 75)
    # else:
    #     lgpio.tx_pwm(h_pwm, PWM_OUT, 10000, 100) 

    #For LED testing
    if t_dif < 0:
        lgpio.tx_pwm(h_pwm, PWM_OUT, 0, 0)
    elif t_dif < 2:
        lgpio.tx_pwm(h_pwm, PWM_OUT, 1, 50)
    elif t_dif < 4:
        lgpio.tx_pwm(h_pwm, PWM_OUT, 2, 50)
    else:
        lgpio.tx_pwm(h_pwm, PWM_OUT, 10, 50) 

def display_lcd():
    lcd.clear()
    lcd.text('Current ' + str(cur_temp), 1)
    lcd.text(enable + ': ' + str(goal_temp), 2)

def read_sensor():
    global cur_temp

    #take average of 3 temp readings for accuracy
    avgTemp = 0
    try:
        for i in range(3):
            while dht.readDHT11Once() != dht.DHTLIB_OK:
               print("Invalid temp reading")
               sleep(0.5)
            avgTemp += dht.temperature
            sleep(0.1)
    except RuntimeError:
        print("Temperature check failed")

    #calculate average
    cur_temp = avgTemp/3

def do_stuff():
    global cur_temp

    while enable:
        read_sensor()
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
    lgpio.gpio_write(h_pwm, PWM_OUT, 0)
    lgpio.gpio_free(h_pwm, PWM_OUT)
    #lcd.clear()


def init_fan():
    global h_pwm
    h_pwm = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h_pwm, PWM_OUT)

def init_lcd():
    global lcd
    lcd = LCD(width=16, rows=2) #instantiate lcd variable
    lcd.clear()

def init_dht():
    global dht
    dht = DHT.DHT(DHT_PIN)

def init():
    global doc_root, goal_temp, cur_temp
    doc_root = os.path.dirname(__file__)
    with open(doc_root + "/goal_temp.txt","r") as f:
        goal_temp = float(f.read())
    cur_temp = 30.1
    init_fan()
    #init_lcd()
    init_dht()
    start()

if __name__ == "__main__":
    print("temp")