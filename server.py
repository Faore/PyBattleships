from bottle import Bottle, get, run, request, response
from sys import argv
from urllib import parse

if len(argv) != 3:
    print("Invalid arguments: port, board")
    exit()

port = argv[1]
board = argv[2]

f = open(board)

cf = open('clientData', 'w+')
cf.write(port)
cf.close()

grid = []

oppGrid = []
for i in range(0, 10):
    oppGrid.append([])
    for j in range(0, 10):
        oppGrid[i].append('_')

for i in range(0, 10):
    line = f.readline().strip('\n')
    grid.append([])
    for letter in line:
        grid[i].append(letter)

app = Bottle()


@app.post('/')
def process_action():
    #Check if x and y exist
    try:
        x = request.POST['x']
        y = request.POST['y']
    except KeyError:
        response.status = 400
        return
    #Check if x is an int
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        response.status = 400
        return
    # Check if x is out of bounds
    if x >= 10 or y >= 10:
        response.status = 404
        return
    # Check the coordinate
    spot = grid[y][x]
    # Check for failure
    if spot == 'X' or spot == 'O':
        response.status = 410
        return
    if spot == '_':
        grid[y][x] = 'X'
        return parse.urlencode({'hit': 0})
    if spot != '_' and spot != 'O':
        grid[y][x] = 'O'
        # Check for a sink
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[j][i] == spot:
                    return parse.urlencode({'hit': 1})
        return parse.urlencode({'hit': 1, 'sink': spot})
@app.get('/own_board.html')
def show_board():
    content = "<h1>Board Contents</h1><table>"
    for i in range(0, len(grid)):
        content += str("<tr>")
        for j in range(0, len(grid[i])):
            content += str("<td>") + str(grid[i][j]) + str("</td>")
        content += str("</tr>")
    content += str("</table>")
    return content

@app.post('/self')
def update_opponent():
    # Check if x and y exist
    try:
        x = request.POST['x']
        y = request.POST['y']
        hit = request.POST['hit']
    except KeyError:
        response.status = 400
        return
    # Check if x is an int
    try:
        x = int(x)
        y = int(y)
        hit = int(hit)
    except ValueError:
        response.status = 400
        return
    # Check if x is out of bounds
    if x >= 10 or y >= 10:
        response.status = 404
        return
    # Check the coordinate
    if hit == 1:
        oppGrid[y][x] = 'O'
    else:
        oppGrid[y][x] = 'X'

    hitcount = 0
    # Check for a win
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if grid[j][i] == 'O':
                hitcount += 1

    if hitcount == 17:
        return parse.urlencode({'win': 1})
    else:
        return parse.urlencode({'win': 0})


@app.get('/opponent_board.html')
def opponent_board():
    content = "<h1>Opponent Board Contents</h1><table>"
    for i in range(0, len(oppGrid)):
        content += str("<tr>")
        for j in range(0, len(oppGrid[i])):
            content += str("<td>") + str(oppGrid[i][j]) + str("</td>")
        content += str("</tr>")
    content += str("</table>")
    return content


run(app, host='0.0.0.0', port=port)
