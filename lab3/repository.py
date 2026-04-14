from database import SessionDep
from models.text import Text
from models.lemma import Lemma
from models.sentence import Sentence
from sqlalchemy import select, delete, func, desc, distinct
from schemas.lemma import SLemmaAddDb, SLemmaUpdate
from schemas.text import STextAdd, STextUpdate
from typing import Optional, List


class TextRepository:

    @classmethod
    async def get_all(cls, session: SessionDep):
        query = select(Text)
        query_result = await session.execute(query)
        texts = query_result.scalars().all()
        return texts

    @classmethod
    async def get_one(cls, id: int, session: SessionDep):
        text_query = select(Text).where(Text.id == id)
        text_result = await session.execute(text_query)
        text = text_result.scalar_one_or_none()
        return text

    @classmethod
    async def add_one(cls, data: STextAdd, session: SessionDep):
        text_dict = data.model_dump()
        text = Text(**text_dict)
        session.add(text)
        await session.commit()
        await session.refresh(text)
        return text

    @classmethod
    async def delete_one(cls, id: int, session: SessionDep):
        text = await session.get(Text, id)
        if text:
            await session.delete(text)
            await session.commit()
        else:
            raise ValueError(f"Text with id {id} not found")
    
    @classmethod 
    async def count_texts(cls, session: SessionDep):
        query = select(func.count(Text.id).label('texts_amount'))
        result = await session.execute(query)
        return result.scalar_one_or_none()
    


class LemmaRepository:

    @classmethod
    async def get_one(cls, id: int, session: SessionDep):
        lemma_query = select(Lemma).where(Lemma.id == id)
        lemma_result = await session.execute(lemma_query)
        lemma = lemma_result.scalar_one_or_none()
        return lemma


    @classmethod
    async def get_many(
        cls,
        text_id: int,
        session: SessionDep,
        search_word: Optional[str] = None,
        exact_match: bool = False,
        group_by_lemma: bool = False,
        limit: Optional[int] = None,
        offset: int = 0
    ):
        lemma_query = select(Lemma).where(Lemma.text_id == text_id)

        if search_word:
            if exact_match:
                lemma_query = lemma_query.where(Lemma.word == search_word)
            else:
                lemma_query = lemma_query.where(Lemma.word.ilike(f'%{search_word}%'))


        if group_by_lemma:
            lemma_query = lemma_query.distinct(Lemma.lemma)
        lemma_query = lemma_query.order_by(Lemma.lemma.asc())

        if limit:
            lemma_query = lemma_query.limit(limit)
        if offset:
            lemma_query = lemma_query.offset(offset)

        lemma_result = await session.execute(lemma_query)
        return lemma_result.scalars().all()

    @classmethod 
    async def count_words(cls, session: SessionDep):
        query = select(func.count(Lemma.id))
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    @classmethod 
    async def count_unique_words(cls, session: SessionDep):
        query = select(func.count(distinct(Lemma.word)))
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    @classmethod 
    async def count_lemmas(cls, session: SessionDep):
        query = select(func.count(distinct(Lemma.lemma)))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_count_words(cls, session:SessionDep):
        query = (select(Lemma.lemma,Lemma.role,Lemma.morph, func.count(Lemma.word).label('count'))
                .group_by(Lemma.lemma,Lemma.role,Lemma.morph)
                .order_by(desc("count")))
        result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def add_one(cls, data: SLemmaAddDb, session: SessionDep):
        data_dict = data.model_dump()
        lemma = Lemma(**data_dict)
        session.add(lemma)
        await session.commit()
        await session.refresh(lemma)
        return lemma

    @classmethod
    async def delete_one(cls, id: int, session: SessionDep):
        lemma = await session.get(Lemma, id)
        if lemma:
            await session.delete(lemma)
            await session.commit()
        else:
            raise ValueError(f"Text with id {id} not found")

    @classmethod
    async def delete_all(cls, text_id: int, session: SessionDep):
        stmt = delete(Lemma).where(Lemma.text_id == text_id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def update_one(cls, id: int, data: SLemmaUpdate, session: SessionDep):
        data_dict = data.model_dump()
        lemma = await session.get(Lemma, id)
        if lemma:
            lemma.lemma = data_dict.get("lemma")
            lemma.morph = data_dict.get("morph")
            lemma.role = data_dict.get("role")
        await session.commit()
        return lemma

    @classmethod
    async def get_all(cls, text_id: int, session: SessionDep, group_by_lemma: bool = False):
        return await cls.get_many(text_id, session, group_by_lemma=group_by_lemma)

    @classmethod
    async def filter(cls, text_id: int, word: str, session: SessionDep, group_by_lemma: bool = False):
        return await cls.get_many(text_id, session, search_word=word, exact_match=False, checkbox=group_by_lemma)

    @classmethod
    async def search(cls, text_id: int, word: str, session: SessionDep, group_by_lemma: bool = False):
        return await cls.get_many(text_id, session, search_word=word, exact_match=True, checkbox=group_by_lemma)


class SentenceRepository:

    @classmethod
    async def get_by_text(cls, text_id: int, session: SessionDep) -> list:
        query = select(Sentence).where(Sentence.text_id == text_id).order_by(Sentence.index)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_one(cls, sentence_id: int, session: SessionDep):
        query = select(Sentence).where(Sentence.id == sentence_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def add_one(cls, text_id: int, index: int, content: str, session: SessionDep):
        sentence = Sentence(text_id=text_id, index=index, content=content)
        session.add(sentence)
        await session.commit()
        await session.refresh(sentence)
        return sentence

    @classmethod
    async def delete_by_text(cls, text_id: int, session: SessionDep):
        stmt = delete(Sentence).where(Sentence.text_id == text_id)
        await session.execute(stmt)
        await session.commit()
