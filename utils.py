import json


def filter_results(json_data, score_threshold=0.70):
  """
  Filters the 'results' list in the given JSON data, returning only the
  'text' from entries with a 'score' greater than the specified threshold.

  Args:
    json_data: A JSON string containing the data (as provided in the problem).
    score_threshold: The minimum score for a result to be included.

  Returns:
    A list of strings, where each string is the 'text' from a result
    with a score above the threshold.  Returns an empty list if the input
    is invalid or no results meet the criteria.
  """
  try:
    data = json_data
    if "results" not in data or not isinstance(data["results"], list):
      print("Warning: 'results' key not found or is not a list in the JSON data.")
      return []

    filtered_texts = []
    for result in data["results"]:
      if "score" in result and isinstance(result["score"], (int, float)) and \
         "text" in result and isinstance(result["text"], str):
        if result["score"] > score_threshold:
          filtered_texts.append(result["text"])
      else:
        print(f"Warning: Invalid data format in result: {result}.  Skipping.")

    return filtered_texts

  except json.JSONDecodeError:
    print("Error: Invalid JSON format.")
    return []
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    return []