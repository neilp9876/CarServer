import time
from threading import Thread
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import lightControl

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_HEAD(s):
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
        def do_GET(s):
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write("<html><head><title>Title goes here.</title></head>")
                s.wfile.write("<body><p>Action has been taken...</p>")
                # If someone went to "http://something.somewhere.net/foo/bar/",
                # then s.path equals "/foo/bar/".
                s.wfile.write("<p>Action: %s</p>" % s.path)
                s.wfile.write("</body></html>")

                #response = "FAIL"

                if s.path == "/Headlight?ON":
                        print "Turning on HEADLIGHT"
                        lightControl.TurnLightsOn(lightControl.HEADLIGHT)
                        lightControl.TurnLightsOn(lightControl.TAILLIGHT)
                elif s.path == "/Headlight?OFF":
                        print "Turning off HEADLIGHT"
                        lightControl.TurnLightsOff(lightControl.HEADLIGHT)
                        lightControl.TurnLightsOff(lightControl.TAILLIGHT)
                elif s.path == "/Spotlight?ON":
                        print "Turning on SPOTLAMP"
                        lightControl.TurnLightsOn(lightControl.SPOTLIGHT)
                elif s.path == "/Spotlight?OFF":
                        print "Turning off SPOTLAMP"
                        lightControl.TurnLightsOff(lightControl.SPOTLIGHT)
                elif s.path == "/Backward?ON":
                        print "Turning on REVERSE"
                        lightControl.TurnLightsOn(lightControl.REVERSE_LIGHT)
                        lightControl.TurnLightsOff(lightControl.BRAKELIGHT)
                elif s.path == "/Backward?OFF":
                        print "Turning off REVERSE"
                        lightControl.TurnLightsOff(lightControl.REVERSE_LIGHT)
                        lightControl.TurnLightsOn(lightControl.BRAKELIGHT)
                elif s.path == "/Forward?ON":
                        lightControl.TurnLightsOff(lightControl.BRAKELIGHT)                        
                elif s.path == "/Forward?OFF":
                        lightControl.TurnLightsOn(lightControl.BRAKELIGHT)                        
                elif s.path == "/Left?ON":
                        print "Turning on LEFT"
                        lightControl.FlashLightsOn(lightControl.LEFT_INDICATOR)
                elif s.path == "/Left?OFF":
                        print "Turning off LEFT"
                        lightControl.FlashLightsOff(lightControl.LEFT_INDICATOR)
                elif s.path == "/Right?ON":
                        print "Turning on RIGHT"
                        lightControl.FlashLightsOn(lightControl.RIGHT_INDICATOR)
                elif s.path == "/Right?OFF":
                        print "Turning off RIGHT"
                        lightControl.FlashLightsOff(lightControl.RIGHT_INDICATOR)
                elif s.path == "/Hazards?ON":
                        print "Turning on HAZARDS"
                        lightControl.FlashLightsOn(lightControl.HAZARDS)
                elif s.path == "/Hazards?OFF":
                        print "Turning off HAZARDS"
                        lightControl.FlashLightsOff(lightControl.HAZARDS)
                elif s.path == "/Foglight?ON":
                        print "Turning on FOGLAMP"
                        lightControl.TurnLightsOn(lightControl.FOGLIGHT)
                elif s.path == "/Foglight?OFF":
                        print "Turning off FOGLAMP"
                        lightControl.TurnLightsOff(lightControl.FOGLIGHT)

                # SERVO CONTROL
                
                if s.path.startswith("/Accelerate"):
                        position = int(s.path[12])
                        print "MOVING FORWARD"
                        lightControl.Throttle(position)
                elif s.path.startswith("/Reverse"):
                        position = int(s.path[9])
                        position *= -1 # Reversing so negate
                        print "REVERSING"
                        lightControl.Throttle(position)                        
                        
                elif s.path.startswith("/Gear"):
                        # Read the gear position
                        gearPos = int(s.path[6])
                        print "Gear changing to - {}".format(gearPos)
                        lightControl.ChangeGear(gearPos)
                        
                elif s.path.startswith("/Steer"):
                        # Read the position of the steering wheel
                        direction = int(s.path[7])
                        lightControl.Steer(direction)

                print s.path


HOST, PORT = "0.0.0.0", 9997

if __name__ == '__main__':
        #Initialise the hardware
        lightControl.Initialise()
        
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((HOST, PORT), MyHandler)
        print time.asctime(), "Server Starts - %s:%s" % (HOST, PORT)
        try:
                httpd.serve_forever()
        except KeyboardInterrupt:
                pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (HOST, PORT)
