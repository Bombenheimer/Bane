"""
MIT License

Copyright (c) 2024 Bombenheimer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# PYTHON STANDARD MODULES
import re
import socket
import argparse

# PYTHON MODULES ADDED VIA PIP
import requests

# MULTICAST ADDRESS, PORT AND MESSAGE FOR SSDP
SSDP_PORT: int = 1900
FILTER_ST: str = "roku:ecp"
SSDP_MULTICAST_ADDRESS: str = "239.255.255.250"
SSDP_MESSAGE: str = """M-SEARCH * HTTP/1.1
HOST: 239.255.255.250:1900
MAN: "ssdp:discover"
MX: 3
ST: ssdp:all
"""

# CREATE A UDP SOCKET
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.settimeout(5)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

# SEND THE M-SEARCH MESSAGE
sock.sendto(SSDP_MESSAGE.encode('utf-8'), (SSDP_MULTICAST_ADDRESS, SSDP_PORT))

# DISCOVER ROKU DEVICES ON LAN
def discover():
    try:
        print("DEVICE NAME                          LOCATION            HOST ID")
        while True:
            data, addr = sock.recvfrom(1024)
            response: str = data.decode('utf-8')
            if f"ST: {FILTER_ST}" in response:
                for line in response.split("\r\n"):
                    if line.startswith("LOCATION:"):
                        location = line.split(":", 1)[1].strip()
                        content = requests.get(location).text
                        matchingText: str = re.search(r'<friendlyName>(.*?)</friendlyName>', content)
                        if matchingText:
                            deviceName = matchingText.group(1)
                            deviceName = deviceName.replace('&quot;', '"')
                            matchingNum: str = re.search(r'http://192.168.1.(.*?):8060/', location)
                            if matchingNum:
                                hostID = matchingNum.group(1)
                                print(f"{deviceName}........{location}........{hostID}")
    except socket.timeout:
        return 0
    finally:
        sock.close()
    return 0

# PRESS UP BUTTON ON REMOTE
def keyup(deviceLocation, stepNumber):
    pass

# PRESS DOWN BUTTON ON REMOTE
def keydown(deviceLocation, stepNumber):
    pass

# PRESS LEFT BUTTON ON REMOTE
def keyleft(deviceLocation, stepNumber):
    pass

# PRESS RIGHT BUTTON ON REMOTE
def keyright(deviceLocation, stepNumber):
    pass

# PRESS HOME BUTTON ON REMOTE
def keyhome(deviceLocation):
    pass

# PRESS VOLUME DOWN BUTTON ON REMOTE
def voldown(deviceLocation, volumeNumber):
    pass

# PRESS VOLUME UP BUTTON ON REMOTE
def volup(deviceLocation, volumeNumber):
    pass

# PRESS VOLUME MUTE BUTTON ON REMOTE
def volmute(deviceLocation):
    pass

# PRESS BACK BUTTON ON REMOTE
def keyback(deviceLocation):
    pass

# PRESS SELECT / OK BUTTON ON REMOTE
def keyselect(deviceLocation):
    pass

# PRESS INFO / * BUTTON ON REMOTE
def keyinfo(deviceLocation):
    pass

# PRESS REWIND BUTTON ON REMOTE
def keyrewind(deviceLocation):
    pass

# PRESS FOWARDS BUTTON ON REMOTE
def keyfowards(deviceLocation):
    pass

# PRESS PAUSE / PLAY BUTTON ON REMOTE
def keypauseplay(deviceLocation):
    pass

# PRESS POWER BUTTON ON REMOTE
def keypower(deviceLocation):
    try:
        response = requests.post(f"http://{deviceLocation}:8060/keypress/PowerOff", data='')
        if (response.status_code == 202):
            requests.post(f"http://{deviceLocation}:8060/keypress/PowerOn", data='')

    except requests.exceptions.RequestException as ERROR_DESCRIPTOR:
        print(f"An error occured: {ERROR_DESCRIPTOR}")

    return 0

# MAIN FUNCTION
def main():
    # PROGRAM USAGE MESSAGE
    USAGE_TEXT: str = """
    Bane v1.0.0
        Flags:
            -h, --help              Show this help message
            -d, --discover          List all devices
            -i, --ip                IP Address of Roku Device
            -g, --gui               Start GUI
            -B, --back              Equivilent to pressing BACK on a remote
            -P, --power             Equivilent to pressing the POWER button on a remote
            -H, --home              Equivilent to pressing the HOME button on a remote
            -U, --up NUMBER         Equivilent to pressing the UP button on a remote a certain number of times
            -D, --down NUMBER       Equivilent to pressing the DOWN button on a remote a certain number of times
            -L, --left NUMBER       Equivilent to pressing the LEFT button on a remote a certain number of times
            -R, --right NUMBER      Equivilent to pressing the RIGHT button on a remote a certain number of times
            -O, --ok                Equivilent to pressing the OK button on a remote
            --return                Equivilent to pressing the RETURN button on a remote
            --vol-down NUMBER       Equivilent to pressing the VOLUME DOWN button on a remote
            --vol-up NUMBER         Equivilent to pressing the VOLUME UP button on a remote
            --vol-mute              Equivilent to pressing the VOLUME MUTE button on a remote
            --toggle-headphones     Equivilent to pressing the TOGGLE HEADPHONE AUDIO button on a remote
            --info                  Equivilent to pressing the INFO button on a remote
            --rewind                Equivilent to pressing the REWIND button on a remote
            --fowards               Equivilent to pressing the FOWARDS button on a remote
            --toggle-pause          Equivilent to pressing the TOGGLE PAUSE / PLAY button on a remote
    """
    # SET UP TOP LEVEL ARGUMENT PARSING
    parser = argparse.ArgumentParser(description='Bane v1.0.0', usage=USAGE_TEXT, formatter_class=argparse.RawTextHelpFormatter, add_help=False)

    # ADD ARGUMENTS
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message')
    parser.add_argument("-d", "--discover", action="store_true", help="List all devices")
    parser.add_argument("-i", "--ip", type=str, help="IP Address of Roku Device")
    parser.add_argument("-g", "--gui", action="store_true", help="Start GUI")
    parser.add_argument("-B", "--back", action="store_true", help="Equivalent to pressing BACK on a remote")
    parser.add_argument("-P", "--power", action="store_true", help="Equivalent to pressing the POWER button on a remote")
    parser.add_argument("-H", "--home", action="store_true", help="Equivalent to pressing the HOME button on a remote")
    parser.add_argument("-U", "--up", type=int, help="Equivalent to pressing the UP button on a remote a certain number of times")
    parser.add_argument("-D", "--down", type=int, help="Equivalent to pressing the DOWN button on a remote a certain number of times")
    parser.add_argument("-L", "--left", type=int, help="Equivalent to pressing the LEFT button on a remote a certain number of times")
    parser.add_argument("-R", "--right", type=int, help="Equivalent to pressing the RIGHT button on a remote a certain number of times")
    parser.add_argument("-O", "--ok", action="store_true", help="Equivalent to pressing the OK button on a remote")
    parser.add_argument("--return", action="store_true", help="Equivalent to pressing the RETURN button on a remote")
    parser.add_argument("--vol-down", type=int, help="Equivalent to pressing the VOLUME DOWN button on a remote")
    parser.add_argument("--vol-up", type=int, help="Equivalent to pressing the VOLUME UP button on a remote")
    parser.add_argument("--vol-mute", action="store_true", help="Equivalent to pressing the VOLUME MUTE button on a remote")
    parser.add_argument("--toggle-headphones", action="store_true", help="Equivalent to pressing the TOGGLE HEADPHONE AUDIO button on a remote")
    parser.add_argument("--info", action="store_true", help="Equivalent to pressing the INFO button on a remote")
    parser.add_argument("--rewind", action="store_true", help="Equivalent to pressing the REWIND button on a remote")
    parser.add_argument("--forward", action="store_true", help="Equivalent to pressing the FORWARD button on a remote")
    parser.add_argument("--toggle-pause", action="store_true", help="Equivalent to pressing the TOGGLE PAUSE / PLAY button on a remote")

    # PARSE THE ARGUMENTS
    args = parser.parse_args()

    # USE THE ARGUMENTS
    if args.discover:
        discover()
    elif args.help:
        print(USAGE_TEXT)
    elif args.power:
        if args.ip is not None:
            keypower(f"{args.ip}")
        else:
            return 1

    return 0

if __name__ == "__main__":
    main()
