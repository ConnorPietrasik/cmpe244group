from threading import Thread
from time import sleep
import os
import lgpio

PWM_OUT = 12

# import lgpio
# def spin_motor(clockwise = True, delay = 0.004, step_max = 4096, con = [17, 27, 22, 23]):
#     #Half-step, so step_max = 4096 for full rotation
#     steps = [
#         0b1001,
#         0b1000,
#         0b1100,
#         0b0100,
#         0b0110,
#         0b0010,
#         0b0011,
#         0b0001
#     ]

#     h = lgpio.gpiochip_open(0)
#     lgpio.group_claim_output(h, con)

#     try:
#         step = 0
#         while command.empty():
#             lgpio.group_write(h, con[0], steps[step])
#             step = (step - 1) % 8 if clockwise else (step + 1) % 8
#             sleep(delay)
#     except Exception:
#         lgpio.group_write(h, con[0], 0)
#         lgpio.group_free(h, con[0])
#         lgpio.gpiochip_close(h)
#         exit(1)

def spin_fan():
    global prev_temp
    t_dif = cur_temp - goal_temp

    #Don't call pwm stuff if not a big difference
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
    prev_temp = cur_temp

def do_stuff():
    while enable:
        spin_fan
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
    global doc_root, goal_temp, cur_temp, h_pwm, prev_temp
    doc_root = os.path.dirname(__file__)
    with open(doc_root + "/goal_temp.txt","r") as f:
        goal_temp = f.read()
    cur_temp = 30.1
    h_pwm = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h_pwm, PWM_OUT)
    prev_temp = 0
    start()

if __name__ == "__main__":
    print("temp")