from flask import Flask, render_template, request, jsonify
import pandas as pd
from wit import Wit
import os
pending_email_request = False  # Initialize a global variable

app = Flask(__name__)

# Initialize Wit.ai client
WIT_TOKEN = 'YOUR_WIT_AI_TOKEN_HERE'  # Replace with your Wit.ai token
wit_client = Wit(WIT_TOKEN)

def load_employees():
    try:
        # Read the existing Employee Contacts Excel file
        df = pd.read_excel('Employee_Contacts.xlsx')
        
        # Convert DataFrame to dictionary format
        employees = {}
        for _, row in df.iterrows():
            employees[row['Name']] = {
                'position': str(row['Position']),
                'phone': str(row['Phone']),
                'email': str(row['Email'])
            }
        
        print(f"Successfully loaded {len(employees)} employees from Employee_Contacts.xlsx")
        return employees
    except Exception as e:
        print(f"Error loading employees from Employee_Contacts.xlsx: {str(e)}")
        return {}

def find_employee_name(message, employees):
    # Check if any employee name is in the message
    message = message.lower()
    for employee in employees.keys():
        if employee.lower() in message:
            return employee
    return None

def format_contact_info(employee_name, employee):
    return (
        f"Here's {employee_name}'s contact information:\n"
        f"Position: {employee['position']}\n"
        f"Phone: {employee['phone']}\n"
        f"Email: {employee['email']}"
    )

def generate_response(intent, entities, message, employees):
    print(f"Debug - Intent: {intent}")
    print(f"Debug - Entities: {entities}")
    print(f"Debug - Message: {message}")
    print(f"Debug - Available employees: {list(employees.keys())}")
    
    # Map intents to responses
    if intent == "services":
        return "XYZ provides various services, including consultancy, training, and advisory services."
    elif intent == "location":
        return "XYZ is headquartered at [REPLACE_WITH_LOCATION]."
    elif intent == "wifi":
        return "WiFi Name: XYZ-WiFi \n WiFi Password: [REPLACE_WITH_PASSWORD]"
    elif intent == "printer":
        return "Printer Name: XYZ-Printer \n Printer Email Address: [REPLACE_WITH_PRINTER_EMAIL]"
    elif intent == "scan_printer":
        return (
        "To scan a document using the printer, follow these steps: \n"
        "1. Place the document you want to scan in the printer.\n"
        "2. Press the 'Send to Desktop' button on the printer.\n"
        "3. On your computer, open File Explorer.\n"
        "4. In the left-hand sidebar of File Explorer, scroll to the bottom and click on Network.\n"
        "5. Look for '[REPLACE_WITH_COMPUTER_NAME]' under Network and click on it.\n"
        "6. Click on the 'printer_folder' folder.\n"
        "7. When prompted, enter the username and password:\n"
        "   - Username: printer\n"
        "   - Password: printer\n"
        "8. Open the folder, and you will find your scanned document.")
    elif intent == "email":
        global pending_email_request  # Access the global variable

        # If the bot is waiting for a name
        if pending_email_request:
            # Look for the employee name in the user's message
            employee_name = find_employee_name(message, employees)
            pending_email_request = False  # Clear the pending request
            if employee_name:
                return f"{employee_name}'s email ID is: {employees[employee_name]['email']}"
            else:
                return "I couldn't find that employee. Could you provide their name again?"

        # If no pending request, check if the message contains a name
        employee_name = find_employee_name(message, employees)
        if employee_name:
            return f"{employee_name}'s email ID is: {employees[employee_name]['email']}"

        # If no name found, ask the user for clarification
        pending_email_request = True  # Set pending request flag
        return "Whose email ID would you like to know?"

    elif intent == "phone":
        # Check if the message contains an employee name
        employee_name = find_employee_name(message, employees)
        if employee_name:
            return f"{employee_name}'s phone number is: {employees[employee_name]['phone']}"
        return "Whose phone number would you like to know?"
    elif intent == "employees_contact":
        # First try to get employee from entities
        employee_name = None
        if 'wit$contact:contact' in entities:
            employee_name = entities['wit$contact:contact'][0]['body'].capitalize()
        
        # If no entity found, try to find employee name in message
        if not employee_name:
            employee_name = find_employee_name(message, employees)
        
        if employee_name and employee_name in employees:
            return format_contact_info(employee_name, employees[employee_name])
        elif employee_name:
            return f"I couldn't find contact information for {employee_name}. Please check the name and try again."
        else:
            employee_list = ", ".join(employees.keys())
            return f"Which employee's contact information would you like to know? I can help you with these employees: {employee_list}"
    elif intent == "greeting":
        return "Hello! How can I help you today?"
    elif intent == "questions":
        return "Sure. Is there anything else I can help you with?"
    elif intent == "goodbye":
        return "Feel free to come back if you have more questions about XYZ. Have a great day! Goodbye!"
    else:
        # Check if message contains employee name even without proper intent
        employee_name = find_employee_name(message, employees)
        if employee_name:
            return format_contact_info(employee_name, employees[employee_name])
        return "I'm sorry I did not understand that, could you please rephrase?"

@app.route('/')
def home():
    return render_template('chatbot.html')


@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Load employees data for each request to get the latest updates
        employees = load_employees()
        if not employees:
            return jsonify({"error": "Could not load employee data from Employee_Contacts.xlsx"}), 500

        user_message = request.json['message']
        # Get response from Wit.ai
        wit_response = wit_client.message(user_message)
        
        print(f"Debug - Full Wit.ai response: {wit_response}")
        
        # Extract the most relevant information from wit_response
        response_text = "I received your message, but I'm still learning how to respond properly."
        
        if 'intents' in wit_response and wit_response['intents']:
            intent = wit_response['intents'][0]['name']
            confidence = wit_response['intents'][0]['confidence']
            
            print(f"Debug - Intent: {intent}, Confidence: {confidence}")
            
            # Lower the confidence threshold and pass the original message
            if confidence > 0.5:  # Changed from 0.7 to 0.5 for testing
                entities = wit_response.get('entities', {})
                response_text = generate_response(intent, entities, user_message, employees)
        else:
            # Even if no intent is detected, try to generate a response
            response_text = generate_response(None, {}, user_message, employees)
        
        return jsonify({
            "text": response_text,
            "wit_response": wit_response  # Including full Wit.ai response for debugging
        })
    except Exception as e:
        print(f"Debug - Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting server...")
    print("Try these URLs:")
    print("1. http://127.0.0.1:8080")
    print("2. http://localhost:8080")
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")
