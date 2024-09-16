import spacy
from spacy.matcher import Matcher
from soap_requests import update_xml_with_new_number, send_soap_request, check_response_success, create_subscriber_xml, add_moh_xml_string
import re

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Initialize the Matcher with the shared vocabulary
matcher = Matcher(nlp.vocab)

# Define a more flexible pattern to match:
pattern_subscriber_create = [
    {"LOWER": "create"},       # Matches "create"
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": "subscriber"},   # Matches "subscriber"
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": "number"},       # Matches "number"
    {"IS_ALPHA": True, "OP": "*"},
    {"IS_DIGIT": True, "LENGTH": 10}  # Matches exactly 12-digit number
]

pattern_add_service_csta = [
    {"LOWER": "service"},            # Matches the word "service"
    {"LOWER": "csta"},               # Matches specifically "csta"
    {"IS_ALPHA": True, "OP": "*"},   # Allows for any words in between
    {"IS_DIGIT": True, "LENGTH": 12}  # Matches exactly 12-digit DN number
]

# Add the pattern to the matcher
matcher.add("SUBSCRIBER_CREATE", [pattern_subscriber_create])
matcher.add("FEATURE_ADD", [pattern_add_service_csta])

# Process the text
doc = nlp("I want to create a new subscriber with number 6867110001")
#doc = nlp("I want to add the service csta to the dn 302103181020")
#doc = nlp("I want to add the service csta ")


# Apply the matcher to the doc
matches = matcher(doc)

# Function to extract 12-digit number from the text
def extract_number(text):
    match = re.search(r'\b\d{10}\b', text)
    if match:
        return match.group(0)  # Returns the 12-digit number
    return None

# Check if any matches were found and print the match details
if matches:
    print(f"Found {len(matches)} match(es):")
    for match_id, start, end in matches:
        match_name = nlp.vocab.strings[match_id]  # Get the string name of the match
        matched_span = doc[start:end].text        # Get the text that was matched
        new_number = extract_number(matched_span)
        # Check if the pattern is 'SUBSCRIBER_CREATE' or 'FEATURE_ADD'
        if match_name == "SUBSCRIBER_CREATE":
            print(f"Matched pattern: SUBSCRIBER_CREATE, Span: {matched_span}")
            updated_create_subscriber_xml = update_xml_with_new_number(create_subscriber_xml, 'DeviceDn', new_number)
            create_subscriber_response = send_soap_request(updated_create_subscriber_xml)
            check_response_success(create_subscriber_response)
        elif match_name == "FEATURE_ADD":
            print(f"Matched pattern: FEATURE_ADD, Span: {matched_span}")
            updated_add_moh_xml = update_xml_with_new_number(add_moh_xml_string, 'DeviceDn', new_number)
            add_moh_response = send_soap_request(updated_add_moh_xml)
            check_response_success(add_moh_response)
        else:
            print(f"Other match: {match_name}, Span: {matched_span}")
else:
    print("No matches found.")