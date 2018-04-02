from modes.rainbow import *
x = Rainbow()
while True:
    print("NOOTS")
    image = ROBOT.take_picture()
    x.ball_aligned(image, "rainbow_blue")

