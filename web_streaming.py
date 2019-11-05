# Web streaming from PiCamera and displaying Sense Hat values on a seperate pop up in real time
# Displays the values from the Sense Hat on a table underneath
# Source code from the official PiCamera package

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
from data_logging import DataLogging
import math


class PageData:
    def __init__(self):
        self.data = """
                    <html>
                      <head>
                      <script type="text/javascript">
                        var xmlhttp;
                        if (window.XMLHttpRequest) {  // code for IE7+, Firefox, Chrome, Opera, Safari
                          xmlhttp=new XMLHttpRequest();
                        }
                        else {                        // code for IE6, IE5
                          xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
                        }
                        function updateTable() {
                          xmlhttp.onreadystatechange=function() {
                            if (xmlhttp.readyState==4 && xmlhttp.status==200) {
                              document.getElementById("table").innerHTML=xmlhttp.responseText;
                            }
                          }
                          xmlhttp.open("GET","/sensor.html",true);
                          xmlhttp.send();
                          }
                        updateTable();
                        setInterval(updateTable, 1000);
                        </script>
                        <title>Raspberry Pi - Emergency Vehicle</title>
                      </head>
                      <body>
                        <center><h1>Raspberry Pi - Emergency Vehicle</h1></center>
                        <center><img src="stream.mjpg" width="640" height="480"></center>
                        <h2>Raspberry Pi - Sensor Information</h2>
                        <div id="table">
                        </div>
                      </body>
                    </html>
                    """
class DisplayData:
    def __init__(self):
        self.senseHat = DataLogging()
        info = self.senseHat.get_sense_data()
        acceleration = math.sqrt(info[8]**2 + info[9]**2 + info[10]**2) * 9.81 #Converting Gs to m/s^2
        self.data = """
                    <html>
                      <head>
                        <title>Raspberry Pi - Emergency Vehicle</title>
                        <style>
                          table {
                            font-family: arial, sans-serif;
                            border-collapse: collapse;
                            width: 100%%;
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
                            <td>Humidity (%%rH)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Yaw (°)</td>
                            <td>%f</td>
                          </tr>
                          <tr>
                            <td>Pitch (°)</td>
                            <td>%f</td>
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
                    """ %(float(info[1]), float(info[2]), float(info[3]), float(info[4]), float(info[5]), float(info[6]), float(info[7]), float(acceleration), float(info[11]), float(info[12]), float(info[13]))  

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
            pageContent = PageData()
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
        elif self.path == '/sensor.html':
            SensorInfo = DisplayData()
            content = SensorInfo.data.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
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
