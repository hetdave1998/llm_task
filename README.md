# AI Chat with SQL Database

![AI Chat with SQL Database](link_to_an_image)

This Streamlit app allows you to interact with a SQL database using natural language queries. It utilizes the LangChain library to create an intelligent AI assistant capable of understanding and executing SQL queries based on user input.

## Getting Started

### Prerequisites

Before running the application, make sure you have the following dependencies installed:

- [Streamlit](https://streamlit.io/)
- [LangChain](https://github.com/langchain/langchain)

You can install them using:

```bash
pip install streamlit
pip install langchain
```
### Setting Up OpenAI API Key

Set your OpenAI API key as an environment variable. Replace "key" with your actual API key.

```bash
export OPENAI_API_KEY="key"
```

### Running the App

```bash
streamlit run your_script_name.py
```
### Usage

Input your SQL-related question in the provided text box.
Click the "Submit" button to get a response from the AI assistant.

### Database Schema

The app is designed to query a database with the following schema:

Employee Table
id
employee_code
first_name
middle_name
last_name
join_date
dob
designation_id
department_id
... (other fields)

Employee Address Table
id
employee_id
present_address
present_town
present_state_id
... (other fields)

Employee Emergency Contact Table
id
employee_id
relation_type
name
mobile_no
... (other fields)

Employee Experience Table
id
employee_id
employer_name
location
start_date
end_date
... (other fields)

Employee Roles Table
id
employee_id
role_id
created_at
updated_at
... (other fields)

### Important Notes

Feel free to ask anything about the connected database!

