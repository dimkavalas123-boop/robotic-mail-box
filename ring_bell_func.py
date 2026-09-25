from time import sleep


def ring_bell_now(servo,num_rings = 2,time_delay = 0.15):
    
    from gpiozero import Servo

    servo = Servo(servo)

    if time_delay < 0.125:
        time_delay = 0.125

    if num_rings > 7:
        num_rings = 7
    elif num_rings < 1:
        num_rings = 1

    try:
        for _ in range(num_rings):
                servo.min()        
                sleep(time_delay)
                servo.max()  
                sleep(time_delay)

    except KeyboardInterrupt:
        servo.detach()   

    try:
        servo.detach()     
    except:
        pass

