# This file contains the code for generating truth tables and diagrams from natural language description.
# We achieve this using Google's LLM (Large Language Model), called "Gemini".
# An LLM is a machine learning model that can understand human language, and can also generate human language (take ChatGPT for example).
# We use the Gemini LLM in this project, and ask it to generate truth tables and diagrams and all the codes, by simply providing it with the description of the circuit.
# In order to use this Gemini LLM, we have to use its "API Key", which acts like a password basically. If this password is authenticated, Google allows us to chat with its LLM. If you don't have an API Key, you won't be able to use the LLM.

import os  # this module is used to fetch API keys (in our case, the Google Gemini API key)
import base64  # this module is used to encode the diagram (in our case, the mermaid code) into a format that can be made into a URL
import typing_extensions as typing  # to define the schema for the Gemini LLM (so that its output format is consistent throughout all prompts)
from prompts import truth_table_prompt  # we import prompts from a separate python file
import google.generativeai as genai  # this is the Gemini API
from dotenv import load_dotenv  # API Keys are like passwords, and we store them in a separate file called ".env". In order to use API Key in this code, we use the dotenv module to search for a .env file and extract the key in order to use it.
from ast import literal_eval as lvl  # this module will convert string datatype to the actual datatype that's inside the string (in our case, a dictionary)
load_dotenv()

# Defining the output format for the LLM
class OutputSchema(typing.TypedDict):
    truth_table: str
    mermaid_code: str

# Configuring the LLM
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
cfg = genai.GenerationConfig(temperature=0.1, response_mime_type="application/json", response_schema=OutputSchema)
truth_table_maker = genai.GenerativeModel('gemini-1.5-flash', generation_config=cfg)

# Function to get diagram url from mermaid code
def get_diagram(mermaid_code):
    graphbytes = mermaid_code.encode("utf8")
    b64bytes = base64.b64encode(graphbytes)
    b64string = b64bytes.decode("ascii")
    return f"https://mermaid.ink/img/{b64string}"

# Function to generate Truth Table and Diagram, given the text description
def text_to_truth_table(text):
    response = truth_table_maker.generate_content(f"{truth_table_prompt}\n{text}").text
    parsed_response = lvl(response)
    tt = lvl(parsed_response["truth_table"])
    # table = pd.DataFrame(tt)
    mcode = parsed_response["mermaid_code"] if "[style=dashed]" not in parsed_response["mermaid_code"] else parsed_response["mermaid_code"].replace("[style=dashed]", "")
    output_array = {"table":tt, "mcode":mcode, "diagram":get_diagram(mcode)}
    return output_array
