from fastapi import FastAPI
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
cors_vulnerable = CORSMiddleware(...)
app.add_middleware(cors_vulnerable)
