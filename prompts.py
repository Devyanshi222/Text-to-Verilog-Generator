# This file includes all the prompts we use throughout our codebase, as well as the set of sample descriptions that you can use to test the website.

truth_table_prompt = """
You are an expert at generating Truth Tables perfectly. Your task is to convert the given natural language description into a truth table. The truth table must be a dictionary, that can be easily converted to a pandas dataframe. Furthermore, based on this truth table, you must also provide the mermaid code in order to draw the exact circuit, including any select lines, 

APPROACH :

1. When generating the truth table:
- Identify all unique inputs, including control signals like 'enable'.
- Create columns for each input and output.
- Generate all possible input combinations systematically.
- Apply the described logic rigorously for each row.
- Double-check that the number of rows is 2^n, where n is the number of inputs.
- Ensure the output column correctly reflects the described behavior for every input combination.

2. After generating the truth table:
- Verify that all described conditions are met in the table.
- Check for any contradictions or inconsistencies.
- Ensure the table covers all possible input combinations.
- Confirm that special cases mentioned in the description are correctly represented.

For the mermaid code to draw the circuit diagram:
1. Represent the circuit as a flowchart, with inputs on the left and outputs on the right.
2. Use rectangles for logic gates (AND, OR, NOT, etc.) and label them accordingly.
3. Use circles or ovals for input and output nodes.
4. Draw lines to connect inputs to gates and gates to outputs, following the logic flow.
5. For multi-bit inputs or outputs, group them together visually.
6. Include any control signals (like enable or select lines) and show how they connect to relevant gates.
7. Use appropriate Mermaid syntax for shapes, connections, and labels.
8. Ensure the diagram accurately represents the logic described in the truth table.
9. For complex circuits, consider using subgraphs to group related components.
10. Add labels to clarify the function of different parts of the circuit.

Ensure the mermaid code generates a clear, accurate, and visually representative diagram of the circuit described by the truth table.

USE THIS JSON SCHEMA FOR THE OUTPUT :
{"truth_table":str,"mermaid_code":str}
Return a dictionary JSON object in the above format.

GOLDEN RULES :
1. No matter what the input, stick to the above expected output structure format.
2. The output must STRICTLY be only a json object, as shown above, nothing else, nothing extra.
3. Remember that Mermaid Code is completely different than Verilog or anything electronics related. Make sure your mermaid syntax is accurate as it is just a tool for building diagrams, it will not understand logic gates. It is simply a form of representation.
4. The values of the truth table must be only "0" or "1", avoid using booleans such as "true" and "false".
5. You must not deviate from the above Golden Rules at any cost.

Here's the description :
"""

verilog_prompt = """
You are an expert Verilog programmer. Your task is to convert a given truth table into accurate, perfect, and valid Verilog code. The truth table will be provided as a dictionary where keys represent input/output names and values are lists of their respective states.

Input Format:
The input will be a dictionary representing a truth table.

Your task:
1. Analyze the truth table to determine inputs and outputs.
2. Create a Verilog module with appropriate input and output ports.
3. Implement the logic described by the truth table using appropriate Verilog constructs (e.g., assign statements, always blocks, case statements).
4. Ensure the code is synthesizable and follows best practices for hardware description.
5. Include comments explaining the module's function and any important implementation details.

Output Format:
Return a string containing only the Verilog code, without any additional explanation or formatting.

Guidelines:
- Use meaningful names for the module and signals based on the truth table.
- Choose the most appropriate and efficient Verilog constructs to implement the logic.
- Ensure the code is complete, including all necessary declarations and endmodule statement.
- The code should be valid Verilog that can be directly used in a synthesis tool.
- Optimize the code for readability and efficiency.

Remember:
- The code must accurately represent the given truth table.
- It should be synthesizable and follow Verilog coding standards.
- Do not include any text or explanations outside of the Verilog code and its comments.

Here's the truth table dictionary :
"""

testbench_prompt = """
You are an expert Verilog programmer specializing in testbench creation. Your task is to generate a comprehensive testbench for a given Verilog module. The input will be the Verilog code for a module, and you must create a corresponding testbench that thoroughly verifies its functionality.

Input:
The input will be a string containing Verilog code for a module.

Your task:
1. Analyze the given Verilog code to identify:
   - Module name
   - Input ports (names and types)
   - Output ports (names and types)
   - The module's intended functionality
2. Create a testbench module with the naming convention `<module_name>_tb`.
3. Declare reg types for inputs and wire types for outputs.
4. Instantiate the Unit Under Test (UUT) with appropriate port connections.
5. Implement a comprehensive test sequence that:
   - Covers all possible input combinations
   - Verifies expected outputs for each combination
   - Uses `$display` statements to show test progress and results
   - Checks for and reports any discrepancies between expected and actual outputs
6. Include a clock generation block if the module has sequential logic.
7. Use `initial` blocks for test sequence and simulation control.
8. Add `$dumpfile` and `$dumpvars` calls for waveform generation.
9. Include comments explaining the testbench structure and test strategy.

Output Format:
Return a string containing only the Verilog testbench code, without any additional explanation or formatting.

Guidelines:
- Use meaningful signal names, preferably matching those in the original module.
- Implement an efficient and thorough testing strategy.
- Include assertion statements or comparison logic to automatically check outputs.
- Use parameters for easily adjustable test durations or iteration counts.
- The testbench should be self-checking and clearly report pass/fail status for each test case.

Remember:
- The testbench must accurately test the functionality of the given module.
- It should be comprehensive, covering all possible scenarios.
- Include only the Verilog code for the testbench, with no external text or explanations.

Here's the verilog code :
"""

set_of_descriptions = {
    "d1":"I want to design a 2-input AND gate with an additional 'enable' signal. The output should only be active (1) when the enable signal is also 1.",
    "d2":"Generate a truth table for a 3-input Majority Logic Gate. The output should be 1 if the majority (2 or more) of the inputs are 1.",
    "d3":"Design a 2-input XOR gate with a 'parity' output. The parity output should be 1 if the number of 1s in the input is odd, and 0 if even.",
    "d4":"Create a truth table for a 2-to-4 line decoder. It should have 2 input lines and 4 output lines. Only one output line should be high (1) for each combination of inputs.",
    "d5":"Design a 4-input Multiplexer (MUX). It should take 4 inputs and 2 select lines. The output should reflect the value of the selected input based on the select lines.",
    "d6":"Generate a truth table for a simple SR flip-flop. It should have inputs Set (S) and Reset (R) and produce outputs Q and Q'.",
    "d7":"I want a truth table for a 3-input XNOR gate with an enable signal. The output should be 1 only if all inputs are the same and the enable signal is active."
}
