How to run team project code:
1. Use Raspberry Pi4B running Ubuntu 22.04
1. Download source code and necessary libraries (lgpio)
2. Ensure Raspberry Pi has internet access for ChatGPT
3. Connect DHT11 input/output to pin 17 and all VCC to 5v, all GND to GND
4. Connect chassis fan PWM to pin 12
5. Connect I2CLCD1602 to I2C bus 1, with:
	a. SDA at pin 3
	b. SCL at pin 5
6. Run "sudo python3 fan_web_control.py" in terminal
7. Open website, ip is given when you run fan_web_control.py
8. Adjust temperature as needed/wanted on site 