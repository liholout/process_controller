from fastapi import FastAPI, status, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from subprocess import Popen, PIPE
import asyncio
import psutil

app = FastAPI()
process = None
output = None


@app.get("/api/docs")
async def get_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")


async def run_process():
    """
    Run the subprocess and store the output
    """
    global process, output
    try:
        process = await asyncio.create_subprocess_exec('bash', 'test.sh', stdout=PIPE, stderr=PIPE)
        stdout, _ = await process.communicate()
        output = stdout.decode()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/api/test.sh")
async def start_process():
    """
    Start process with name pn
    """
    global process, output
    if process is not None and process.returncode is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Process is already running")
    try:
        asyncio.create_task(run_process())
        return {"message": "Process started successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/api/test.sh/stop")
async def stop_process():
    """
    Stop process with name pn
    """
    global process, output
    if process is None or process.returncode is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Process is not running")
    try:
        process.terminate()
        output = None
        return {"message": "Process stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/test.sh")
async def get_process_status():

    """
    Get status of process with name pn
    """

    global process

    if process is None or process.returncode is not None:
        return {"status": "Process is not running"}

    # Get process resource usage
    process_id = process.pid
    process_cpu_usage = psutil.Process(process_id).cpu_percent()
    process_memory_usage = psutil.Process(process_id).memory_percent()

    # Get process uptime
    process_start_time = psutil.Process(process_id).create_time()
    process_uptime = psutil.time.time() - process_start_time

    return {
        "status": "Process is running",
        "uptime": process_uptime,
        "cpu_usage": process_cpu_usage,
        "memory_usage": process_memory_usage
    }


@app.get("/api/test.sh/result")
async def get_process_result():
    """
    Get result of process with name pn
    """
    global output, process
    if process is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 Not Found")
    elif process.returncode is None and output is None:
        return {"result": "Results are not available yet, process is running"}
    elif output is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not available")
    return {"result": output}
