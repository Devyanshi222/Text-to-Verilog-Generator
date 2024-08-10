from tablemaker import text_to_truth_table
from verilog_util import verilog_generator

def verilogify(description):
    truth_table = text_to_truth_table(description)
    tt = truth_table['table']
    diagram = truth_table['diagram']
    output_data = verilog_generator(truth_table['table'])
    return {"diagram":diagram, "final_table":tt, "verilog_code":output_data["verilog_code"], "testbench_code":output_data["testbench_code"]}