# This file contains the code for generating Verilog code and Testbench code from previously generated Truth Table.

import os
import google.generativeai as genai
from prompts import verilog_prompt, testbench_prompt
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
cfg = genai.GenerationConfig(temperature=0.1)
verilog_agent = genai.GenerativeModel('gemini-1.5-flash', generation_config=cfg)
testbench_agent = genai.GenerativeModel('gemini-1.5-flash', generation_config=cfg)

# This is what the truth table looks like, after getting generated in the previous step.
# truth_table = {'Input1': ['0', '0', '1', '1'], 'Input2': ['0', '1', '0', '1'], 'Parity': ['0', '1', '1', '0']}
# verilog_code = verilog_agent.generate_content(f"{verilog_prompt}\n{truth_table}").text
# print(verilog_code)

# Function to generate Verilog & Testbench codes from Truth Table as input
def verilog_generator(truth_table):
    verilog_code = verilog_agent.generate_content(f"{verilog_prompt}\n{truth_table}").text
    testbench_code = testbench_agent.generate_content(f"{testbench_prompt}\n{verilog_code}").text
    return {"verilog_code":verilog_code, "testbench_code":testbench_code}
