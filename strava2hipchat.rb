##!/usr/bin/ruby

##
# Script to pull activities from Stava and send to Hipchat
#
##

require 'rubygems'
require 'hipchat'
require 'json'
require 'pp'
require 'strava/api/v3'

#
# Object to hold the strava activities
class StavaActivity
	attr_accessor :id, :athlete, :city, :activity_name, :type, :start_time, :time, :distance
end

#
# Object to take strava activities and send to hipchat
class Strava2HipChat

	attr_accessor :strava_key, :hipchat_key
	attr_reader :strava_activities

	def initialize(strava_key, hipchat_key, hipchat_room, hipchat_username)
		#
		# Initialize the keys and stuff
		@strava_key = strava_key
		@hipchat_key = hipchat_key
		@hipchat_room = hipchat_room
		@hipchat_username = hipchat_username

		#
		# Cache file
		@cache_file = "strava.cache"

		#
		# Get the latest strava activities
		@strava_client = Strava::Api::V3::Client.new(:access_token => @strava_key)
		@strava_activities = []
                @strava_client.list_friends_activities.each do |activity|
                        a = StavaActivity.new
                        a.id = activity['id']
                        a.athlete = activity['athlete']['firstname'] + " " + activity['athlete']['lastname']
                        a.city = activity['city']
                        a.activity_name = activity['name']
                        a.type = activity['type']
                        a.start_time = activity['start_time']
                        a.time = activity['moving_time']
                        a.distance = activity['distance']
                        @strava_activities.push(a)
                end

		#
		# Create the hipchat client
		#
		@hipchat_client = HipChat::Client.new(@hipchat_key)

		return 0
	end

	def send2hipchat()
		
		#
		# Check each activity from strava
		@strava_activities.each do |activity|
			#
			# if the activity hasn't been seen before
			if ! File.read(@cache_file).include?(activity.id.to_s)
				#
				# Create the text to send
				output_str = "#{activity.athlete} just #{activity.type} #{(activity.distance / 1000).round(2)}km in #{activity.time / 60} minutes!".gsub('Run','ran').gsub('Ride', 'rode').gsub('Swim','swam')
				#
				# Sent to HipChat
				@hipchat_client[@hipchat_room].send(@hipchat_username, output_str, :color => 'yellow')
				#
				# Record the ID
				strava_cache = File.new(@cache_file,"a")		
				strava_cache << activity.id.to_s + "\n"
				strava_cache.close()
			end
		end

	end
end


#
# Main 

#
# Api Keys and Usernames from config file
conf_file = File.read("strava2hipchat.conf")
conf = JSON.parse(conf_file)

#
# Create the Strava2HipChat and send
Strava2HipChat.new(conf["strava_key"], conf["hipchat_key"], conf["hipchat_room"], conf["hipchat_user"]).send2hipchat()

