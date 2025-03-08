from flask import *
from database import *
from public import public
from admin import admin
from police import police
from api import api
      

app = Flask(__name__)

app.secret_key="sdfvgb"

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(police)
app.register_blueprint(api)



app.run(debug=True,host="0.0.0.0",port=5037)

