from threading import Thread
from time import sleep

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

def do_stuff():
    while enable:
        print("Testing!")
        sleep(1)

def start():
    global enable, fan_thread
    enable = True
    fan_thread = Thread(target=do_stuff)
    fan_thread.start()

def init():
    global goal_temp, cur_temp
    with open("goal_temp.txt","r") as f:
        goal_temp = f.read()
    cur_temp = 30.1
    start()

