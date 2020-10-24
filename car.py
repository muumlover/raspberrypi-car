# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
from pyPS4Controller.controller import Controller


class Car():
    # 小车电机引脚定义
    IN1 = 20
    IN2 = 21
    IN3 = 19
    IN4 = 26
    ENA = 16
    ENB = 13

    def __init__(self):
        # 设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)

        # 忽略警告信息
        GPIO.setwarnings(False)

        # 电机引脚初始化操作
        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)

        # 设置pwm引脚和频率为2000hz
        self.pwm_ENA = GPIO.PWM(self.ENA, 2000)
        self.pwm_ENB = GPIO.PWM(self.ENB, 2000)
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

    def destory(self):
        self.pwm_ENA.stop()
        self.pwm_ENB.stop()
        GPIO.cleanup()

    def forward(self, speed=1):
        """
        小车前进
        """
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(speed)
        self.pwm_ENB.ChangeDutyCycle(speed)

    def back(self, speed=1):
        """
        小车后退
        """
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(speed)
        self.pwm_ENB.ChangeDutyCycle(speed)

    def left(self, speed=1):
        """
        小车左转
        """
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(speed)
        self.pwm_ENB.ChangeDutyCycle(speed)

    def right(self, speed=1):
        """
        小车右转
        """
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(speed)
        self.pwm_ENB.ChangeDutyCycle(speed)

    def spin_left(self, speed=1):
        """
        小车原地左转
        """
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(speed)
        self.pwm_ENB.ChangeDutyCycle(speed)

    def spin_right(self, speed=1):
        """
        小车原地右转
        """
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(speed)
        self.pwm_ENB.ChangeDutyCycle(speed)

    def stop(self):
        """
        小车停止
        """
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(0)
        self.pwm_ENB.ChangeDutyCycle(0)


class MyController(Controller):

    def __init__(self, car, **kwargs):
        Controller.__init__(self, **kwargs)
        self.car = car

    def on_L3_up(self, value):
        print("on_L3_up: {}".format(value))
        self.car.forward(int(value * 100 / -32768))

    def on_L3_down(self, value):
        print("on_L3_down: {}".format(value))
        self.car.back(int(value * 100 / 32768))

    def on_L3_left(self, value):
        print("on_L3_left: {}".format(value))
        self.car.spin_left(int(value * 100 / -32768))

    def on_L3_right(self, value):
        print("on_L3_right: {}".format(value))
        self.car.spin_right(int(value * 100 / 32768))

    def on_L3_x_at_rest(self):
        print("on_L3_x_at_rest")
        self.car.stop()

    def on_L3_y_at_rest(self):
        print("on_L3_y_at_rest")
        self.car.stop()


if __name__ == "__main__":
    car = Car()
    controller = MyController(car=car, interface="/dev/input/js0",
                              connecting_using_ds4drv=False)
    controller.listen()
