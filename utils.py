import json


def filter_responses(data, threshold=0.75):
  """
  Filters the input data based on a score threshold.
  :param data: Dictionary containing 'results' key with a list of responses.
  :param threshold: Minimum score required to include a response.
  :return: Filtered data in the same format.
  """
  filtered_results = [item for item in data['results'] if item['score'] >= threshold]
  return {'results': filtered_results}