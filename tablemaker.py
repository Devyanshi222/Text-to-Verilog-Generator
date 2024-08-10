import os
import base64
import typing_extensions as typing
from prompts import truth_table_prompt
import google.generativeai as genai
from dotenv import load_dotenv
from ast import literal_eval as lvl
load_dotenv()

class OutputSchema(typing.TypedDict):
    truth_table: str
    mermaid_code: str

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
cfg = genai.GenerationConfig(temperature=0.1, response_mime_type="application/json", response_schema=OutputSchema)
truth_table_maker = genai.GenerativeModel('gemini-1.5-flash', generation_config=cfg)


def get_diagram(mermaid_code):
    graphbytes = mermaid_code.encode("utf8")
    b64bytes = base64.b64encode(graphbytes)
    b64string = b64bytes.decode("ascii")
    return f"https://mermaid.ink/img/{b64string}"

def text_to_truth_table(text):
    response = truth_table_maker.generate_content(f"{truth_table_prompt}\n{text}").text
    parsed_response = lvl(response)
    tt = lvl(parsed_response["truth_table"])
    # table = pd.DataFrame(tt)
    mcode = parsed_response["mermaid_code"] if "[style=dashed]" not in parsed_response["mermaid_code"] else parsed_response["mermaid_code"].replace("[style=dashed]", "")
    output_array = {"table":tt, "mcode":mcode, "diagram":get_diagram(mcode)}
    return output_array