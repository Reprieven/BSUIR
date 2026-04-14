import spacy
import json
from typing import List, Dict, IO, Tuple
from spacy.tokens import Doc, Token

_model = None


def get_model():
    global _model
    if _model is None:
        _model = spacy.load("en_core_web_md")
    return _model


class JsonProcesser:
    @classmethod
    def process_json(cls, file_path: str):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data


class Processer:
    @classmethod
    def process(
        cls, text: str, role_rules_path: str, morph_rules_path: str
    ) -> List[Dict[str, str]]:
        text = text.replace("\n", " ")
        model = get_model()
        doc = model(text)
        result_dict = []
        dep_rules = JsonProcesser.process_json(role_rules_path)
        morph_rules = JsonProcesser.process_json(morph_rules_path)
        for token in doc:
            morph = token.pos_
            if morph == "PUNCT" or morph == "SPACE":
                continue
            word = token.text
            lemma = token.lemma_
            dep = token.dep_
            role = dep_rules.get(dep, "Unknown Role")
            morphology = morph_rules.get(morph, "Unknown Morph")
            full_analisis = dict(word=word, lemma=lemma, morph=morphology, role=role)
            result_dict.append(full_analisis)

        return result_dict

    @classmethod
    def process_with_sentences(
        cls, text: str, role_rules_path: str, morph_rules_path: str
    ) -> Dict:
        """Process text: extract lemmas AND split into sentences in one spaCy pass."""
        clean = text.replace("\n", " ")
        model = get_model()
        doc = model(clean)

        
        result_dict = []
        dep_rules = JsonProcesser.process_json(role_rules_path)
        morph_rules = JsonProcesser.process_json(morph_rules_path)
        for token in doc:
            morph = token.pos_
            if morph == "PUNCT" or morph == "SPACE":
                continue
            word = token.text
            lemma = token.lemma_
            dep = token.dep_
            role = dep_rules.get(dep, "Unknown Role")
            morphology = morph_rules.get(morph, "Unknown Morph")
            full_analisis = dict(word=word, lemma=lemma, morph=morphology, role=role)
            result_dict.append(full_analisis)

        
        sentences = [sent.text.strip() for sent in doc.sents
                     if sent.text.strip() and len(sent.text.strip()) > 1]

        return {"lemmas": result_dict, "sentences": sentences}


class RtfReader:
    @classmethod
    async def read_rtf(cls, filename: str, file: IO[bytes]) -> str:
        from striprtf.striprtf import rtf_to_text
        raw = file.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        return rtf_to_text(raw).strip()





