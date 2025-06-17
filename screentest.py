from smbus2 import SMBus
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

if __name__ == "__main__":
    address = 0x70
    channel_input = int(input("Enter the Channel number: "))
    # channel    76543210
    channel = 1 << channel_input
    # channel2 = 0b00000100  # channel 1

    bus = SMBus(1)
    bus.write_byte(address, channel)

    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30, 40), f"Channel: {channel_input}", fill="white")
