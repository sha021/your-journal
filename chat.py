import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
import sentimentAnalysis 
import classification
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'privateKey.json'

DIALOGFLOW_PROJECT_ID = 'journal-wkwhjy'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

def journal():
    text_to_be_analyzed = ''
    conversation = ''
    record = 0

    print('\n======================= Your Journal ========================')
    print('-------- Type "bye" if you want to close the Journal --------\n')

    while text_to_be_analyzed != 'bye':
        text_to_be_analyzed = input('You: ')
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise
        if (record == False and response.query_result.intent.display_name == 'record'):
            print('\nYour Journal:', response.query_result.fulfillment_text)
            record = True
            continue
        if (text_to_be_analyzed == 'bye'):
            print('\nYour Journal:', response.query_result.fulfillment_text)
            continue
        if (record):
            if (text_to_be_analyzed[-1] != r'\[(\.\?\!\*\)\+\/)\]'):
                text_to_be_analyzed += '.'
            conversation += text_to_be_analyzed + '\n'
        # print('\nQuery text:', response.query_result.query_text)
        print('\nDetected intent:', response.query_result.intent.display_name)
        print('Detected intent confidence:', response.query_result.intent_detection_confidence)
        print('\nYour Journal:', response.query_result.fulfillment_text)

    print('\n', conversation, sep='')
    return conversation

if __name__ == '__main__':
    result = journal()
    text = result.replace("\n", " ")
    sentimentAnalysis.analyzeText(text)
    # text2 = 'The Dog is a very faithful animal. Having a dog as a pet brings a moment of joy and excitement in our life. Almost everyone wants to have a cute dog in his home. Breeding a dog requires the best care to make him healthy and happy'
    classification.classify(text)