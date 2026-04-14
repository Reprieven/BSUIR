import streamlit as st
import requests
import pandas as pd
import graphviz


st.set_page_config(
    page_title="Лемматизатор Текстов",
    layout="wide",
    initial_sidebar_state="expanded"
)


API_URL = "http://127.0.0.1:8000"


if "selected_text_id" not in st.session_state:
    st.session_state.selected_text_id = None
if "lemma_offset" not in st.session_state:
    st.session_state.lemma_offset = 0
if "lemma_limit" not in st.session_state:
    st.session_state.lemma_limit = 100
if "stats_offset" not in st.session_state:
    st.session_state.stats_offset = 0
if "stats_limit" not in st.session_state:
    st.session_state.stats_limit = 100



def get_all_texts():
    try:
        response = requests.get(f"{API_URL}/text/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка получения списка текстов: {e}")
        return []

def upload_text_file(uploaded_file):
    try:
        files = {
            "new_text": (uploaded_file.name, uploaded_file.getvalue(), "application/rtf")
        }
        response = requests.post(f"{API_URL}/text/add", files=files)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка загрузки файла: {e}")
        return None

def get_text_details(text_id):
    try:
        response = requests.get(f"{API_URL}/text/{text_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка получения деталей текста: {e}")
        return None

def delete_text(text_id):
    try:
        response = requests.post(f"{API_URL}/text/delete/{text_id}")
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Ошибка удаления: {e}")
        return False

