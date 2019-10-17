# Web streaming from PiCamera and displaying Sense Hat values on a seperate pop up in real time
# Displays the values from the Sense Hat on a table underneath
# Source code from the official PiCamera package

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import data_logging as DataLogging
import math

class DisplayData:
    def __init__(self):
        self.senseHat = DataLogging()
        info = senseHat.get_sense_data()
        acceleration = math.sqrt(info[8]**2 + info[9]**2 + info[10]**2) * 9.81 #Converting Gs to m/s^2
        self.data = """
                    <html>
                      <head>
                        <title>Raspberry Pi - Emergency Vehicle</title>
                        <script type="text/javascript">
                          window.onload = startInterval;

                          function startInterval()
                          {
                            setInterval("startTime();",1000);
                          }

                          function startTime()
                          {
                            document.getElementById('table').innerHTML = document.getElementById('table').innerHTML;
                          }
                        </script>
                        <style>
                          table {
                            font-family: arial, sans-serif;
                            border-collapse: collapse;
                            width: 100%;
                          }

                          td, th {
                            border: 1px solid #dddddd;
                            text-align: left;
                            padding: 8px;
                          }

                          tr:nth-child(even) {
                            background-color: #dddddd;
                          }
                        </style>
                      </head>
                      <body>
                        <center><h1>Raspberry Pi - Emergency Vehicle</h1></center>
                        <h2>Raspberry Pi - Sensor Information</h2>
                        <center><img src="stream.mjpg" width="640" height="480"></center>
                        <div id="table">
                        <table>
                          <tr>
                            <th>Information</th>
                            <th>Values</th>
                          </tr>
                          <tr>
                            <td>Temperature (°C)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Pressure (mbar)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Humidity (%rH)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Yaw (°)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Pitch (°)</td>
                            <td>d</td>
                          </tr>
                          <tr>
                            <td>Roll (°)</td>
                            <td>%f</td>
                          </tr>
                            <tr>
                            <td>North (°)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Acceleration (m/s<sup>2</sup>)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Angular velocity - x (rads/s)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Angular velocity - y (rads/s)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Angular velocity - z (rads/s)</td>
                            <td>%f</td>
                          </tr>
                        </table>
                        </div>
                      </body>
                    </html>
                    """ %(info[1], info[2], info[3], info[4], info[5], info[6], info[7], acceleration, info[11], info[12], info[13])  

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            pageContent = DisplayData()
            content = pageContent.data.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))      
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
