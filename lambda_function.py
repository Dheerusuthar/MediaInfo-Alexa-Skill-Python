"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function
import requests
import json

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MovieInfoIntent":
        return get_movie_info(intent, session)
    elif intent_name == "RatingInfoIntent":
        return get_movie_info(intent, session)
    elif intent_name == "PlotInfoIntent":
        return get_movie_info(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the MediaInfo Alexa Skills. Please tell me movie name or tv series or tv series to get i m d b rating and pllot of movie." \
                    "If you want rating of the movie then say movie name or tv series or tv series followed by rating."\
                    "if you want to hear full plot of movie say movie name or tv series or tv series followed by plot"
    # If the user either does not reply to the welcome message or says something.
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me a movie name or tv show name to get information."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the MediaInfo Alexa Skills. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_movie_info(intent, session):
    '''this fuction get the movie plot and its rating through api'''
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    if 'movie' in intent['slots']:
        if intent['name'] == "MovieInfoIntent":
	    moviename = intent['slots']['movie']['value']
            jsonobj = get_json_data(moviename)
	    plot = jsonobj['Plot']
	    rating = jsonobj['imdbRating']
	    speech_output = "The Rating of \""+moviename+"\" is "+rating+". The plot is "+plot		
            reprompt_text = "You can say  moviename to get its i m d b rating and its plot"
        elif intent['name'] == "PlotInfoIntent":
	    moviename = intent['slots']['movie']['value']
	    plot="plot=full"
            jsonobj = get_json_data(moviename,plot)
	    plot = jsonobj['Plot']
	    speech_output = "The Plot of \""+moviename+"\" is "+plot		
            reprompt_text = "You can say  moviename to get its i m d b rating and its plot"
        elif intent['name'] == "RatingInfoIntent":
	    moviename = intent['slots']['movie']['value']
            jsonobj = get_json_data(moviename)
	    rating = jsonobj['imdbRating']
	    speech_output = "The Rating of \""+moviename+"\" is "+rating		
            reprompt_text = "You can say  moviename to get its i m d b rating and its plot"
        else:
            speech_output = "I'm not sure what your movie name or tv show name is. " \
                        "Please try again."
            reprompt_text = "I'm not sure what your query is. " \
                        "You can tell me your movie name or tv show name to get information"
    
    else:
        speech_output = "I'm not sure what your movie name or tv show name is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your query is. " \
                        "You can tell me your movie name or tv show name to get information"

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
		
		
def get_json_data(moviename,plot="plot=short"):
	output = (requests.get("http://www.omdbapi.com/?t="+moviename+"&y=&"+plot+"&r=json")).json()
	return output		
		
		
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
