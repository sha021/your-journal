
import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    return 0


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
    print_result(annotations)


def analyzeText(result):
    analyze(result)

# from google.cloud import language
# from google.cloud.language import enums
# from google.cloud.language import types
# import re


# def print_result(annotations):
#     score = annotations.document_sentiment.score
#     magnitude = annotations.document_sentiment.magnitude

#     for index, sentence in enumerate(annotations.sentences):
#         sentence_sentiment = sentence.sentiment.score
#         print(sentence)
#         print('Sentence {} has a sentiment score of {}'.format(
#             index, sentence_sentiment))

#     print('Overall Sentiment: score of {} with magnitude of {}'.format(
#         score, magnitude))
#     return 0


# def analyzeText(result):
#     # Instantiates a client
#     client = language.LanguageServiceClient()

#     # The text to analyze
#     # document = types.Document(
#     #     content=result,
#     #     type=enums.Document.Type.PLAIN_TEXT)

#     # Detects the sentiment of the text
#     score = 0
#     index = 0
#     text = result.rstrip('\n')
#     s = re.split('[\r\n]+', text)
#     for line in s:
#         document = types.Document(
#             content=line,
#             type=enums.Document.Type.PLAIN_TEXT)

#         sentiment = client.analyze_sentiment(document=document).document_sentiment

#         print('Text: {}'.format(line))
#         print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
    # print('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))