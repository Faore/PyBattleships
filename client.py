import http.client, sys, urllib.parse

ip = sys.argv[1]
port = sys.argv[2]
x = sys.argv[3]
y = sys.argv[4]
print(ip)
hit = 0
sink = 0

params = urllib.parse.urlencode({'x': x, 'y': y})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = http.client.HTTPConnection(ip, port)
conn.request("POST", "", params, headers)
response = conn.getresponse()
print(response.status, response.reason)
results = str(response.read())
for letter in results:
    if letter == '1':
        print("Hit!")
    if letter == '0':
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


conn.close()