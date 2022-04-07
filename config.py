
class Config:
    pass

class RaspberryPi(Config):
    broker = "192.168.0.33"

class Development(Config):
    broker = "localhost"
