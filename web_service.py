# Our entire code so far has been written in Python. However, if we wish to build a website, we would write the code for that in HTML,CSS and JavaScript. But we also know that we can't directly use our Python code inside the HTML, CSS, JS codebase. 
# In order to combat this issue, we use something known as an "API". An API allows us to "call" or "request" some data from Python logic, right inside JavaScript. 
# The module called "FastAPI" is used to create a simple API - we define the URL, and decide which function should be called, when this url is accessed by the JavaScript. In our case, our JavaScript code calls our API, provides it the text description (that the user enters on the website), and requests the 4 output components that we wish to display on the website. 
# However, there's another problem. This code that we've written, is only available for us to run. Even if we were to build an API here, and call that in our JavaScript code, it will only work on our device. So how will anyone else use our website, if our API only runs on our device?
# To solve that problem, we use a platform called "Render". Render lets you upload (also known as DEPLOY) your python code (of the API you've made), and it returns a publicly accessible API URL, which you can then use in your javascript and build the website successfully.
# Our goal with this file, is to build an API that takes in natural language descriptions, and returns a dictionary as output.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main_logic import verilogify  # we import the function that generates 4 components from text descriptions

# Define the FastAPI app
app = FastAPI()

# CORS settings (Cross Origin Resource Sharing, or CORS, allows any domain / IP to access our API without issues)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the input model
class VerilogifyRequest(BaseModel):
    description: str

# Define the output model
class VerilogifyResponse(BaseModel):
    diagram: str
    final_table: dict
    verilog_code: str
    testbench_code: str

# The main endpoint
# An endpoint is the part that comes at the end of any base URL.
# In our case, the base URL is of the deployed API (https://text-to-verilog-generator.onrender.com/) while the endpoint we're defining below is "/verilogify"
# It means that whenever we write "/verilogify" after the base url, and access it, we will get those 4 components in return. JavaScript automatically does this for us, whenever the user presses on the "Proceed" button.
@app.post("/verilogify", response_model=VerilogifyResponse)
async def verilogify_endpoint(request: VerilogifyRequest):
    try:
        result = verilogify(request.description)
        return VerilogifyResponse(
            diagram=result["diagram"],
            final_table=result["final_table"],
            verilog_code=result["verilog_code"],
            testbench_code=result["testbench_code"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
