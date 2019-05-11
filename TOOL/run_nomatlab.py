#import matlab.engine
import os
import config
from app import app
#from controllers import mod_controllers
#from heidicontrollers_nomatlab import mod_heidicontrollers

from mod_auth.controllers import mod_controllers 
from mod_datacleaning.controllers import mod_datacleaning_controllers
from mod_heidi.controllers import mod_heidi_controllers
from mod_heidiPreprocessing.controllers import mod_heidiPreprocessing_controllers

#eng = matlab.engine.start_matlab()
app.register_blueprint(mod_controllers)
app.register_blueprint(mod_datacleaning_controllers)
app.register_blueprint(mod_heidi_controllers)
app.register_blueprint(mod_heidiPreprocessing_controllers)

os.system('mkdir ' + config.STATIC_DIR)
os.system('mkdir ' + config.UPLOADS_DIR)
#app.register_blueprint(mod_heidicontrollers)
print('App ready to run')

app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