def update_text_content(text_id, new_text_content):
    try:
        payload = {"text": new_text_content}
        response = requests.post(f"{API_URL}/text/update/{text_id}", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка обновления текста: {e}")
        return None

def get_lemmas(text_id, search=None, exact_match=False, checkbox=False, limit=100, offset=0):
    try:
        params = {k: v for k, v in {
            "search": search,
            "exact_match": exact_match,
            "checkbox": checkbox,
            "limit": limit,
            "offset": offset
        }.items() if v is not None}
        response = requests.get(f"{API_URL}/text/{text_id}/lemma/", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка получения лемм: {e}")
        return []

def add_lemma(text_id, word, lemma, morph, role):
    try:
        data = {"word": word, "lemma": lemma, "morph": morph, "role": role}
        response = requests.post(f"{API_URL}/text/{text_id}/lemma/add", data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка добавления леммы: {e}")
        return None

def export_lemmas(text_id, search=None, exact_match=False, checkbox=False, limit=100, offset=0):
    try:
        params = {k: v for k, v in {
            "search": search,
            "exact_match": exact_match,
            "checkbox": checkbox,
            "limit": limit,
            "offset": offset
        }.items() if v is not None}
        response = requests.get(f"{API_URL}/text/{text_id}/lemma/export/txt", params=params)
        response.raise_for_status()
        return response.content, response.headers.get("Content-Disposition", "attachment; filename=lemmas.txt")
    except Exception as e:
        st.error(f"Ошибка экспорта: {e}")
        return None, None

def get_lemmas_count():
    try:
        response = requests.get(f"{API_URL}/text/{0}/lemma/count/words")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка получения статистики: {e}")
        return []

def get_global_stats():
    try:
        response = requests.get(f"{API_URL}/text/0/lemma/count/all")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка получения глобальной статистики: {e}")
        return None



def get_sentences(text_id):
    try:
        response = requests.get(f"{API_URL}/text/{text_id}/sentence/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка получения предложений: {e}")
        return []

def analyze_sentence(text_id, sentence_id):
    try:
        response = requests.get(f"{API_URL}/text/{text_id}/sentence/{sentence_id}/analyze")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка анализа предложения: {e}")
        return None

def analyze_custom_sentence(text_id, text):
    try:
        response = requests.post(
            f"{API_URL}/text/{text_id}/sentence/analyze-custom",
            json={"text": text}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка анализа: {e}")
        return None




POS_RU = {
    "NOUN": "существительное", "VERB": "глагол", "ADJ": "прилагательное",
    "ADV": "наречие", "ADP": "предлог", "AUX": "вспомогательный глагол",
    "DET": "артикль / определитель", "PRON": "местоимение",
    "CCONJ": "сочинительный союз", "SCONJ": "подчинительный союз",
    "NUM": "числительное", "PART": "частица", "INTJ": "междометие",
    "PROPN": "имя собственное", "SYM": "символ", "X": "прочее",
}

DEP_RU = {
    "ROOT": "главный глагол / сказуемое", "nsubj": "подлежащее (действ.)",
    "nsubjpass": "подлежащее (страд.)", "dobj": "прямое дополнение",
    "iobj": "косвенное дополнение", "pobj": "дополнение предлога",
    "attr": "атрибут", "csubj": "придаточное-подлежащее",
    "amod": "определение (прилагат.)", "advmod": "обстоятельство (нареч.)",
    "nummod": "числительное-модиф.", "neg": "отрицание",
    "det": "артикль / детерминатор", "poss": "притяжательный модификатор",
    "compound": "составное слово", "prep": "предложный модификатор",
    "agent": "агент", "cc": "сочинит. союз", "mark": "маркер подчинения",
    "conj": "однородный член", "advcl": "обстоятельств. придаточное",
    "ccomp": "придаточное-дополнение", "xcomp": "открытое придаточное",
    "acl": "придаточное-определение", "relcl": "определит. придаточное",
    "aux": "вспомогат. глагол", "auxpass": "вспомогат. (страд.)",
    "cop": "связка", "appos": "приложение", "expl": "формальн. подлежащее",
    "punct": "пунктуация", "fixed": "устойчивое словосочетание",
    "flat": "составное имя", "parataxis": "парентезис",
    "dep": "неопределённая зависимость", "discourse": "дискурсивный элемент",
    "intj": "междометие", "vocative": "обращение",
}

CONST_RU = {
    "S": "предложение (Sentence)", "NP": "именная группа (Noun Phrase)",
    "VP": "глагольная группа (Verb Phrase)", "PP": "предложная группа (Prep. Phrase)",
    "AdjP": "группа прилагательного (AdjP)", "AdvP": "группа наречия (AdvP)",
}



def build_dep_graphviz(dep_tree: dict) -> str:
    """Build DOT source string from dependency tree data."""
    g = graphviz.Digraph("dep", format="png",
                         graph_attr={"rankdir": "LR", "fontsize": "12"},
                         node_attr={"shape": "box", "style": "filled",
                                    "fillcolor": "#E8F4FD", "fontname": "Arial"},
                         edge_attr={"fontname": "Arial", "fontsize": "10"})
    for n in dep_tree["nodes"]:
        label = f"{n['word']}\n({n['pos']})"
        g.node(str(n["id"]), label=label)
    for e in dep_tree["edges"]:
        g.edge(str(e["source"]), str(e["target"]), label=e["label"])
    return g.source


def build_constituency_graphviz(tree: dict) -> str:
    """Build DOT source string from constituency tree data."""
    g = graphviz.Digraph("const", format="png",
                         graph_attr={"rankdir": "TB", "fontsize": "12", "splines": "ortho"},
                         node_attr={"shape": "ellipse", "style": "filled",
                                    "fillcolor": "#FFF3E0", "fontname": "Arial"},
                         edge_attr={"fontname": "Arial"})
    counter = [0]

    def add_nodes(node, parent_id=None):
        if node is None:
            return
        nid = f"n{counter[0]}"
        counter[0] += 1
        label = node.get("label", "?")
        if node.get("word"):
            label = f"{label}\n{node['word']}"
        color = "#C8E6C9" if node.get("word") else "#FFF3E0"
        shape = "box" if node.get("word") else "ellipse"
        g.node(nid, label=label, fillcolor=color, shape=shape)
        if parent_id is not None:
            g.edge(parent_id, nid)
        for child in (node.get("children") or []):
            add_nodes(child, nid)

    root = tree.get("root", tree) if isinstance(tree, dict) else tree
    add_nodes(root)
    return g.source


def tree_to_text(node: dict, indent: int = 0) -> str:
    """Convert constituency tree to indented text representation."""
    prefix = "  " * indent
    label = node["label"]
    word = node.get("word")
    children = node.get("children")

    if not children:
        if word:
            return f"{prefix}{label}: {word}"
        return f"{prefix}{label}"

    lines = [f"{prefix}{label}"]
    for child in (children or []):
        lines.append(tree_to_text(child, indent + 1))
    return "\n".join(lines)




st.title("Система управления леммами и текстами")


with st.sidebar:
    st.header("Навигация")
    mode = st.radio(
        "Выберите режим работы:",
        ["Управление текстами", "Анализ лемм", "Статистика лемм", "Предложения"],
        index=0
    )
    st.divider()
    st.caption(f"API: {API_URL}")
    if st.button("Обновить данные"):
        st.rerun()




if mode == "Управление текстами":
    st.header("Управление текстами")
    col_upload, col_list = st.columns([1, 2])
    
    with col_upload:
        st.subheader("Загрузка нового файла")
        uploaded_file = st.file_uploader("Выберите .rtf", type=["rtf"])
        if uploaded_file is not None:
            st.info(f"Файл: {uploaded_file.name} ({uploaded_file.size} bytes)")
            if st.button("Загрузить и обработать"):
                with st.spinner("Обработка файла..."):
                    result = upload_text_file(uploaded_file)
                    if result:
                        st.success(f"Текст '{result.get('name')}' успешно добавлен!")
                        st.rerun()

    with col_list:
        st.subheader("Список текстов")
        texts = get_all_texts()
        if texts:
            df_texts = pd.DataFrame(texts)
            if not df_texts.empty:
                display_df = df_texts[['id', 'name', 'date']].copy()
                display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%Y-%m-%d %H:%M')
                st.dataframe(display_df, width='stretch', hide_index=True)
                
                text_options = {f"{t['id']}: {t['name']}": t['id'] for t in texts}
                selected_label = st.selectbox("Выберите текст для просмотра/редактирования:", list(text_options.keys()), key="manage_text_select")
                
                if selected_label:
                    selected_id = text_options[selected_label]
                    st.session_state.selected_text_id = selected_id
                    text_details = get_text_details(selected_id)
                    
                    if text_details:
                        st.divider()
                        st.subheader(f"Редактирование: {text_details['name']}")
                        with st.form("edit_text_form"):
                            edited_text = st.text_area("Содержимое текста", value=text_details['text'], height=300)
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                submit_edit = st.form_submit_button("Сохранить изменения", width='stretch')
                            with col_btn2:
                                submit_delete = st.form_submit_button("Удалить текст", type="primary", width='stretch')
                            
                            if submit_edit and edited_text != text_details['text']:
                                with st.spinner("Сохранение..."):
                                    update_text_content(selected_id, edited_text)
                                    st.success("Текст обновлен!")
                                    st.rerun()
                            if submit_delete and st.checkbox("Подтвердите удаление"):
                                if delete_text(selected_id):
                                    st.success("Текст удален")
                                    st.session_state.selected_text_id = None
                                    st.rerun()
        else:
            st.info("Список текстов пуст. Загрузите файл слева.")




elif mode == "Анализ лемм":
    st.header("Анализ лемм")
    
    texts = get_all_texts()
    text_options = {f"{t['id']}: {t['name']}": t['id'] for t in texts}
    
    if not text_options:
        st.warning("Нет доступных текстов. Перейдите в режим 'Управление текстами'.")
        st.stop()
    
    selected_label = st.selectbox("Выберите файл для анализа:", list(text_options.keys()), key="lemma_text_select")
    current_text_id = text_options[selected_label]
    
    if st.session_state.get("last_analyzed_text_id") != current_text_id:
        st.session_state.lemma_offset = 0
        st.session_state.last_analyzed_text_id = current_text_id

    st.divider()
    
    with st.expander("Параметры фильтрации", expanded=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            search_query = st.text_input("Поиск (слово/лемма)", value="", key="lemma_search")
        with col_f2:
            exact_match = st.checkbox("Точное совпадение", value=False, key="lemma_exact")
        with col_f3:
            group_by_lemma = st.checkbox("Группировать по лемме", value=False, key="lemma_group")
        
        col_f4, col_f5 = st.columns(2)
        with col_f4:
            limit = st.number_input("Лимит", min_value=1, max_value=1000, value=st.session_state.lemma_limit, key="lemma_limit_input")
        
        filters_changed = (
            st.session_state.get("prev_search") != search_query or
            st.session_state.get("prev_exact") != exact_match or
            st.session_state.get("prev_group") != group_by_lemma or
            st.session_state.get("prev_limit") != limit
        )
        
        if filters_changed:
            st.session_state.lemma_offset = 0
            st.session_state.prev_search = search_query
            st.session_state.prev_exact = exact_match
            st.session_state.prev_group = group_by_lemma
            st.session_state.prev_limit = limit
        
        with col_f5:
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                if st.button("Назад", key="lemma_prev"):
                    st.session_state.lemma_offset = max(0, st.session_state.lemma_offset - limit)
                    st.rerun()
            with p_col2:
                if st.button("Вперёд", key="lemma_next"):
                    st.session_state.lemma_offset += limit
                    st.rerun()
        
        offset = st.session_state.lemma_offset
        st.caption(f"Страница: {offset // limit + 1} (offset={offset})")

    action_col1, action_col2 = st.columns([1, 1])
    with action_col1:
        load_btn = st.button("Загрузить леммы", type="primary", width='stretch')
    with action_col2:
        export_data, export_filename = export_lemmas(
            current_text_id, 
            search=search_query if search_query else None, 
            exact_match=exact_match, 
            checkbox=group_by_lemma,
            limit=limit,
            offset=offset
        )
        if export_data:
            fname = export_filename.split("filename=")[-1].strip().replace('"', '') if "filename=" in (export_filename or "") else "lemmas.txt"
            st.download_button(
                label="Скачать отчёт (.txt)",
                data=export_data,
                file_name=fname,
                mime="text/plain",
                width='stretch'
            )

    if load_btn:
        with st.spinner("Загрузка данных..."):
            lemmas = get_lemmas(
                current_text_id,
                search=search_query if search_query else None,
                exact_match=exact_match,
                checkbox=group_by_lemma,
                limit=limit,
                offset=offset
            )
            if lemmas:
                df_lemmas = pd.DataFrame(lemmas)
                cols_order = ['id', 'word', 'lemma', 'morph', 'role']
                existing_cols = [c for c in cols_order if c in df_lemmas.columns]
                st.dataframe(df_lemmas[existing_cols], width='stretch', hide_index=True)
                st.success(f"Найдено записей: {len(lemmas)}")
            else:
                st.info("Леммы не найдены по заданным критериям.")

    st.divider()
    with st.expander("Добавить лемму вручную"):
        with st.form("add_lemma_form"):
            c1, c2, c3, c4 = st.columns(4)
            with c1: in_word = st.text_input("Слово (форма)")
            with c2: in_lemma = st.text_input("Лемма")
            with c3: in_morph = st.text_input("Морфология")
            with c4: in_role = st.text_input("Роль")
            submit_lemma = st.form_submit_button("Добавить", width='stretch')
            if submit_lemma and in_word and in_lemma:
                result = add_lemma(current_text_id, in_word, in_lemma, in_morph, in_role)
                if result:
                    st.success("Лемма добавлена!")




elif mode == "Статистика лемм":
    st.header("Статистика по леммам")
    
    texts = get_all_texts()
    text_options = {f"{t['id']}: {t['name']}": t['id'] for t in texts}
    
    with st.expander("Глобальная статистика по базе", expanded=True):
        if st.button("Обновить глобальную статистику", width='stretch'):
            with st.spinner("Загрузка..."):
                global_stats = get_global_stats()
                if global_stats:
                    st.session_state.global_stats = global_stats
                    st.rerun()
        
        if st.session_state.get("global_stats"):
            gs = st.session_state.global_stats
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Текстов", gs.get("texts", 0))
            m2.metric("Всего слов", gs.get("words", 0))
            m3.metric("Уникальных слов", gs.get("unique_words", 0))
            m4.metric("Лемм", gs.get("lemmas", 0))
        else:
            st.info("Нажмите кнопку выше для загрузки глобальной статистики")
    
    st.divider()
    
    st.subheader("Детальная статистика по тексту")

    with st.expander("Параметры отображения", expanded=False):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            stats_limit = st.number_input(
                "Лимит записей", 
                min_value=1, 
                max_value=1000, 
                value=st.session_state.stats_limit, 
                key="stats_limit_input"
            )
        with col_s2:
            stats_sort = st.selectbox(
                "Сортировка", 
                ["По убыванию (частые)", "По возрастанию", "По лемме (А-Я)"], 
                key="stats_sort"
            )
        
        if (st.session_state.get("prev_stats_limit") != stats_limit or 
            st.session_state.get("prev_stats_sort") != stats_sort):
            st.session_state.stats_offset = 0
            st.session_state.prev_stats_limit = stats_limit
            st.session_state.prev_stats_sort = stats_sort
        
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            if st.button("Назад", key="stats_prev"):
                st.session_state.stats_offset = max(0, st.session_state.stats_offset - stats_limit)
                st.rerun()
        with p_col2:
            if st.button("Вперёд", key="stats_next"):
                st.session_state.stats_offset += stats_limit
                st.rerun()
    
    if st.button("Загрузить статистику по тексту", type="primary", width='stretch'):
        with st.spinner("Загрузка агрегированных данных..."):
            lemmas_count = get_lemmas_count()
            
            if lemmas_count:
                df_stats = pd.DataFrame(lemmas_count)
                
                if "По убыванию" in stats_sort:
                    df_stats = df_stats.sort_values("count", ascending=False)
                elif "По возрастанию" in stats_sort:
                    df_stats = df_stats.sort_values("count", ascending=True)
                else:
                    df_stats = df_stats.sort_values("lemma", ascending=True)
                
                df_paginated = df_stats.iloc[st.session_state.stats_offset : st.session_state.stats_offset + stats_limit]
                
                st.dataframe(
                    df_paginated[['lemma', 'morph', 'role', 'count']], 
                    width='stretch', 
                    hide_index=True,
                    column_config={
                        "lemma": "Лемма",
                        "morph": "Морфология", 
                        "role": "Роль",
                        "count": st.column_config.NumberColumn("Количество", format="%d")
                    }
                )
                
                total = len(df_stats)
                current_page = st.session_state.stats_offset // stats_limit + 1
                total_pages = (total + stats_limit - 1) // stats_limit
                st.caption(f"Страница {current_page} из {total_pages} | Всего уникальных лемм: {total}")
                
                csv = df_stats.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Скачать статистику (CSV)",
                    data=csv,
                    file_name=f"lemmas_stats_text.csv",
                    mime="text/csv",
                    width='stretch'
                )
            else:
                st.warning("Статистика пуста или не загружена.")




elif mode == "Предложения":
    st.header("Анализ предложений")
    
    texts = get_all_texts()
    text_options = {f"{t['id']}: {t['name']}": t['id'] for t in texts}
    
    if not text_options:
        st.warning("Нет доступных текстов. Загрузите файл в режиме 'Управление текстами'.")
        st.stop()
    
    selected_label = st.selectbox(
        "Выберите текст:",
        list(text_options.keys()),
        key="sent_text_select"
    )
    current_text_id = text_options[selected_label]
    
    st.divider()
    
    
    with st.expander("Ввести произвольное предложение для анализа"):
        custom_input = st.text_area(
            "Введите предложение на английском языке:",
            height=80,
            key="custom_sentence_input"
        )
        if st.button("Анализировать", key="analyze_custom_btn") and custom_input.strip():
            with st.spinner("Анализ..."):
                result = analyze_custom_sentence(current_text_id, custom_input.strip())
                if result:
                    st.session_state["sentence_analysis"] = result
                    st.session_state["sentence_label"] = "[Произвольное предложение]"
    
    st.divider()
    
    
    st.subheader("Предложения текста")
    
    if st.button("Загрузить предложения", type="primary", width='stretch'):
        with st.spinner("Загрузка предложений..."):
            sentences = get_sentences(current_text_id)
            if sentences:
                st.session_state["sentences_list"] = sentences
            else:
                st.session_state["sentences_list"] = []
        st.rerun()
    
    sentences = st.session_state.get("sentences_list", [])
    
    
    sentences = [s for s in sentences if s.get("content", "").strip()]
    
    if sentences:
        st.info(f"Найдено предложений: {len(sentences)}")
        df_sent = pd.DataFrame(sentences)
        st.dataframe(
            df_sent[["index", "content"]],
            width='stretch',
            hide_index=True,
            column_config={
                "index": st.column_config.NumberColumn("№", format="%d"),
                "content": "Предложение"
            },
            height=300
        )
        
        
        sent_options = {f"{s['index']+1}. {s['content'][:80]}...": s['id'] for s in sentences}
        selected_sent_label = st.selectbox(
            "Выберите предложение для анализа:",
            list(sent_options.keys()),
            key="sent_select"
        )
        
        if st.button("Анализировать предложение", key="analyze_sent_btn"):
            sent_id = sent_options[selected_sent_label]
            with st.spinner("Синтаксический разбор..."):
                result = analyze_sentence(current_text_id, sent_id)
                if result:
                    st.session_state["sentence_analysis"] = result
                    st.session_state["sentence_label"] = selected_sent_label
    
    
    analysis = st.session_state.get("sentence_analysis")
    
    if analysis:
        st.divider()
        st.subheader(f"Разбор: {st.session_state.get('sentence_label', '')}")
        st.markdown(f"**Предложение:** {analysis['sentence']}")
        
        tab_dep, tab_const = st.tabs(["Dependency Tree", "Constituency Tree"])
        
        
        with tab_dep:
            dep = analysis["dependency_tree"]
            if dep["nodes"]:
                dep_g = build_dep_graphviz(dep)
                st.graphviz_chart(dep_g)
                
                with st.expander("Таблица зависимостей с пояснениями"):
                    dep_data = []
                    for n in dep["nodes"]:
                        head_word = next(
                            (x["word"] for x in dep["nodes"] if x["id"] == n["head_id"]),
                            "ROOT"
                        ) if n["dep"] != "ROOT" else "\u2014"
                        dep_data.append({
                            "Слово": n["word"],
                            "Лемма": n["lemma"],
                            "Часть речи": n["pos"],
                            "Часть речи (рус.)": POS_RU.get(n["pos"], n["pos"]),
                            "Зависимость": n["dep"],
                            "Зависимость (рус.)": DEP_RU.get(n["dep"], n["dep"]),
                            "Глава": head_word,
                        })
                    st.dataframe(pd.DataFrame(dep_data), width='stretch', hide_index=True)
            else:
                st.info("Нет данных для дерева зависимостей.")
        
        
        with tab_const:
            const = analysis.get("constituency_tree")
            if const and isinstance(const, dict) and const.get("root"):
                col_graph, col_text = st.columns([3, 2])
                
                with col_graph:
                    st.markdown("**Дерево составляющих (граф):**")
                    try:
                        const_g = build_constituency_graphviz(const["root"])
                        st.graphviz_chart(const_g)
                    except Exception as e:
                        st.error(f"Ошибка визуализации: {e}")
                
                with col_text:
                    st.markdown("**Текстовое представление:**")
                    text_repr = tree_to_text(const["root"])
                    st.code(text_repr, language=None)
                    
                    st.markdown("**Bracket notation:**")
                    st.code(const.get("bracket_notation", ""), language=None)

                
                found_constituents = set()
                def collect_labels(node):
                    found_constituents.add(node["label"])
                    for child in (node.get("children") or []):
                        collect_labels(child)
                collect_labels(const["root"])

                with st.expander("Пояснения составляющих"):
                    for lbl in sorted(found_constituents):
                        ru = CONST_RU.get(lbl, POS_RU.get(lbl, lbl))
                        st.markdown(f"**{lbl}** — {ru}")
            else:
                st.info("Не удалось построить дерево составляющих для данного предложения.")

        
        st.divider()
        with st.expander("Справочник терминов (части речи, зависимости, составляющие)"):
            tab_pos, tab_dep_ref, tab_const_ref = st.tabs([
                "Части речи", "Зависимости", "Составляющие"
            ])
            with tab_pos:
                pos_df = pd.DataFrame(
                    [{"Обозначение": k, "Значение (рус.)": v} for k, v in POS_RU.items()]
                )
                st.dataframe(pos_df, width='stretch', hide_index=True)
            with tab_dep_ref:
                dep_df = pd.DataFrame(
                    [{"Обозначение": k, "Значение (рус.)": v} for k, v in DEP_RU.items()]
                )
                st.dataframe(dep_df, width='stretch', hide_index=True)
            with tab_const_ref:
                const_df = pd.DataFrame(
                    [{"Обозначение": k, "Значение (рус.)": v} for k, v in CONST_RU.items()]
                )
                st.dataframe(const_df, width='stretch', hide_index=True)
