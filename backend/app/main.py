from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, paper

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OpenClaw 论文生成系统",
    description="基于智能体的高质量毕业论文自动生成服务",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(paper.router)


@app.get("/")
def root():
    return {"message": "OpenClaw API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
