from fastapi import FastAPI, status, Request
from router import text, lemma, sentence
from contextlib import asynccontextmanager
from database import Base, engine
from fastapi.responses import RedirectResponse
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(text.router)
app.include_router(lemma.router)
app.include_router(sentence.router)

@app.middleware('http')
async def timer(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    print(process_time)
    return response



@app.get("/")
async def index():
    return RedirectResponse("/text", status_code=status.HTTP_308_PERMANENT_REDIRECT)
