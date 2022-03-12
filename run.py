#!/usr/bin/env python3

### IMPORTS ###
import logging

from hasts.server import Server, setup_server

### GLOBALS ###

### FUNCTIONS ###

### CLASSES ###

### MAIN ###
def main():
    # Get Environment Variables
    #debug_logging = os.getenv('DEBUG')
    debug_logging = True

    # Setup Logging
    log_format = "%(asctime)s:%(levelname)s:%(name)s.%(funcName)s: %(message)s"
    logging.basicConfig(
        format = log_format,
        level = (logging.DEBUG if debug_logging else logging.INFO)
    )

    # FIXME: For uWSGI and similar, the flask app should be at the top level.
    #        How should this be handled here?
    app = setup_server()
    main_server = Server(app)
    app.run(debug = True)

if __name__ == '__main__':
    main()
