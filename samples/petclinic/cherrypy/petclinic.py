"""
   Copyright 2006-2008 SpringSource (http://springsource.com), All Rights Reserved

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.       
"""


import cherrypy
import logging
import os
import noxml
from springpython.context import ApplicationContext
from springpython.security.context import SecurityContextHolder

if __name__ == '__main__':
    """This allows the script to be run as a tiny webserver, allowing quick testing and development.
    For more scalable performance, integration with Apache web server would be a good choice."""

    # This turns on debugging, so you can see everything Spring Python is doing in the background
    # while executing the sample application.

    logger = logging.getLogger("springpython")
    loggingLevel = logging.DEBUG
    logger.setLevel(loggingLevel)
    ch = logging.StreamHandler()
    ch.setLevel(loggingLevel)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") 
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    applicationContext = ApplicationContext(noxml.PetClinicClientAndServer())
    applicationContext.get_object("filterChainProxy")
    
    SecurityContextHolder.setStrategy(SecurityContextHolder.MODE_GLOBAL)
    SecurityContextHolder.getContext()
    
    conf = {'/': 	{"tools.staticdir.root": os.getcwd(),
                         "tools.sessions.on": True,
                         "tools.filterChainProxy.on": True},
            "/images": 	{"tools.staticdir.on": True,
                         "tools.staticdir.dir": "images"},
            "/html": 	{"tools.staticdir.on": True,
                      	 "tools.staticdir.dir": "html"}
            }

    cherrypy.tree.mount(applicationContext.get_object(name = "root"), '/', config=conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
