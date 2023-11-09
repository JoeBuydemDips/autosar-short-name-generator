import pandas as pd
# import os, openai
from fuzzywuzzy import process
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv())


# openai.api_key  = os.getenv('OPENAI_API_KEY')


def long_name_to_short_name(user_input, data_frame):
    # user_input = input("Enter keyword(s) separated by space: ").lower()
    user_input = user_input.lower()
    keywords = user_input.split()
    df = data_frame

    # Lists to hold found abbreviations and keywords with no matches
    abbreviation_list = []
    no_match_list = []

    # Loop through each user-entered keyword to find abbreviations
    for keyword in keywords:
        # Use DataFrame filtering to find matching abbreviation
        abbreviation_series = df[df['Keyword'].str.lower() == keyword]['Abbreviation']
        
        # If abbreviation found, append to abbreviation_list
        if not abbreviation_series.empty:
            abbreviation_list.append(abbreviation_series.iloc[0])
        else:
            # Otherwise, add keyword to no_match_list
            no_match_list.append(keyword.title())

    # Output results
    if no_match_list:
        # print(f"No abbreviation found for the following keyword(s): {', '.join(no_match_list)}")
        result = "Invalid Autosar Long Name"
        result += f"Consider changing the following keyword(s): {', '.join(no_match_list)}"
        
        # For each keyword with no match, get and print GPT-3 suggestions
        for keyword in no_match_list:
            suggestions = get_similar_keywords(keyword, df)
            # suggestions = find_closest_match(keyword, df)
            # suggestions = get_suggestions(keyword, df)
            # print(f"Suggestions for {keyword}: {suggestions}")
            result += f"\nSuggestions for {keyword}: {suggestions.title()}"
    elif abbreviation_list:
        # If all abbreviations found, output concatenated result
        result = "".join(abbreviation_list)
        result = f"\n{result}\n"
        # print(f"Short Name: {result}")
        # result = f"{result}"

    
    return result

# Function to get GPT-3 suggestions for a given keyword and find closest matches in the DataFrame
# Function to get GPT-3 suggestions based on the DataFrame content
# def get_gpt3_suggestions(keyword, data_frame, num_suggestions=2):
#     keyword_list = data_frame['Keyword'].tolist()
#     keyword_str = ', '.join(keyword_list)

#     prompt = f"The list of Keywords includes: {keyword_str}. List 3 keywords similar to '{keyword}'?"

#     # Call the GPT-3.5-turbo API
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant. Your response should be a list of keywords."},
#             {"role": "user", "content": prompt}
#         ]
#     )

#     # Extract and process the suggestions
#     suggested_keywords = response['choices'][0]['message']['content'].strip().split(', ')
#     print(suggested_keywords)

#     # Use fuzzy matching to find the closest matches from the DataFrame
#     closest_matches = process.extractBests(keyword, keyword_list + suggested_keywords, limit=num_suggestions)

#     # Filter the closest matches to only include those present in the DataFrame's Keyword list
#     filtered_matches = [match for match in closest_matches if match[0] in keyword_list]

#     return [match[0] for match in filtered_matches]
# def get_suggestions(keyword, df):
#     # Query GPT-3 to get suggestions (Make sure you have your API key properly set up)
#     keyword_list = df['Keyword'].tolist()
#     keyword_str = ', '.join(keyword_list)
#     prompt = f"This is a list of keywords: {keyword_str}. Suggest a singular form or a typo correction for the keyword: '{keyword}' from the list of keywords."
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # replace with your desired engine
#         prompt=prompt,
#         max_tokens=3
#     )
#     suggestion = response.choices[0].text.strip()  # This will be your suggestion
#     return suggestion


# Function to find similar matches in the DataFrame
def get_similar_keywords(keyword, data_frame, num_suggestions=3):
    # Extract the list of keywords from the DataFrame
    keyword_list = data_frame['Keyword'].tolist()

    if keyword == "min":
        return "Minimum"
    elif keyword == "max":
        return "Maximum"
    else:
    # Use fuzzy matching to find closest matches within the DataFrame
        closest_matches = process.extractBests(keyword, keyword_list, limit=num_suggestions)
    # print((closest_matches))
    
    if len(closest_matches) == 1:
        return closest_matches[0][0]
    else:
        results = [match[0] for match in closest_matches]
        return ', '.join(results)


# def find_closest_match(user_input, df):
#     # Add the user input to the keyword list for vectorization
#     keyword_list = df['Keyword'].tolist()
#     # keyword_str = ', '.join(keyword_list)
#     keywords_with_input = keyword_list + [user_input]
    
#     # Vectorize the words
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(keywords_with_input)
    
#     # Compute cosine similarity
#     cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
    
#     # Get the index of the most similar keyword
#     closest_idx = np.argmax(cosine_similarities[0][:-1])
    
#     return keyword_list[closest_idx]

def split_pascal_case(pascal_string):
    """
    Splits a PascalCase string into individual words.

    Parameters:
    pascal_string (str): The PascalCase string to be split.

    Returns:
    list: A list of strings that were concatenated in PascalCase format.
    """
    # List to store the split words
    words = []
    
    # The start index of the current word
    start_index = 0

    # Iterate over the string, character by character
    for i in range(1, len(pascal_string)):
        # If the current character is uppercase and not the start of the string
        if pascal_string[i].isupper() and i > start_index:
            # Append the word from the start index to the current position
            words.append(pascal_string[start_index:i])
            # Set the new start index
            start_index = i
    
    # Append the last word
    words.append(pascal_string[start_index:])

    return words

def short_name_to_long_name(pascal_string, df):
    """
    Takes a short name, and outputs the corresponding keywords for each abbreviation.

    Parameters:
    short_name: An autosar short name.
    df: A dataframe where key is keyword and value is abbreviation.

    Returns:
    str: A string containing the full keywords separated by spaces.
    """
    # Initialize an empty list to store keywords
    keywords = []
    abbreviations_not_found = []

    abbreviations_list = split_pascal_case(pascal_string)

    # Iterate through each abbreviation in the list
    for abbreviation in abbreviations_list:
        # Retrieve the keyword from the dictionary and append to the keywords list
        # If abbreviation not found, append the abbreviation itself
        keyword_row = df[df["Abbreviation"] == abbreviation]
            # If there's a match, return the "Keyword", otherwise return None
        if not keyword_row.empty:
            keywords.append(keyword_row["Keyword"].values[0])
        else:
            abbreviations_not_found.append(abbreviation)

    # Join the keywords with a space and return
    if abbreviations_not_found == []:
        return ' '.join(keywords)
    else:
        text = "Invalid Autosar Short Name!\n"
        text += "Consider changing the following Abbreviation(s): "
        text += (', '.join(abbreviations_not_found))
        return text


