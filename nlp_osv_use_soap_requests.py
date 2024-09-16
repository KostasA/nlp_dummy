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
    {"LOWER": "create"},       
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": "subscriber"},   
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": "number"},       
    {"IS_ALPHA": True, "OP": "*"},
    {"IS_DIGIT": True, "LENGTH": 10}  
]

pattern_add_service_csta = [
    {"LOWER": "service"},            
    {"LOWER": "csta"},               
    {"IS_ALPHA": True, "OP": "*"},   
    {"IS_DIGIT": True, "LENGTH": 12}  
]

# Add the pattern to the matcher
matcher.add("SUBSCRIBER_CREATE", [pattern_subscriber_create])
matcher.add("FEATURE_ADD", [pattern_add_service_csta])

# Function to extract 10-digit number from the text
def extract_number(text):
    match = re.search(r'\b\d{10}\b', text)
    if match:
        return match.group(0)  
    return None

# Function to validate phone number format
def validate_number_format(text):
    match = re.fullmatch(r'\d{10}', text)
    return bool(match)

# Function to process the input from the GUI
def process_input(user_input):
    doc = nlp(user_input)
    matches = matcher(doc)

    if matches:
        for match_id, start, end in matches:
            match_name = nlp.vocab.strings[match_id]  
            matched_span = doc[start:end].text        
            
            new_number = extract_number(matched_span) or extract_number(doc.text)
            
            if new_number:
                if match_name == "SUBSCRIBER_CREATE":
                    updated_create_subscriber_xml = update_xml_with_new_number(create_subscriber_xml, 'DeviceDn', new_number)
                    create_subscriber_response = send_soap_request(updated_create_subscriber_xml)
                    check_response_success(create_subscriber_response)
                    show_info("Subscriber created successfully!")
                elif match_name == "FEATURE_ADD":
                    updated_add_moh_xml = update_xml_with_new_number(add_moh_xml_string, 'DeviceDn', new_number)
                    add_moh_response = send_soap_request(updated_add_moh_xml)
                    check_response_success(add_moh_response)
                    show_info("CSTA service added successfully!")
            else:
                show_error("No valid 10-digit number found.")
    else:
        show_error("No matches found.")

def show_info(message):
    messagebox.showinfo("Information", message)

def show_error(message):
    messagebox.showerror("Error", message)

# Function to clear the placeholder text
def clear_placeholder(event):
    if input_box.get("1.0", tk.END).strip() == placeholder_text.strip():
        input_box.delete("1.0", tk.END)
        input_box.config(fg="black")

# Function to set the placeholder text if the box is empty
def set_placeholder(event):
    if not input_box.get("1.0", tk.END).strip():
        input_box.insert("1.0", placeholder_text)
        input_box.config(fg="gray")

# Function to provide real-time validation feedback
def validate_input(event):
    text = input_box.get("1.0", tk.END).strip()
    number = extract_number(text)
    if number and validate_number_format(number):
        input_box.config(bg="white")  # Reset background color
        status_bar.config(text="Status: Valid phone number")
    else:
        input_box.config(bg="pink")  # Highlight invalid input
        status_bar.config(text="Status: Invalid phone number")

# Placeholder text with three sentences, one on each line
placeholder_text = (
    "I want to create a new subscriber with number 302103181020\n"
    "I want to add the service csta to the dn 302103181020\n"
    "I want to delete the subscriber with number 302103181020"
)

def create_gui():
    global input_box
    global status_bar

    root = tk.Tk()
    root.title("Configuration Assistant")
    root.geometry("600x400")  

    # Menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)
    
    # Main frame
    frame_main = tk.Frame(root, padx=20, pady=20)
    frame_main.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    label_instruction = tk.Label(frame_main, text="Type a request or use the proposed actions below:")
    label_instruction.pack(pady=5)

    input_box = tk.Text(frame_main, height=10, width=70, fg="gray", font=("Helvetica", 12))
    input_box.insert("1.0", placeholder_text)
    input_box.pack(pady=10)

    input_box.bind("<FocusIn>", clear_placeholder)
    input_box.bind("<FocusOut>", set_placeholder)
    input_box.bind("<KeyRelease>", validate_input)  # Bind validation function

    submit_button = tk.Button(frame_main, text="Submit", width=20, command=lambda: process_input(input_box.get("1.0", tk.END)))
    submit_button.pack(pady=10)

    # Status bar
    status_bar = tk.Label(root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()

# Run the GUI
create_gui()