from bottle import get, post, request, run, Bottle



app = Bottle()

@post('')
def processAction():
    x = request.forms.get('x')
    y = request.forms.get('y')

run(app, host='0.0.0.0', port=)