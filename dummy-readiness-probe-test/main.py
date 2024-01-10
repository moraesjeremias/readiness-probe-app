import os
import time

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketException
from statemachine import StateMachine, State

node_replica = os.getenv('NODE_REPLICA')
startup_probe_delay = float(os.getenv('STARTUP_PROBE_DELAY', 10))
app = FastAPI()


class NodeStatus(StateMachine):
    ready_state = State(name='READY', initial=True, value='READY')
    not_ready_state = State('NOT_READY', value='NOT_READY')

    flip_state_not_ready = ready_state.to(not_ready_state)
    flip_state_ready = not_ready_state.to(ready_state)


node_status = NodeStatus()


@app.get("/status")
async def status():
    return build_response_message()


@app.websocket('/ws/healthz')
async def health(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            if data['method'] == 'is_alive':
                await websocket.send_json(build_response_message())
            if data['method'] == 'close_conn':
                await websocket.close(reason='Connection closed by user')
                break
        except WebSocketException as ws_execpt:
            await websocket.close(code=ws_execpt.code, reason=ws_execpt.reason)


@app.get("/healthz")
async def health():
    if node_status.current_state.value == 'READY':
        return build_response_message()
    else:
        raise HTTPException(status_code=502, detail=f'Node {node_replica} status is not Ready!')


@app.get('/termination')
async def kill():
    node_status.flip_state_not_ready()
    return build_response_message()


@app.get('/recovery')
async def recover():
    node_status.flip_state_ready()
    return build_response_message()


def build_response_message() -> dict:
    return {"status": node_status.current_state.value, "replica": node_replica}


if __name__ == '__main__':
    time.sleep(startup_probe_delay)
    uvicorn.run("main:app", host='0.0.0.0', port=8081)
