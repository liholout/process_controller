from fastapi import FastAPI

app = FastAPI()
process_running = False
last_result = ""


@app.post("/api/{process_name}/start")
async def start_process(process_name: str):
    global process_running, last_result
    if process_running:
        return {"message": f"{process_name} process is already running."}
    else:
        # Здесь необходимо запустить процесс process_name
        process_running = True
        last_result = ""
        return {"message": f"{process_name} process has been started."}


@app.post("/api/{process_name}/stop")
async def stop_process(process_name: str):
    global process_running
    if process_running:
        # Здесь необходимо остановить процесс process_name
        process_running = False
        return {"message": f"{process_name} process has been stopped."}
    else:
        return {"message": f"{process_name} process is not running."}


@app.get("/api/{process_name}")
async def get_process_status(process_name: str):
    global process_running
    if process_running:
        return {"message": f"{process_name} process is running."}
    else:
        return {"message": f"{process_name} process is not running."}


@app.get("/api/{process_name}/result")
async def get_last_result(process_name: str):
    global last_result, process_running
    if not process_running:
        return {"message": f"{process_name} process is not running."}
    elif last_result == "":
        return {"message": f"No result available for {process_name} process."}
    else:
        return {"result": last_result}


@app.get("/api/docs")
async def get_api_docs():
    return {"message": "API documentation goes here."}
