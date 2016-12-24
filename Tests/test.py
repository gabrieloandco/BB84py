import time
ku = False

def UpdateKeyClock(delay):
    global ku
    def ukc():
        global ku
        if not ku:
            print "clock started: ku ="+ str(ku) 
            time.sleep(delay)
            ku = not ku
            print "clock finished: ku ="+ str(ku)
            return ku
        if ku:
             pass

    while True:
        ukc()


UpdateKeyClock(3)
