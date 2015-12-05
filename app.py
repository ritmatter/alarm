import os, sys
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

APPLICATION_ID = os.environ['ALARM_APPLICATION_ID']
REST_API_KEY = os.environ['ALARM_REST_API_KEY']

from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object as ParseObject

register(APPLICATION_ID, REST_API_KEY)

# ex: localhost:<PORT>/doorevent?opened=1
@app.route('/doorevent', methods=['POST'])
def add_door_event():
    doorEvent = ParseObject()
    opened = request.args.get('opened', '');
    if opened == '1':
        doorEvent.opened = True
    elif opened == '0':
        doorEvent.opened = False
    else:
        return 'Invalid request.'
    doorEvent.save()

    response = {}
    response['opened'] = doorEvent.opened
    response['createdAt'] = str(doorEvent.createdAt)
    return json.dumps(response)


if __name__ == '__main__':
    app.run(debug=True)
