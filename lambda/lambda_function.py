# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# import pandas as pd
import csv
import requests
import io
import calendar
from io import StringIO
from datetime import datetime


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("request was received")
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome,to Zodiac Match. Would you like to know your zodiac Sign?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


def read_csv_from_string(csv_string):
    reader = csv.DictReader(StringIO(csv_string))
    return [row for row in reader]


def find_zodiac(zodiac_data, month, day):
    month = month.lower().capitalize()
    date_str = f"{month} {day}"
    # Convert input date string to datetime object
    input_date = datetime.strptime(date_str, '%B %d')

    for zodiac in zodiac_data:
        zodiac['Start'] = datetime.strptime(zodiac['Start'], '%B %d')
        zodiac['End'] = datetime.strptime(zodiac['End'], '%B %d')

    for zodiac in zodiac_data:
        start_date = zodiac['Start'].replace(year=input_date.year)  # Set the year of start date to match input year
        end_date = zodiac['End'].replace(year=input_date.year)  # Set the year of end date to match input year
        if start_date <= input_date <= end_date:
            return zodiac['Zodiac']

    return "No matching zodiac found"


class CaptureZodiacSignIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CaptureZodiacSignIntent")(handler_input)

    def filter(self, X):
        date = X.splitO
        month = date[0]
        month_as_index = list(calendar.month_abbr).index(month[:3].title)
        day = int(date[1])
        return (month_as_index, day)

    def handle(self, handler_input):
        print("Requesto received inside CaptureZodiacSignIntentHandler handle ")
        slots = handler_input.request_envelope.request.intent.slots
        year = slots["year"].value
        month = slots["month"].value
        day = slots["day"].value  # ENTER YOUR URL HERE
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJ9nFnQQDNrp6KfitFixbAIzvIF98EyY9jmilF74AZmRanJK3HQtHY33ObX8I77w/pub?gid=1653297855&single=true&output=csv"
        csv_content = requests.get(url).content
        print(csv_content)
        # Example data
        print("before csv data")
        data = read_csv_from_string(csv_content.decode('utf-8'))
        print("got data")

        zodiac = find_zodiac(data, month, day)
        # df = pd.read_csv(io.StringlO(csv_content.decode('utf-8')))
        # zodiac = ''
        # month_as_index = list(calendar.month_abbr).index(month[:3].title)
        # ust_dob = (month_as_index, int(day))
        # for index, row in df.iterrows:
        #     if self.filter(row['Start']) <= ust_dob <= self.filter(row['End']):
        #         zodiac = row['Zodiac']
        speak_output = 'I see you were born on the {day} of {month} {year},which means that your zodiac sign will be {zodiac}'.format(
            month=month, day=day, year=year, zodiac=zodiac)

        return (handler_input.response_builder.speak(speak_output).response)


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureZodiacSignIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()