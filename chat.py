import os
import dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'privateKey.json'

DIALOGFLOW_PROJECT_ID = 'journal-wkwhjy'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'


print('\n======================= Your Journal ========================')
print('-------- Type "bye" if you want to close the Journal --------')

text_to_be_analyzed = ''
while text_to_be_analyzed != 'bye':
    text_to_be_analyzed = input('\nYou: ')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    # print('\nQuery text:', response.query_result.query_text)
    # print('Detected intent:', response.query_result.intent.display_name)
    # print('Detected intent confidence:', response.query_result.intent_detection_confidence)
    print('Your Journal:', response.query_result.fulfillment_text)
