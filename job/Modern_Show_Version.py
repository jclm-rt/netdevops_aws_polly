# ----------------
# Copywrite
# ----------------
# Written by John Capobianco, March 2021 
# Copyright (c) 2021 John Capobianco

# ----------------
# Python
# ----------------
import sys
import os
import time
import logging
import json
import requests
import base64
from twilio.rest import Client
import boto3
from boto3 import Session
from rich import print
from rich import print as rprint


# ----------------
# Jinja2
# ----------------
from jinja2 import Environment, FileSystemLoader
template_dir = '../templates'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Import pyATS and the pyATS Library
# ----------------
#from genie.testbed import load
#from pyats.topology import loader
from pyats.log.utils import banner
from genie.conf import Genie
from pyats import aetest


# Get logger for script
log = logging.getLogger(__name__)

# ----------------
# Template sources
# ----------------
csv_template = env.get_template('show_version_csv.j2')
md_template = env.get_template('show_version_md.j2')
html_template = env.get_template('show_version_html.j2')
#discord_template = env.get_template('show_version_discord.j2')
#webex_template = env.get_template('show_version_webex.j2')
slack_template = env.get_template('show_version_slack.j2')
aws_tts_eng_template = env.get_template('show_version_aws_tts_english.j2')
aws_tts_esp_template = env.get_template('show_version_aws_tts_spanish.j2')

# ----------------
# Enable logger
# ----------------
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

# ----------------
# Load the testbed
# ----------------
log.info(banner("Loading testbed"))
testbed = Genie.init("../testbed/testbed0.yaml")
parsed_show_version = {}
log.info("\nPASS: Successfully loaded testbed '{}'\n".format(testbed.name))

# --------------------------
# Connect to device Devices
# Execute parser to show version
#--------------------------
log.info(banner(f"Connect to device {testbed.devices}"))
for device in testbed.devices:
    testbed.devices[device].connect()
    log.info(f"\nPASS: Successfully connected to device {testbed.devices[device]}\n")
    print(f"[blue]PASS: Successfully connected to {testbed.devices[device]}[/blue]")
    version_details = testbed.devices[device].parse("show version")
    log.info(banner("Executing parser to get show version and create documentation..."))
    parsed_show_version[device] = version_details

# ---------------------------------------
# Template Results
# ---------------------------------------
output_from_parsed_csv_template = csv_template.render(to_parse_version=parsed_show_version[device])
output_from_parsed_md_template = md_template.render(to_parse_version=parsed_show_version[device])
output_from_parsed_html_template = html_template.render(to_parse_version=parsed_show_version[device])
#output_from_parsed_discord_template = discord_template.render(to_parse_version=parsed_show_version['version'])
#output_from_parsed_webex_template = webex_template.render(to_parse_version=parsed_show_version['version'])
output_from_parsed_slack_template = slack_template.render(to_parse_version=parsed_show_version[device])
output_from_parsed_aws_tts_eng_template = aws_tts_eng_template.render(to_parse_version=parsed_show_version[device])
output_from_parsed_aws_tts_esp_template = aws_tts_esp_template.render(to_parse_version=parsed_show_version[device])


# ---------------------------------------
# Create Files
# ---------------------------------------
with open("../output/show_version_csv.csv", "w") as fh:
    fh.write(output_from_parsed_csv_template)

with open("../output/show_version_md.md", "w") as fh:
    fh.write(output_from_parsed_md_template)

with open("../output/show_version_html.html", "w") as fh:
    fh.write(output_from_parsed_html_template)

# ---------------------------------------
# #chatbots 
# ---------------------------------------
#discord_response = requests.post('https://discord.com/api/webhooks/{{ your webhook here }}', data=output_from_parsed_discord_template, headers={"Content-Type":"application/json"})
#print('The POST to Discord had a response code of ' + str(discord_response.status_code) + 'due to' + discord_response.reason)

#webex_response = requests.post('https://webexapis.com/v1/messages', data=output_from_parsed_webex_template, headers={"Content-Type":"application/json", "Authorization": "Bearer {{ your bearer token here }} "})
#print('The POST to WebEx had a response code of ' + str(webex_response.status_code) + 'due to' + webex_response.reason)
webhook_slack_var=os.environ["WEBHOOK_SLACK"]
slack_response = requests.post(webhook_slack_var, data=output_from_parsed_slack_template, headers={"Content-Type":"application/json"})
print('The POST to Slack had a response code of ' + str(slack_response.status_code) + 'due to' + slack_response.reason)

# ---------------------------------------
# #voicebots
# ---------------------------------------

# ----------------------------------
# Instantiates a client
# ----------------------------------
user_aws= os.environ["USER_AWS"]
session = Session(profile_name=user_aws)
polly_client = session.client("polly")

# ----------------
# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
# Select the type of audio file you want returned
# Build the voice request, select the voice id 
# voice engine ("standart")
# Set the text input to be synthesized
# ----------------

response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = output_from_parsed_aws_tts_eng_template,
                Engine = 'standard')

file = open('../output/show_version_aws_tts_eng.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()

response = polly_client.synthesize_speech(VoiceId='Lucia',
                OutputFormat='mp3', 
                Text = output_from_parsed_aws_tts_esp_template,
                Engine = 'standard')

file = open('../output/show_version_aws_tts_esp.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()

# ---------------------------------------
# #phonebots
# ---------------------------------------

# ---------------------------------------
# Twilio
# ---------------------------------------

# ---------------------------------------
# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
# ---------------------------------------

account_sid = os.environ["TWILIO_ID"]
auth_token = os.environ["TWILIO_TOKEN"]

client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='{{ MP3 File location }}',
                        to='{{ number to call }}',
                        from_='{{ number calling from }}'
                    )
rprint(call.sid)

#twiml='<Response><Say>Ahoy, World!</Say></Response>',
#url='http://demo.twilio.com/docs/voice.xml',