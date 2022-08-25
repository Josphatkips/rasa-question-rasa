# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# import  rasa.core.events.FollowupAction
from rasa_sdk.events import AllSlotsReset, FollowupAction, SlotSet
import requests

# url= "http://localhost:8000/api/"
url= "https://rq.roycehub.com/api/"
# urlimages= "http://localhost:8000/storage/images/"
urlimages= "https://rq.roycehub.com/storage/images/"
class ActionCustomQuestion(Action):

    def name(self) -> Text:
        return "action_submit_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("submit Form")
        myobj = {
            'question':tracker.get_slot('question'),
            'category':tracker.get_slot('category_id'),
             }

        x = requests.post(url+'query', json = myobj).json()
        if(x['response_code']==0):
            dispatcher.utter_message(text=x['message'])
            dispatcher.utter_message(response = "utter_other_question")
        else:
            dispatcher.utter_message(text=x['answer'])
            dispatcher.utter_message(response = "utter_other_question")


        return []

class ActionCustomQuestion(Action):

    def name(self) -> Text:
        return "action_custom_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
       
        myobj = {'question_id':tracker.get_slot('question_id') }

        x = requests.post(url+'question', json = myobj).json()
        dispatcher.utter_message(text=x['answer'])
        dispatcher.utter_message(response = "utter_other_question")

        # print(x['answer'])
        print("Please do follow up")

        return []
class ActionGetActions(Action):

    def name(self) -> Text:
        return "action_browse_questions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        myobj = {'category_id':tracker.get_slot('category_id') }

        # print("Category Id")
        print(tracker.get_slot('category_id'))

        x = requests.post(url+'category', json = myobj).json()

        # print(x['message'])
        
        # print(x['questions'])
        if(x['response_code']==0):
            dispatcher.utter_message(text=x['message'])
            return [FollowupAction('action_get_categories')]
        else:


            myelements=[]
            for xy in x['questions']:
                payload = "/custom_question{\"question_id\":\"" + str(xy['id']) + "\"}"
                newobj={
                        "title": xy['question'],
                        "subtitle": xy['question'],
                        "image_url": urlimages+xy['image'],
                        "buttons": [ 
                            {
                            "title": "Get Answer",
                            # "url": '',
                            "type": "postback",
                            "payload":payload
                            }
                        ]
                    }
                myelements.append(newobj)
                print(xy)
            message = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": myelements
                    
                    }
            }
            dispatcher.utter_message(attachment=message)


        return []
class ActionGetActions(Action):

    def name(self) -> Text:
        return "action_get_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        

       
        myobj = {'user_id':tracker.get_slot('user_id') }

        x = requests.post(url+'categories', json = myobj).json()

        print(tracker.get_slot('user_id'))

        if(x['response_code']==0):
            dispatcher.utter_message(text=x['message'])
        else:

            y= x['categories']

            buttons = []
            for z in y:
                # print(z['id'])
                payload = "/category{\"category_id\":\"" + str(z['id']) + "\"}"
                buttons.append(
                    {"title": "{}".format(z['name']), "payload": payload})
          
            dispatcher.utter_message(text="Choose a Category", buttons=buttons)

        return []
