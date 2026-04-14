from database import SessionDep
from schemas.lemma import SLemmaAddDb, SLemmaUpdate, SLemmaResponse, SLemmaCount
from fastapi import APIRouter, status, HTTPException, Form, Query, Response
from repository import LemmaRepository, TextRepository
from typing import List, Optional
from schemas.stat import SStat


router = APIRouter(prefix="/text/{text_id}/lemma", tags=["Леммы"])


@router.get("/", response_model=List[SLemmaResponse])
async def get_lemmas(
    session: SessionDep,
    text_id: int,
    search: Optional[str] = Query(None),
    exact_match: bool = Query(False),
    checkbox: bool = Query(False),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    current_text = await TextRepository.get_one(text_id, session)
    if not current_text:
        raise HTTPException(status_code=404, detail="Text not found")
    lemmas = await LemmaRepository.get_many(
        text_id=text_id,
        session=session,
        search_word=search,
        exact_match=exact_match,
        group_by_lemma=checkbox,
        limit=limit,
        offset=offset
    )
    return lemmas

@router.get('/count/words', response_model = List[SLemmaCount])
async def get_lemmas_count_words(session: SessionDep):
    lemmas = await LemmaRepository.get_count_words(session)
    return lemmas

@router.get('/count/all', response_model= SStat)
async def count_all(session: SessionDep):
    texts = await TextRepository.count_texts(session)
    words = await LemmaRepository.count_words(session)
    unique_words = await LemmaRepository.count_unique_words(session)
    lemmas = await LemmaRepository.count_lemmas(session)
    return SStat(texts=texts,
                 words=words,
                 unique_words=unique_words,
                 lemmas=lemmas)



@router.get("/export/txt", response_model=List[SLemmaResponse], status_code=status.HTTP_200_OK)
async def export_lemmas_txt(
    session: SessionDep,
    text_id: int,
    search: Optional[str] = Query(None),
    exact_match: bool = Query(False),
    checkbox: bool = Query(False),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    lemmas = await LemmaRepository.get_many(
        text_id=text_id,
        session=session,
        search_word=search,
        exact_match=exact_match,
        group_by_lemma=checkbox,
        limit=limit,
        offset=offset
    )
    
    text_content = ''
    for i, lemma in enumerate(lemmas, 1):
        text_content += f"{i}. {lemma.lemma}\n"
        text_content += f"   Слово: {lemma.word}\n"
        text_content += f"   Морфология: {lemma.morph}\n"
        text_content += f"   Роль: {lemma.role}\n"
        text_content += "-" * 40 + "\n"
    
    return Response(
        content=text_content,
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename=lemmas_text{text_id}.txt",
            "Content-Type": "text/plain; charset=utf-8"
        }
    )


@router.post("/add", response_model=SLemmaResponse, status_code=status.HTTP_201_CREATED)
async def add_one(
    session: SessionDep,
    text_id: int,
    word: str = Form(...),
    lemma: str = Form(...),
    morph: str = Form(...),
    role: str = Form(...),
):
    new_lemma = await LemmaRepository.add_one(
        SLemmaAddDb(
            lemma=lemma,
            morph=morph,
            role=role,
            word=word,
            text_id=text_id,
        ),
        session,
    )
    return new_lemma

