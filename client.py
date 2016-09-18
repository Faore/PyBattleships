import http.client, sys, urllib.parse

ip = sys.argv[1]
port = sys.argv[2]
x = int(sys.argv[3])
y = int(sys.argv[4])
print(ip)
print("Please be patient! Sometimes the requests can take a long time. Just wait until the console prompt comes back.")
hit = 0
sink = 0
f = open("clientData")
selfPort = int(f.readline())

params = urllib.parse.urlencode({'x': x, 'y': y})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = http.client.HTTPConnection(ip, port)
conn.request("POST", "", params, headers)
response = conn.getresponse()
print(response.status, response.reason)
results = str(response.read())
for letter in results:
    if letter == '1':
        params = urllib.parse.urlencode({'x': x, 'y': y, 'hit': '1'})
        print("Hit!")
    if letter == '0':
        params = urllib.parse.urlencode({'x': x, 'y': y, 'hit': '0'})
        print("Miss :(")
    if letter == 'C':
        print("You sunk my Carrier")
    if letter == 'B':
        print("You sunk my Battleship")
    if letter == 'R':
        print("You sunk my Cruiser")
    if letter == 'S':
        print("You sunk my Submarine")
    if letter == 'D':
        print("You sunk my Destroyer")

conn = http.client.HTTPConnection('localhost', selfPort)
conn.request("POST", "/self", params, headers)
conn.close()
