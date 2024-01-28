import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.prompts.chat import ChatPromptTemplate
from langchain.llms import CTransformers
from sqlalchemy import create_engine
from langchain.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os


st.set_page_config(page_title="AI APP TO CHAT WITH SQL DB")
st.header="ASK ANYTHING ABOUT YOUR DB"
query=st.text_input("ask question here")


cs="mysql+pymysql://llmtask:1234@localhost:3306/final_llm_task"
db_engine=create_engine(cs)
db=SQLDatabase(db_engine)
config = {'max_new_tokens': 256, 'repetition_penalty': 1.1, 'temperature': 0, 'context_length': 10000}



llm=llm = CTransformers(model="TheBloke/CodeLlama-7B-Instruct-GGUF",  model_file="codellama-7b-instruct.Q4_K_M.gguf",config=config, verbose=True) #--local path can be added here of selected models.

#--------Use this code if Ctransformers model take too much time

# callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
 
# n_gpu_layers = 1
# n_batch = 512
# llm = LlamaCpp(
# model_path="./models/llama-2-7b-chat.Q8_0.gguf",
# n_gpu_layers=n_gpu_layers,
# n_batch=n_batch,
# n_ctx=4000,
# f16_kv=True,
# callback_manager=callback_manager, 
# verbose=True,
# )


sql_toolkit=SQLDatabaseToolkit(db=db,llm=llm)
sql_toolkit.get_tools()

prompt=ChatPromptTemplate.from_messages(
    [
        ("system",
        """
        you are a very intelligent AI assistant who is expert in identifing relevant questions from user and converting into sql queriers to generate correct answer.
        Please use the belolw context to write mysql queries.
        context:
        you must query against the connected database,it has total 5 tables,these are employee, employee_address,employee_emergency_contact,employee_experience,employee_roles.
        employee : This table represents the details of every employee. Schema : employee.id, employee.employee_code, employee.first_name, employee.middle_name, employee.last_name, employee.join_date, employee.dob, employee.designation_id, employee.department_id, employee.email_id, employee.personal_email_id, employee.mobile_no, employee.gender, employee.blood_group, employee.reporting_to, employee.status, employee.password_updated_at, employee.marital_status, employee.password, employee.profile_image, employee.google_profile, employee.mother_name, employee.father_name, employee.spouse_name, employee.marriage_date, employee.createdAt, employee.updatedAt, employee.created_by, employee.updated_by, employee.prev_experience, employee.confirmation_date, employee.last_email_sent, employee.email_sent_count, employee.business_unit_id, employee.spouse_dob, employee.remarks, employee.country_code, employee.timesheet_filling
        employee_address : This table represents the corresponding address of the users. Schema : employee_address.id, employee_address.employee_id, employee_address.present_address, employee_address.present_town, employee_address.present_state_id, employee_address.present_mobile_no, employee_address.present_pincode, employee_address.permanent_address, employee_address.permanent_town, employee_address.permanent_state_id, employee_address.permanent_mobile_no, employee_address.permanent_pincode, employee_address.is_same_address, employee_address.createdAt, employee_address.updatedAt, employee_address.present_country_code, employee_address.permanent_country_code
        employee_emergency_contact : This table represents the contact number of a person to reach out in case of an emergency. Schema : employee_emergency_contact.id, employee_emergency_contact.employee_id, employee_emergency_contact.relation_type, employee_emergency_contact.name, employee_emergency_contact.mobile_no, employee_emergency_contact.createdAt, employee_emergency_contact.updatedAt, employee_emergency_contact.country_code
        employee_experience : This table represents the employee work experience related information. Schema : employee_experience.id, employee_experience.employee_id, employee_experience.employer_name, employee_experience.location, employee_experience.start_date, employee_experience.end_date, employee_experience.designation, employee_experience.website, employee_experience.document, employee_experience.remark, employee_experience.createdAt, employee_experience.updatedAt
        employee_roles : This table represents the employee position and job related information. Schema : employee_roles.id, employee_roles.employee_id, employee_roles.role_id, employee_roles.created_at, employee_roles.updated_at, employee_roles.deleted_at, employee_roles.expiry_date, employee_roles.description
        As an expert you must use joins whenewver required.
        """
        ),
        ("user","{question}\ ai: ")
    ]

        )
agent=create_sql_agent(llm=llm,toolkit=sql_toolkit,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True,max_execution_time=100,max_iterations=1000,handle_parsing_errors=True)

if st.button("Submit",type="primary"):
    if query is not None:
        response=agent.run(prompt.format_prompt(question=query))
        st.write(response)
