# internal_chatbot-
Internal Website Chatbot
An intelligent chatbot designed for internal use within the company's web portal. This chatbot simplifies the process of retrieving employee contact information and responding to frequently asked internal queries, providing a seamless and user-friendly experience for employees.

Features
Employee Contact Directory:
Retrieve detailed contact information, including position, email, and phone number, for employees listed in an internal directory.
Natural Language Understanding:
Leverages Wit.ai to interpret and respond to user queries in natural language.
Frequently Asked Questions (FAQs):
Preprogrammed responses to common queries, such as Wi-Fi details, printer setup, and company services.
Dynamic Data Loading:
Reads from an up-to-date employee directory stored in an Excel file to ensure accurate information.
Integrated Web Interface:
Embedded directly into the company's internal website for easy access.
How It Works
Chatbot Interface:

Employees interact with the chatbot via a lightweight, embedded chat window in the company’s internal website.
Query Handling:

Messages are sent to the Flask-based backend, where they are analyzed for intent and entities using Wit.ai.
Response Logic:

Based on the detected intent:
FAQs are addressed with predefined responses.
Employee-specific data is fetched from the internal directory.
Unrecognized queries are handled gracefully with fallback messages.
Data Display:

Responses are displayed within the chat interface for a conversational experience.

Usage
Employees can query the chatbot for:
Contact details of specific employees.
Internal resources like Wi-Fi credentials or printer setup guides.
General company-related information.
The chatbot provides instant responses, improving efficiency and accessibility of information.

To Launch the Chatbot:
python run.py
