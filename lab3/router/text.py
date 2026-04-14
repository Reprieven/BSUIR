from database import SessionDep
from schemas.lemma import SLemmaAdd, SLemmaUpdate, SLemmaResponse, SLemmaAddDb
from schemas.text import STextAdd, STextUpdate, STextResponse
from fastapi import APIRouter, status, HTTPException, UploadFile
from repository import LemmaRepository, TextRepository, SentenceRepository
from processers.processing import RtfReader, Processer
from typing import List

router = APIRouter(prefix="/text", tags=["Тексты"])


@router.get("/", response_model=List[STextResponse], status_code=status.HTTP_200_OK)
@router.get("/all", response_model=List[STextResponse], status_code=status.HTTP_200_OK)
async def get_all(session: SessionDep):
    all_texts = await TextRepository.get_all(session)
    return all_texts
    

@router.post("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_one(id: int, session: SessionDep):
    await TextRepository.delete_one(id, session)
    await LemmaRepository.delete_all(id, session)
    await SentenceRepository.delete_by_text(id, session)
    return {"message": "Text and associated data deleted successfully"}


@router.post("/add", response_model=STextResponse, status_code=status.HTTP_201_CREATED)
async def add_text(new_text: UploadFile, session: SessionDep):
    all_words = await RtfReader.read_rtf(new_text.filename, new_text.file)
    text_add = STextAdd(name=new_text.filename, text=all_words)
    text = await TextRepository.add_one(text_add, session)

    processed = Processer.process_with_sentences(
        all_words, "mapping/dep_rules.json", "mapping/morph_rules.json"
    )

    for lemma_dic in processed["lemmas"]:
        await LemmaRepository.add_one(
            SLemmaAddDb(**lemma_dic, text_id=text.id), session
        )

    for idx, s in enumerate(processed["sentences"]):
        await SentenceRepository.add_one(text_id=text.id, index=idx, content=s, session=session)

    return text


@router.get("/{id}", response_model=STextResponse, status_code=status.HTTP_200_OK)
async def get_text(id: int, session: SessionDep):
    text = await TextRepository.get_one(id, session)
    if text is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Text with id {id} not found"
        )
    return text

@router.post('/update/{text_id}')
async def update_text(session: SessionDep,text_id: int, upd_text: STextUpdate):
    try:
        text = await TextRepository.get_one(text_id, session)
        if text.text != upd_text.text:
            await TextRepository.delete_one(text_id, session)
            new_text = STextAdd(name = text.name, text = upd_text.text)
            new = await TextRepository.add_one(new_text, session)
            processed = Processer.process_with_sentences(
                new.text, "mapping/dep_rules.json", "mapping/morph_rules.json"
            )
            for lemma_dic in processed["lemmas"]:
                await LemmaRepository.add_one(
                    SLemmaAddDb(**lemma_dic, text_id=new.id), session
                )
            for idx, s in enumerate(processed["sentences"]):
                await SentenceRepository.add_one(text_id=new.id, index=idx, content=s, session=session)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
