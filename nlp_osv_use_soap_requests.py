import tkinter as tk
from tkinter import messagebox
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
    {"IS_DIGIT": True, "LENGTH": 10}  # Matches exactly 12-digit DN number
]

# Add the pattern to the matcher
matcher.add("SUBSCRIBER_CREATE", [pattern_subscriber_create])
matcher.add("FEATURE_ADD", [pattern_add_service_csta])

# Function to extract 12-digit number from the text
def extract_number(text):
    match = re.search(r'\b\d{10}\b', text)
    if match:
        return match.group(0)  # Returns the 12-digit number
    return None

# Function to process the input from the GUI
def process_input(user_input):
    # Process the input text with spaCy
    doc = nlp(user_input)
    

    # Apply the matcher to the doc
    matches = matcher(doc)

    # Check if any matches were found
    if matches:
        for match_id, start, end in matches:
            match_name = nlp.vocab.strings[match_id]  # Get the string name of the match
            matched_span = doc[start:end].text        # Get the text that was matched
            
            # Extract the number from the matched span or from the doc
            new_number = extract_number(matched_span) or extract_number(doc.text)
            
            if new_number:
                if match_name == "SUBSCRIBER_CREATE":
                    updated_create_subscriber_xml = update_xml_with_new_number(create_subscriber_xml, 'DeviceDn', new_number)
                    create_subscriber_response = send_soap_request(updated_create_subscriber_xml)
                    check_response_success(create_subscriber_response)
                    messagebox.showinfo("Success", "Subscriber created successfully!")
                elif match_name == "FEATURE_ADD":
                    updated_add_moh_xml = update_xml_with_new_number(add_moh_xml_string, 'DeviceDn', new_number)
                    add_moh_response = send_soap_request(updated_add_moh_xml)
                    check_response_success(add_moh_response)
                    messagebox.showinfo("Success", "CSTA service added successfully!")
            else:
                messagebox.showerror("Error", "No valid 12-digit number found.")
    else:
        messagebox.showerror("Error", "No matches found.")


# Create the main application window
def create_gui():
    # Create a new window
    root = tk.Tk()
    root.title("SOAP Request Input")

    # Create and configure a text entry box
    label = tk.Label(root, text="Enter command:")
    label.pack(pady=10)
    
    input_box = tk.Entry(root, width=50)
    input_box.pack(pady=10)

    # Function to get the input when the button is pressed
    def on_submit():
        user_input = input_box.get()
        process_input(user_input)

    # Create a button that triggers the on_submit function
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    # Run the application
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()