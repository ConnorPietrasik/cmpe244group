from threading import Thread
from time import sleep
import os
import lgpio

PWM_OUT = 12

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

def do_stuff():
    while enable:
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

def init():
    global doc_root, goal_temp, cur_temp, h_pwm
    doc_root = os.path.dirname(__file__)
    with open(doc_root + "/goal_temp.txt","r") as f:
        goal_temp = float(f.read())
    cur_temp = 30.1
    h_pwm = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h_pwm, PWM_OUT)
    start()

if __name__ == "__main__":
    print("temp")