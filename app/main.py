from fastapi import FastAPI

from app.entities.order.router import router as order_router


app = FastAPI(
    title="Kafka Order Event Pipeline",
    version="1.0.0",
)


app.include_router(order_router)


@app.get("/")
def root():

    return {
        "message": "Kafka Order Event Pipeline"
    }