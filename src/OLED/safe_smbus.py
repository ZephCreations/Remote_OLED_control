from utils import is_pi

if is_pi():
    from smbus2 import SMBus
else:
    # Mock SMBus for Windows or non-rpi linux to avoid module not found error
    class SMBus:
        def __init__(self, bus):
            print(f"[Mock SMBus] Initialising fake bus {bus}")

        def write_byte(self, addr, value):
            print(f"[Mock SMBus] write_byte(addr={hex(addr)}, value={hex(value)})")