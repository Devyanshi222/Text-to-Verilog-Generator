from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main_logic import verilogify

# Define the FastAPI app
app = FastAPI()

# CORS settings
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