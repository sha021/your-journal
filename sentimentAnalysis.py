
import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    sentimentValues = []
    sentiment = ''
    quote = ''
    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        # print('Sentence {} has a sentiment score of {}'.format(
        #     index, sentence_sentiment))
        sentimentValues.append((sentence.text.content, sentence_sentiment))
    # print('Overall Sentiment: score of {} with magnitude of {}'.format(
    #     score, magnitude))
    print(sentimentValues)
    sort_sentimentValues = sorted(sentimentValues, key=lambda x:x[1], reverse=True)
    print(sort_sentimentValues)

    if (score < -0.25): 
        print('You must be having a bad day. There will be better days.')
        sentiment = 'Very negative'
        quote = sort_sentimentValues[-1][0]
    elif (score < -0.15):
        print('You are feeling a little bit blue today.')
        sentiment = 'Somewhat negative'
        quote = sort_sentimentValues[-1][0]
    elif (score > 0.25):
        print('Hey, someone is happy today!')
        sentiment = 'Very positive'
        quote = sort_sentimentValues[0][0]
    elif (score > 0.15):
        print('There is always little happiness to find in every day.')
        sentiment = 'Somewhat positive'
        quote = sort_sentimentValues[0][0]
    else:
        print('Today was somewhat okay, I guess. Good ones and Bad ones. ')
        sentiment = 'Neutral'
        quote = sort_sentimentValues[0][0]
    print("++++++++", quote)
    tup = (sentiment, quote)
    return tup


def analyze(movie_review_filename):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    # with open(movie_review_filename, 'r') as review_file:
    #     # Instantiates a plain text document.
    #     content = review_file.read()

    document = types.Document(
        content=movie_review_filename,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Print the results
    return print_result(annotations)
