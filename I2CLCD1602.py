"""
Author          -   Aidan Zastrow
Description     -   
I2CLCD thread that sets up a connections to an LCD8574 display and then
by default writes "User" and "message" to the 2 line display

Calling code would use it in such a way they call Update and the two
messages would change to what the calling code wanted them to be.

They are intended to be a user and the message associated with that 
user. Provided from a server of some sort.
"""
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import threading
from time import sleep


class PrintLCD(threading.Thread):
    """
    A subclass of threading.Thread 
    Prints out a message onto an LCD8574 screen every second
    Upon Deletion it will clear the LCD screen
    """
    def __init__(self, thread_watch : threading.Thread) -> None:
        """
        Inputs: threading.Thread - The thread that it watches to know when to stop running
        Outputs: None
        Inits the PrintLCD class with "User" for the first line and "Message" for the
        second line of the LCD screen
        Then inits the rest of the LCD screen specfics for the chip
        """
        super().__init__()
        self.thread_watch = thread_watch
        self.header = "User"
        self.message = "Message"
        self.PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        self.PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        try:
            mcp = PCF8574_GPIO(self.PCF8574_address)
        except:
            try:
                mcp = PCF8574_GPIO(self.PCF8574A_address)
            except:
                print ('I2C Address Error !')
                exit(1)

        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
    
    def update(self, header : str, message : str) -> None:
        """
        Inputs header : str - the first line to be output on the LCD screen
               message : str - the second line to be output on the LCD screen
        Ouputs None
        Allows for the message on the LCD screen to be changed
        """
        self.header = header
        self.message = message

    def run(self):
        """
        Initializes the LCD Screen the outputs the header and message
        runs until watched thread is no longer running
        """
        self.mcp.output(3,1)     # turn on LCD backlight
        self.lcd.begin(16,2)
        while self.thread_watch.is_alive():
            self.lcd.setCursor(0,0)  # set cursor position
            self.lcd.message(self.header + '\n')
            self.lcd.message(self.message)
            sleep(1)
        self.destroy()

    def destroy(self):
        """
        Clears the LCD screen
        """
        self.lcd.clear()
    

# Create PCF8574 GPIO adapter.

# Create LCD, passing in MCP GPIO adapter.
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

