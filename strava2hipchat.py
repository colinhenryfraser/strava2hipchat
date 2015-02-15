#!/usr/bin/python

#
# Script to pull activities from Stava and send to Hipchat
#####

import json
from stravalib import Client, unithelper
import datetime

#
# Strava Parent Class
####
class Strava:

	#
	# Set the Strava key
	def __init__(self, strava_key):
		self.strava_key = strava_key
		#	
		# Ensure the cache file exists
		open('strava.cache', 'a').close()
		#
                # Get the last 10 Activies
                self.getStravaActivities(10)
		
				
	def getStravaActivities(self, limit=10):
		self.client = Client(access_token=self.strava_key)
		self.activities = self.client.get_friend_activities(limit)
		return self.activities

	def getStravaClient(self):
		return self.client
		
#
# Strava to Hipchat Class
####
class Strava2HipChat(Strava):

	def __init__(self, strava_key, hipchat_key, hipchat_room, hipchat_user="Strava"):
		#
		# HipChat Stuff
		self.hipchat_key = hipchat_key
		self.hipchat_room = hipchat_room
		self.hipchat_user = hipchat_user
		#
		# Strava Key
		Strava.__init__(self, strava_key)
	#
	# Send the Strava stuff to HipChat
	####
	def send(self):
		#
		# Each Activity...
		for activity in self.activities:
			#
			# Check if the activity has been seen already
			if str(activity.id) not in open('strava.cache').read():
				#
				# The details to send:
		        	athlete = activity.athlete
				athlete_firstname = self.client.get_athlete(athlete.id).firstname
				athlete_lastname = self.client.get_athlete(athlete.id).lastname
		        	athlete_name = "%s %s" % (athlete_firstname, athlete_lastname)
				date = activity.start_date_local
		        	distance = unithelper.miles(activity.distance)
		        	activity_name = activity.name
				time = activity.moving_time
				#
				# Form the message
				message = "New Strava Activity! %s -- %s -- %s in %s. Well done %s!" % (athlete_name, activity_name, distance, time, athlete_firstname)
				#
				# Send to HipChat
				print message
				#
				# Record the activity id in cache (don't know if cache is the right name for this)
				open('strava.cache','a').write(str(activity.id) + "\n")

#
# MAIN
####

#
# Get the config from JSON file:
config = json.load(open('strava2hipchat.conf'))

#
# Do the business
Strava2HipChat(config["strava_key"], config["hipchat_key"], config["hipchat_room"], config["hipchat_user"]).send()

