import os

import uvicorn
from fastapi import FastAPI, HTTPException
from statemachine import StateMachine, State

node_replica = os.getenv('NODE_REPLICA')
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


def build_response_message():
    return {"status": node_status.current_state.value, "replica": node_replica}


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8081)
