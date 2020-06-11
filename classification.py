import argparse
import io
import json
import os
from google.cloud import language
import numpy
import six

def classify(text, verbose=True):
    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)
    response = language_client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        result[category.name] = category.confidence

    # if verbose:
    #     print(text)
    #     for category in categories:
    #         print(u'=' * 20)
    #         print(u'{:<16}: {}'.format('category', category.name))
    #         print(u'{:<16}: {}'.format('confidence', category.confidence))
    summary = []
    for key in result.keys():
        summary.append(key)

    return summary
    
