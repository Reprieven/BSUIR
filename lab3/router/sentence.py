from database import SessionDep
from schemas.sentence import SSentenceResponse, SSentenceAnalysis, SSentenceAnalyzeInput
from fastapi import APIRouter, status, HTTPException
from repository import SentenceRepository, TextRepository
from processers.processing import SentenceProcessor
from typing import List

router = APIRouter(prefix="/text/{text_id}/sentence", tags=["Предложения"])


@router.get("/", response_model=List[SSentenceResponse], status_code=status.HTTP_200_OK)
async def get_sentences(text_id: int, session: SessionDep):
    current_text = await TextRepository.get_one(text_id, session)
    if not current_text:
        raise HTTPException(status_code=404, detail="Text not found")
    sentences = await SentenceRepository.get_by_text(text_id, session)
    return sentences


@router.get("/{sentence_id}/analyze", response_model=SSentenceAnalysis)
async def analyze_sentence(text_id: int, sentence_id: int, session: SessionDep):
    sentence = await SentenceRepository.get_one(sentence_id, session)
    if not sentence:
        raise HTTPException(status_code=404, detail="Sentence not found")
    result = SentenceProcessor.analyze_sentence(sentence.content)
    return result


@router.post("/analyze-custom", response_model=SSentenceAnalysis)
async def analyze_custom_text(text_id: int, body: SSentenceAnalyzeInput):
    result = SentenceProcessor.analyze_sentence(body.text)
    return result
