#!/usr/bin/python

##
# Script to pull activities from Stava and send to Hipchat
#
##

import json

#
# Get the conf from JSON file
conf_file = open('strava2hipchat.conf')
config = json.load(conf_file)
conf_file.close()

print """
strava_key: %s
hipchat_key: %s
hipchat_room: %s
hipchat_user: %s
""" % (config["strava_key"], config["hipchat_key"], config["hipchat_room"], config["hipchat_user"])