import json
from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
#from langchain.chat_models import AzureChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from dotenv import load_dotenv

load_dotenv() # load OPENAI_API_KEY from .env
app = FastAPI()

system = """You are a technical product manager and solution architect. You write detailed technical user stories for given product requirements.

The Platform used for the product is AWS cloud. Following are the AWS services that can be used in the product:
- Arbitration-Layer (proprietary channel routing engine for push to outbound channels, REST APIs for inbound channels)
- T3 (proprietary data-lake, similar to AWS Athena)
- T3 -Feature-Mart (proprietary customer  model input data and metadata management)
- Job-Server (proprietary platform for data processing and model inference, similar to AWS EMR)
- Analytical-Cluster (proprietary data science work-bench, similar to AWS SageMaker)
- Core Banking (On-prem Account and transaction management system)
- Credit Card & Loans System (On-prem) 
- Internet Banking Website 
- Mobile Banking App 
- P2P Payment App
- API Gateway
- Data Loader (for loading data from T3 to MariaDB)
- CyberArk (for managing secrets)
- Confluent Kafka (as real time event source)
- MariaDB (as application database)
- ReactJS (for UI)
- AWS S3
- AWS SageMaker (for AI model training and inference)
- AWS EMR (for AI model training and inference)
- AWS Lambda

Mention the users as 'Business user', 'Customer', 'System Developer' and other users if relevant e.g. 'Data Scientist', 'Analyst', 'Compliance Officer', 'Site Reliability Engineer'

Write detailed technical user stories in a JSON array with title, user, description and questions for each story.
"""
requirement1 = """Business Requirements:
A self-service marketing rule-engine for business users to develop targeted marketing rules using AI model recommendations and customer data, including product-propensities, demographics, behavior, service usage, and transaction history. The platform ensures minimal spam and delivers messages via inbound and outbound channels. AI models provide product recommendations, predict propensities, optimize relevance, and align with revenue goals, while determining the best contact method, channels, timing, and content. Data is sourced from T3 for historical customer information and from Confluence Kafka for real-time customer events."""
epics1 = '[{"title":"Marketing rules for targeted messages","description":"Create marketing rules based on AI model recommendations and customer data to deliver targeted messages via inbound and outbound channels. The rules should allow me to filter customers based on product-propensities, demographics, behavior, recent usage of services, and transaction history. The rules should also comply with regulatory requirements and prevent spamming customers. The system should provide a user-friendly interface to create, edit, and delete rules.","questions":["List of events to be available in the system.","Examples of complex conditions to be supported in rules. e.g. timeout between start and end events, event sequence.","List of spamming prevention rules."]},{"title":"Arbitration between inbound and outbound channels","description":"Create rules to arbitrate across all inbound and outbound channels. Inbound channels should include mobile apps, website and support calls. Outbound channels should include push-notes, email and SMS. The rules should allow me to specify the priority of channels and the conditions under which a channel should be used. The system should integrate with Arbitration-Layer and provide options to setup routing to one or multiple channels of Arbitration-Layer. Rules should be able to use a mix of AI model recommended touch points/channels, product/offer information and customer data to determine the best channel to contact a customer.","questions":["List of all inbound and outbound channels to support.","Types and examples of criteria to be supported"]},{"title":"Train AI models and monitor model performance over time","description":"Train AI models to provide product recommendations, product propensities and content personalization. The system should provide a way to make training data available to Analytical-Cluster or AWS SageMaker to train the models. The system should also provide a way to update the models with new data and retrain them periodically.","questions":["Training data in T3-Feature-Mart should include customer demographics, behavior, service usage logs including Adobe/Google Analytics and customer transaction history.","Training data should be accessible in Analytical-Cluster or AWS SageMaker for training the models.","List of Model monitoring metrics. Definition of each metric.","Threshold values for each model monitoring metric, to raise alerts."]},{"title":"Integrate AI models into the rule engine system","user":"System Developer","description":"Integrate AI models into the rule engine system to predict product-propensity, maximizing relevance of products to customers and bank\'s revenue expectations. The AI models should predict the best way to contact a customer, determining the optimal channels, timing, and content. The system should provide REST APIs to access the real-time AI models in rule engine. The system should also provide batch scoring option on Job-Server or AWS EMR, where scores across all customers need to be calculated at the same time.","questions":["List of AI models. Inputs and outputs of each AI model","List of APIs. Inputs and outputs of each API","List of batch scoring jobs. Inputs and outputs of each job"]},{"title":"Measure campaign effectiveness using control groups","user":"Business user","description":"Measure the effectiveness of campaigns using control groups. The system should provide a way to create control groups, assign them to campaigns and compare the results with the treatment groups. The system should generate reports with metrics such as conversion rate, revenue generated, and customer satisfaction.","questions":["List of metrics to be used for measuring campaign effectiveness.","Treatment group evaluation criteria for stratified sampling.","Types and examples of campaigns to be supported."]},{"title":"Handle high volumes and build fault-tolerant and resilient system","user":"System Developer","description":"Handle high volume and velocity of events and actions without compromising performance or reliability. The event handling should use scalable platforms like AWS Lambda and AWS SQS to process events asynchronously and scale up or down based on the load. The system should also use caching and load balancing for APIs to improve performance and reduce latency.","questions":["Maximum expected volume of events and actions.","Expected expect historical data to be loaded."]},{"title":"Secure and compliant system","user":"Compliance Officer","description":"Ensure that the system is secure and compliant with the bank\'s policies and regulations. The system should use CyberArk or AWS KMS to store keys to encrypt data at rest and in transit. The system should also use an APM like Splunk or AWS CloudTrail to monitor and audit system activity. The system should be regularly tested for vulnerabilities and compliance with the bank\'s policies and regulations.","questions":["List of compliance tests to be performed."]},{"title":"System monitoring dashboard","user":"Site Reliability Engineer","description":"Ensure that the system health is monitored and displayed on a live dashboard. There should be configurable thresholds for system metrics, to raise alarms and send notifications relevant SRE and development teams.","questions":["List of system metrics to be monitored.","List of alarms to be raised.","List of notifications to be sent."]}]'

@app.get("/")
async def root():
    return {"message": "Usage: Call /epics with the requirements text in the post body"}

# Generate epics for the given requirements using OpenAI ChatCompletion API
@app.get("/epics/{requirements}")
@app.post("/epics")
def epics(requirements: str):
    req = "Business Requirements:\n{requirements}".format(requirements=requirements)
    chat = ChatOpenAI(temperature=0.5, max_tokens=2000)
    messages = [
        SystemMessage(content=system),
        HumanMessage(content=requirement1),
        AIMessage(content=epics1),
        HumanMessage(content=req),
    ]
    print("\nCalling OpenAI ChatCompletion API with messages: {messages}".format(messages=messages))
    epics_str = chat(messages).content
    print("\nReceived epics from OpenAI ChatCompletion API: {epics}".format(epics=epics_str))
    epics_json = json.loads(epics_str)
    print("\n{epics_length} epics received from OpenAI ChatCompletion API".format(epics_length=len(epics_json)))
    return epics_json
