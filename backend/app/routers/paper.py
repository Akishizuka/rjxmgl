from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, GenerationLog
from app.schemas import PaperGenRequest, PaperGenResponse
from app.auth import get_current_user
from app.agent import paper_agent
import json

router = APIRouter(prefix="/api/paper", tags=["paper"])


@router.post("/generate")
def generate_paper(
    payload: PaperGenRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.quota <= 0:
        raise HTTPException(status_code=403, detail="生成次数已用完")

    content = paper_agent.generate(payload.topic)

    current_user.quota -= 1
    db.add(GenerationLog(user_id=current_user.id, topic=payload.topic, content=content))
    db.commit()
    db.refresh(current_user)

    return {"content": content, "remaining_quota": current_user.quota}


@router.post("/generate-stream")
async def generate_paper_stream(
    payload: PaperGenRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.quota <= 0:
        raise HTTPException(status_code=403, detail="生成次数已用完")

    async def event_stream():
        full_content = ""
        async for chunk in paper_agent.generate_stream(payload.topic):
            full_content += chunk
            yield f"data: {json.dumps({'chunk': chunk}, ensure_ascii=False)}\n\n"
        
        # 保存到数据库
        current_user.quota -= 1
        db.add(GenerationLog(user_id=current_user.id, topic=payload.topic, content=full_content))
        db.commit()
        db.refresh(current_user)
        
        yield f"data: {json.dumps({'done': True, 'remaining_quota': current_user.quota}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
