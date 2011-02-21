import os
import sys
import site

# Reordering the path code from http://code.google.com/p/modwsgi/wiki/VirtualEnvironments

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Look for Virtual Envs
if os.environ.has_key("VIRTUAL_ENV"):
    env_path = os.environ["VIRTUAL_ENV"]
if os.environ.has_key("WORKON_HOME"):
    env_path = os.path.join(os.environ["WORKON_HOME"], $(project))
else:
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../env"))

# Add our Virtual Env
site.addsitedir(os.path.join(
    env_path,
    "lib/python%s/site-packages" % sys.version[:3]
))

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path 

#redirecting stdout to stderr cuz geopy uses print statements
sys.stdout = sys.stderr

# Discover our settings file
if not os.environ.has_key("DJANGO_SETTINGS_MODULE"):
    if not os.environ.has_key("DEPLOYMENT_TARGET"):
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
    else:
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.%s.settings" % os.environ["DEPLOYMENT_TARGET"]

# Fire up the WSGI
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