class SentenceProcessor:
    """Split text into sentences, build dependency tree, build constituency tree."""

    @classmethod
    def split_sentences(cls, text: str) -> List[str]:
        model = get_model()
        doc = model(text.replace("\n", " "))
        return [sent.text.strip() for sent in doc.sents if sent.text.strip() and len(sent.text.strip()) > 1]

    

    @classmethod
    def build_dependency_tree(cls, sentence: str) -> Dict:
        """Return {nodes: [...], edges: [...]} for dependency parse."""
        model = get_model()
        doc = model(sentence)
        nodes = []
        edges = []
        print('------------------------------------------')
        for attr in dir(doc):
            if not attr.startswith('_'):
                try:
                    value = getattr(doc, attr)
                    if not callable(value):
                        print(f"{attr}: {value}")
                except Exception:
                    pass
        print('==========================')
        for token in doc:
            if token.pos_ in ("PUNCT", "SPACE"):
                continue
            # print('------------------------------------------')
            # for attr in dir(token):
            #     if not attr.startswith('_'):
            #         try:
            #             value = getattr(token, attr)
            #             if not callable(value):
            #                 print(f"{attr}: {value}")
            #         except Exception:
            #             pass
            # print('==========================')
            nodes.append({
                "id": token.i,
                "word": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "dep": token.dep_,
                "head_id": token.head.i,
            })
            if token.dep_ != "ROOT":
                edges.append({
                    "source": token.head.i,
                    "target": token.i,
                    "label": token.dep_,
                })
        
        
        return {"nodes": nodes, "edges": edges}

    

    @classmethod
    def build_constituency_tree(cls, sentence: str) -> Dict:
        try:
            return cls._build_constituency_tree_impl(sentence)
        except Exception:
            fallback = {"label": "S", "word": sentence}
            return {"root": fallback, "bracket_notation": f"(S {sentence})"}

    @classmethod
    def _build_constituency_tree_impl(cls, sentence: str) -> Dict:
        model = get_model()
        doc = model(sentence)
        noun_chunks = {}
        chunk_token_ids = set()
        for chunk in doc.noun_chunks:
            noun_chunks[chunk.root.i] = {
                "label": "NP",
                "start": chunk.start,
                "end": chunk.end,
                "text": chunk.text,
            }
            for t in chunk:
                chunk_token_ids.add(t.i)

        root_token = None
        for token in doc:
            if token.dep_ == "ROOT":
                root_token = token
                break

        if root_token is None:
            for token in doc:
                if token.pos_ not in ("PUNCT", "SPACE"):
                    root_token = token
                    break

        if root_token is None:
            empty = {"label": "S", "children": []}
            return {"root": empty, "bracket_notation": "(S)"}

        children_by_head = {}
        for t in doc:
            if t.dep_ == "punct" or t.pos_ == "SPACE":
                continue
            children_by_head.setdefault(t.head.i, []).append(t)

        
        visited = set()
        visited.add(root_token.i)
        for t in doc:
            if t.i in chunk_token_ids and t.i not in noun_chunks:
                visited.add(t.i)

        
        s_children = []
        vp_children = []

        for child in children_by_head.get(root_token.i, []):
            if child.i in visited:
                continue
            if child.dep_ in ("nsubj", "nsubjpass", "csubj"):
                
                s_children.append(
                    cls._build_constituent_subtree(child, doc, noun_chunks,
                                                   children_by_head, visited, 0)
                )
            else:
                
                vp_children.append(
                    cls._build_constituent_subtree(child, doc, noun_chunks,
                                                   children_by_head, visited, 0)
                )

        
        if vp_children:
            vp_node = {"label": "VP", "word": root_token.text, "children": vp_children}
        else:
            vp_node = {"label": "VP", "word": root_token.text}
        s_children.append(vp_node)

        tree = {"label": "S", "children": s_children or None}
        bracket = cls._to_bracket(tree)
        return {"root": tree, "bracket_notation": bracket}

    @classmethod
    def _build_constituent_subtree(
        cls, token: Token, doc: Doc, noun_chunks: dict,
        children_by_head: Dict[int, List[Token]] = None,
        visited: set = None, depth: int = 0
    ) -> dict:
        """Recursively build a constituent subtree rooted at *token*."""
        if visited is None:
            visited = set()
        if token.i in visited or depth > 50:
            return {"label": token.pos_, "word": token.text}
        visited.add(token.i)

        if children_by_head is None:
            children_by_head = {}
            for t in doc:
                if t.dep_ == "punct" or t.pos_ == "SPACE":
                    continue
                children_by_head.setdefault(t.head.i, []).append(t)

        my_children = children_by_head.get(token.i, [])

        
        if token.i in noun_chunks:
            nc = noun_chunks[token.i]
            return {"label": "NP", "word": nc["text"]}

        
        if token.pos_ in ("VERB", "AUX"):
            vp_children = []
            for child in my_children:
                if child.i in visited:
                    continue
                if child.dep_ in ("nsubj", "nsubjpass", "csubj"):
                    continue
                vp_children.append(
                    cls._build_constituent_subtree(child, doc, noun_chunks,
                                                   children_by_head, visited, depth + 1)
                )
            return {"label": "VP", "word": token.text, "children": vp_children or None}

        
        if token.dep_ == "prep" or token.pos_ == "ADP":
            pp_children = []
            for child in my_children:
                if child.i in visited:
                    continue
                pp_children.append(
                    cls._build_constituent_subtree(child, doc, noun_chunks,
                                                   children_by_head, visited, depth + 1)
                )
            return {"label": "PP", "word": token.text, "children": pp_children or None}

        
        if token.pos_ == "ADJ":
            adj_children = []
            for child in my_children:
                if child.i in visited:
                    continue
                adj_children.append(
                    cls._build_constituent_subtree(child, doc, noun_chunks,
                                                   children_by_head, visited, depth + 1)
                )
            return {"label": "AdjP", "word": token.text, "children": adj_children or None}

        
        if token.pos_ == "ADV":
            adv_children = []
            for child in my_children:
                if child.i in visited:
                    continue
                adv_children.append(
                    cls._build_constituent_subtree(child, doc, noun_chunks,
                                                   children_by_head, visited, depth + 1)
                )
            return {"label": "AdvP", "word": token.text, "children": adv_children or None}

        
        return {"label": token.pos_, "word": token.text}

    @classmethod
    def _to_bracket(cls, node: dict) -> str:
        """Convert tree to Penn Treebank bracket notation."""
        label = node["label"]
        word = node.get("word")
        children = node.get("children")
        if not children:
            if word:
                return f"({label} {word})"
            return f"({label})"
        parts = []
        if word:
            parts.append(f"({label} {word})")
        for c in children:
            parts.append(cls._to_bracket(c))
        if word:
            return " ".join(parts)
        child_str = " ".join(parts)
        return f"({label} {child_str})"

    @classmethod
    def analyze_sentence(cls, sentence: str) -> Dict:
        """Full analysis: dep tree + constituency tree."""
        dep = cls.build_dependency_tree(sentence)
        const = cls.build_constituency_tree(sentence)
        return {
            "sentence": sentence,
            "dependency_tree": dep,
            "constituency_tree": const,
        }

    

    POS_EXPLANATIONS = {
        "NOUN": "существительное",
        "VERB": "глагол",
        "ADJ": "прилагательное",
        "ADV": "наречие",
        "ADP": "предлог",
        "AUX": "вспомогательный глагол",
        "DET": "артикль / определитель",
        "PRON": "местоимение",
        "CONJ": "союз",
        "CCONJ": "сочинительный союз",
        "SCONJ": "подчинительный союз",
        "NUM": "числительное",
        "PART": "частица",
        "INTJ": "междометие",
        "PROPN": "имя собственное",
        "PUNCT": "пунктуация",
        "SYM": "символ",
        "X": "прочее",
    }

    DEP_EXPLANATIONS = {
        "ROOT": "главный глагол / сказуемое",
        "nsubj": "подлежащее (действительное)",
        "nsubjpass": "подлежащее (страдательное)",
        "dobj": "прямое дополнение",
        "iobj": "косвенное дополнение",
        "pobj": "дополнение предлога",
        "attr": "атрибут",
        "csubj": "придаточное-подлежащее",
        "amod": "определение (прилагательное)",
        "advmod": "обстоятельство (наречие)",
        "nummod": "числительное-модификатор",
        "npadvmod": "обстоятельство (сущ.)",
        "neg": "отрицание",
        "det": "артикль / детерминатор",
        "poss": "притяжательный модификатор",
        "compound": "составное слово",
        "prep": "предложный модификатор",
        "agent": "агент (кем/чем)",
        "cc": "сочинительный союз",
        "mark": "маркер (подчинение)",
        "conj": "однородный член",
        "advcl": "обстоятельственное придаточное",
        "ccomp": "придаточное-дополнение",
        "xcomp": "открытое придаточное-дополнение",
        "acl": "придаточное-определение",
        "relcl": "придаточное определительное",
        "parataxis": "парентезис / вставная конструкция",
        "aux": "вспомогательный глагол",
        "auxpass": "вспомогательный (страдательный)",
        "cop": "связка",
        "appos": "приложение",
        "expl": "формальное подлежащее",
        "fixed": "устойчивое словосочетание",
        "flat": "составное имя",
        "punct": "пунктуация",
        "dep": "неопределённая зависимость",
        "discourse": "дискурсивный элемент",
        "intj": "междометие",
        "vocative": "обращение",
        "meta": "мета-модификатор",
    }

    CONSTITUENT_EXPLANATIONS = {
        "S": "предложение (Sentence)",
        "NP": "именная группа (Noun Phrase)",
        "VP": "глагольная группа (Verb Phrase)",
        "PP": "предложная группа (Prepositional Phrase)",
        "AdjP": "группа прилагательного (Adjective Phrase)",
        "AdvP": "группа наречия (Adverb Phrase)",
        "ADJ": "прилагательное",
        "ADV": "наречие",
        "ADP": "предлог",
        "AUX": "вспомогательный глагол",
        "DET": "артикль",
        "NOUN": "существительное",
        "NUM": "числительное",
        "PRON": "местоимение",
        "PROPN": "имя собственное",
        "VERB": "глагол",
        "PART": "частица",
        "CCONJ": "сочинительный союз",
        "SCONJ": "подчинительный союз",
    }

    @classmethod
    def get_pos_ru(cls, pos: str) -> str:
        return cls.POS_EXPLANATIONS.get(pos, pos)

    @classmethod
    def get_dep_ru(cls, dep: str) -> str:
        return cls.DEP_EXPLANATIONS.get(dep, dep)

    @classmethod
    def get_constituent_ru(cls, label: str) -> str:
        return cls.CONSTITUENT_EXPLANATIONS.get(label, label)
