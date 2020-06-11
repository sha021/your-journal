import os
import dialogflow
import sentimentAnalysis 
import classification
from google.api_core.exceptions import InvalidArgument
from firebase import firebase
from datetime import datetime

BOT_NAME = 'Your Journal'
CLOSING = 'bye' #r'(\[gG\]ood\[\s-\]?)?\[bB\]ye.*'

def getUser():
    name = input('Please enter your name: ')
    if not name:
        return 'Guest'
    else:
        return name

def readJournal(firebaseApp, name):
    print(f'{BOT_NAME}: Sure! I\'ll start with the most recent page of your Journal.')
    print(f'{BOT_NAME}: Please say either "next" to continue, "delete" to remove, or "stop" to quit reading.')

    journal = firebaseApp.get(f'JournalEntries/{name}', '')
    for entry in reversed(journal.keys()):
        print('\nDate & Time:', journal[entry]['Date & Time'])
        print('Conversation:', )
        for sentence in journal[entry]['Conversation']:
            print('    ', sentence)
        # Backwards compatibility (before Sentiment Analysis & Quote of the Day were implemented)
        if 'Quote of the Day' in journal[entry]:
            print('Quote of the Day:', journal[entry]['Quote of the Day'])
        if 'Sentiment' in journal[entry]:
            print('Sentiment:', journal[entry]['Sentiment'])

        command = ''
        while True:
            command = input('\nYou: ')
            if command == 'next' or command == 'delete' or command == 'stop':
                break
            else:
                print(f'{BOT_NAME}: Please say either "next" to continue, "delete" to remove, or "stop" to quit reading.')
        if command == 'delete':
            firebaseApp.delete(f'JournalEntries/{name}', entry)
            print(f'{BOT_NAME}: The above Journal entry has been deleted.')
        elif command == 'stop':
            print(f'{BOT_NAME}: No problem! I\'ll close your Journal for now.')
            return
    
    print(f'{BOT_NAME}: That\'s every page of your journal! ')

def runDialog():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'privateKey.json'

    DIALOGFLOW_PROJECT_ID = 'journal-wkwhjy'
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = 'me'

    # Initialize Firebase Entry
    firebaseApp = firebase.FirebaseApplication('https://journal-wkwhjy.firebaseio.com/', None)
    timeStamp = datetime.now().strftime(f'%b-%d-%Y at %H:%M:%S')
    name = getUser()

    text_to_be_analyzed = ''
    conversation = []
    record = False

    print('\n======================= Your Journal ========================')
    print('-------- Type "bye" if you want to close the Journal --------')

    while text_to_be_analyzed != CLOSING:
        text_to_be_analyzed = input('\nYou: ')
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise
        # Start recording
        if (record == False and response.query_result.intent.display_name == 'Record Journal Entry'):
            print(f'{BOT_NAME}:', response.query_result.fulfillment_text)
            record = True
            continue
        # End session
        if (text_to_be_analyzed == CLOSING):
            print(f'{BOT_NAME}:', response.query_result.fulfillment_text)
            continue
        # Record statment
        if (record):
            if (text_to_be_analyzed[-1] != r'\[(\.\?\!\*\)\+\/)\]'):
                text_to_be_analyzed += '.'
            conversation.append(text_to_be_analyzed)
        # Visit entry
        if response.query_result.intent.display_name == 'Visit Journal Entry':
            readJournal(firebaseApp, name)
            continue
        # print()
        # print('Query text:', response.query_result.query_text)
        # print('Detected intent:', response.query_result.intent.display_name)
        # print('Detected intent confidence:', response.query_result.intent_detection_confidence)
        print(f'{BOT_NAME}:', response.query_result.fulfillment_text)

    if not len(conversation):
        print('\nConversation not recorded.')
        return
    else:
        print('\nConversation: ', conversation, sep='')

    text = ' '.join(conversation)
    sentimentAnalysis.analyzeText(text)
    # text2 = 'The Dog is a very faithful animal. Having a dog as a pet brings a moment of joy and excitement in our life. Almost everyone wants to have a cute dog in his home. Breeding a dog requires the best care to make him healthy and happy'
    classification.classify(text)
    
    entry = {
        'Date & Time': timeStamp,
        'Conversation': conversation,
    }
    result = firebaseApp.post(f'JournalEntries/{name}', entry)
    print('\nEntry:', result)

if __name__ == '__main__':
    runDialog() 
