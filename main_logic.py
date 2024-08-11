# This file is the main logic of the project. Think of the entire workflow as a tree, then this file becomes the root node.
# We import some functions from other files (or branches of the tree) and then get the final output, which is a dictionary consisting of 4 things : a diagram, a truth table, the verilog code & the testbench code.
# This is how it works : 
# Step 1] we pass (Natural Language Description) to --> (Truth Table Maker) -> & we get Truth Table and Diagram as output.
# Step 2] we then pass (Truth Table) to --> (Verilog Generator) -> & we get Verilog Code and Testbench Code as output.

from tablemaker import text_to_truth_table  # we import the code that has the function to generate truth tables from text
from verilog_util import verilog_generator  # we import the code that has the function to generate codes from truth table

# Function that takes in natural language description, and directly outputs the 4 components as discussed above
def verilogify(description):
    truth_table = text_to_truth_table(description)
    tt = truth_table['table']
    diagram = truth_table['diagram']
    output_data = verilog_generator(truth_table['table'])
    return {"diagram":diagram, "final_table":tt, "verilog_code":output_data["verilog_code"], "testbench_code":output_data["testbench_code"]}
