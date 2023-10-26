from project import app

@app.route('/')
def index():
    return "Destination: Index"