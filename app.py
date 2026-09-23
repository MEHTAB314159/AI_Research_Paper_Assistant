# import streamlit as st
# import numpy as np

# from modules.pdf_processor import (
#     extract_pdf_pages
# )

# from modules.text_processor import (
#     create_chunks
# )

# from modules.embedding_engine import (
#     EmbeddingEngine
# )

# from modules.hybrid_search import (
#     HybridSearch
# )

# from modules.qa_engine import (
#     QAEngine
# )

# from modules.ner_engine import (
#     NEREngine
# )

# from config import (
#     TOP_K_RETRIEVAL,
#     TOP_K_FINAL,
#     RELEVANCE_THRESHOLD
# )


# st.set_page_config(
#     page_title="AI Research Paper Assistant",
#     page_icon="📚",
#     layout="wide"
# )


# @st.cache_resource
# def load_engines():

#     embedding_engine = (
#         EmbeddingEngine()
#     )

#     qa_engine = QAEngine()

#     ner_engine = NEREngine()

#     return (
#         embedding_engine,
#         qa_engine,
#         ner_engine
#     )


# (
#     embedding_engine,
#     qa_engine,
#     ner_engine
# ) = load_engines()


# st.title(
#     "📚 AI Research Paper Semantic Search "
#     "& Question Answering System"
# )

# st.write(
#     """
#     Upload research papers and ask questions
#     using semantic search, hybrid retrieval,
#     question answering and named entity recognition.
#     """
# )


# with st.sidebar:

#     st.header("🔧 NLP Components")

#     st.write("✓ PDF Text Extraction")
#     st.write("✓ Text Preprocessing")
#     st.write("✓ Intelligent Chunking")
#     st.write("✓ TF-IDF Search")
#     st.write("✓ Semantic Embeddings")
#     st.write("✓ FAISS Search")
#     st.write("✓ Hybrid Retrieval")
#     st.write("✓ Question Answering")
#     st.write("✓ Named Entity Recognition")


# uploaded_files = st.file_uploader(
#     "📄 Upload Research Papers",
#     type=["pdf"],
#     accept_multiple_files=True
# )


# if uploaded_files:

#     if st.button(
#         "🚀 Process Research Papers",
#         type="primary"
#     ):

#         all_chunks = []

#         progress = st.progress(0)

#         for file_number, pdf_file in enumerate(
#             uploaded_files
#         ):

#             pages = extract_pdf_pages(
#                 pdf_file
#             )

#             chunks = create_chunks(
#                 pages,
#                 pdf_file.name
#             )

#             all_chunks.extend(chunks)

#             progress.progress(
#                 (file_number + 1)
#                 / len(uploaded_files)
#             )

#         if not all_chunks:

#             st.error(
#                 "No readable text found."
#             )

#             st.stop()

#         st.session_state[
#             "chunks"
#         ] = all_chunks

#         texts = [
#             item["text"]
#             for item in all_chunks
#         ]

#         with st.spinner(
#             "Creating semantic embeddings..."
#         ):

#             embeddings = (
#                 embedding_engine
#                 .create_embeddings(texts)
#             )

#             embedding_engine.build_index(
#                 embeddings
#             )

#         with st.spinner(
#             "Building TF-IDF index..."
#         ):

#             hybrid_engine = HybridSearch()

#             hybrid_engine.build_tfidf(
#                 texts
#             )

#             st.session_state[
#                 "hybrid_engine"
#             ] = hybrid_engine

#         st.success(
#             f"Processed {len(uploaded_files)} "
#             f"research papers and "
#             f"{len(all_chunks)} text chunks."
#         )


# if "chunks" in st.session_state:

#     st.divider()

#     st.header(
#         "🔎 Ask Your Research Question"
#     )

#     question = st.text_input(
#         "Enter your question",
#         placeholder=(
#             "Example: What techniques are "
#             "used for sentiment analysis?"
#         )
#     )

#     top_k = st.slider(
#         "Number of retrieved passages",
#         3,
#         10,
#         TOP_K_RETRIEVAL
#     )

#     if st.button(
#         "🔍 Search & Answer",
#         type="primary"
#     ):

#         if not question.strip():

#             st.warning(
#                 "Please enter a question."
#             )

#             st.stop()

#         chunks = st.session_state[
#             "chunks"
#         ]

#         hybrid_engine = st.session_state[
#             "hybrid_engine"
#         ]

#         texts = [
#             item["text"]
#             for item in chunks
#         ]

#         semantic_scores, semantic_indices = (
#             embedding_engine.search(
#                 question,
#                 top_k
#             )
#         )

#         tfidf_scores = (
#             hybrid_engine.search_tfidf(
#                 question
#             )
#         )

#         selected_indices = list(
#             set(
#                 semantic_indices.tolist()
#             )
#         )

#         final_scores = []

#         for index in selected_indices:

#             semantic_score = 0

#             positions = np.where(
#                 semantic_indices == index
#             )[0]

#             if len(positions) > 0:

#                 semantic_score = (
#                     semantic_scores[
#                         positions[0]
#                     ]
#                 )

#             combined_score = (
#                 0.65 * semantic_score
#                 +
#                 0.35 * tfidf_scores[index]
#             )

#             final_scores.append(
#                 (
#                     index,
#                     combined_score
#                 )
#             )

#         final_scores.sort(
#             key=lambda x: x[1],
#             reverse=True
#         )

#         selected = final_scores[
#             :TOP_K_FINAL
#         ]

#         retrieved_chunks = []

#         for index, score in selected:

#             item = chunks[index].copy()

#             item[
#                 "retrieval_score"
#             ] = float(score)

#             retrieved_chunks.append(
#                 item
#             )

#         with st.spinner(
#             "Finding the answer..."
#         ):

#             answer = qa_engine.answer(
#                 question,
#                 retrieved_chunks
#             )

#         st.subheader(
#             "💡 Answer"
#         )

#         if answer:

#             st.success(
#                 answer["answer"]
#             )

#             col1, col2, col3 = st.columns(3)

#             with col1:

#                 st.metric(
#                     "QA Confidence",
#                     f"{answer['score']:.2f}"
#                 )

#             with col2:

#                 st.metric(
#                     "Source Page",
#                     answer["page"]
#                 )

#             with col3:

#                 st.write("📄 Source")

#                 st.write(
#                     answer["source"]
#                 )

#         else:

#             st.warning(
#                 "No answer found."
#             )

#         st.divider()

#         st.subheader(
#             "🧠 Named Entities"
#         )

#         combined_text = " ".join(
#             item["text"]
#             for item in retrieved_chunks
#         )

#         entities = (
#             ner_engine.extract_entities(
#                 combined_text
#             )
#         )

#         if entities:

#             grouped = {}

#             for entity in entities:

#                 label = entity["label"]

#                 if label not in grouped:

#                     grouped[label] = set()

#                 grouped[label].add(
#                     entity["text"]
#                 )

#             columns = st.columns(4)

#             column_number = 0

#             for label, values in grouped.items():

#                 with columns[
#                     column_number % 4
#                 ]:

#                     st.markdown(
#                         f"**{label}**"
#                     )

#                     for value in list(values)[:10]:

#                         st.write(
#                             f"• {value}"
#                         )

#                 column_number += 1

#         else:

#             st.info(
#                 "No named entities detected."
#             )

#         st.divider()

#         st.subheader(
#             "📑 Retrieved Sources"
#         )

#         for rank, item in enumerate(
#             retrieved_chunks,
#             start=1
#         ):

#             with st.expander(
#                 f"{rank}. {item['source']} "
#                 f"— Page {item['page']}"
#             ):

#                 st.write(
#                     item["text"]
#                 )

#                 st.write(
#                     "Relevance Score: "
#                     f"{item['retrieval_score']:.4f}"
#                 )

import streamlit as st
import numpy as np

from modules.pdf_processor import (
    extract_pdf_pages
)

from modules.text_processor import (
    create_chunks
)

from modules.embedding_engine import (
    EmbeddingEngine
)

from modules.hybrid_search import (
    HybridSearch
)

from modules.qa_engine import (
    QAEngine
)

from modules.ner_engine import (
    NEREngine
)

from config import (
    TOP_K_RETRIEVAL,
    TOP_K_FINAL,
    RELEVANCE_THRESHOLD
)


st.set_page_config(
    page_title="AI Research Paper Assistant",
    page_icon="📚",
    layout="wide"
)


@st.cache_resource
def load_engines():

    embedding_engine = EmbeddingEngine()

    qa_engine = QAEngine()

    ner_engine = NEREngine()

    return (
        embedding_engine,
        qa_engine,
        ner_engine
    )


(
    embedding_engine,
    qa_engine,
    ner_engine
) = load_engines()


st.title(
    "📚 AI Research Paper Semantic Search "
    "& Question Answering System"
)

st.write(
    """
    Upload research papers and ask questions
    using semantic search, hybrid retrieval,
    question answering and named entity recognition.
    """
)


with st.sidebar:

    st.header("🔧 NLP Components")

    st.write("✓ PDF Text Extraction")
    st.write("✓ Text Preprocessing")
    st.write("✓ Intelligent Chunking")
    st.write("✓ TF-IDF Search")
    st.write("✓ Semantic Embeddings")
    st.write("✓ FAISS Search")
    st.write("✓ Hybrid Retrieval")
    st.write("✓ Question Answering")
    st.write("✓ Named Entity Recognition")


uploaded_files = st.file_uploader(
    "📄 Upload Research Papers",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    if st.button(
        "🚀 Process Research Papers",
        type="primary"
    ):

        all_chunks = []

        progress = st.progress(0)

        for file_number, pdf_file in enumerate(
            uploaded_files
        ):

            pages = extract_pdf_pages(
                pdf_file
            )

            chunks = create_chunks(
                pages,
                pdf_file.name
            )

            all_chunks.extend(chunks)

            progress.progress(
                (file_number + 1)
                / len(uploaded_files)
            )

        if not all_chunks:

            st.error(
                "No readable text found."
            )

            st.stop()

        st.session_state[
            "chunks"
        ] = all_chunks

        texts = [
            item["text"]
            for item in all_chunks
        ]

        with st.spinner(
            "Creating semantic embeddings..."
        ):

            embeddings = (
                embedding_engine
                .create_embeddings(texts)
            )

            embedding_engine.build_index(
                embeddings
            )

        with st.spinner(
            "Building TF-IDF index..."
        ):

            hybrid_engine = HybridSearch()

            hybrid_engine.build_tfidf(
                texts
            )

            st.session_state[
                "hybrid_engine"
            ] = hybrid_engine

        st.success(
            f"Processed {len(uploaded_files)} "
            f"research papers and "
            f"{len(all_chunks)} text chunks."
        )


if "chunks" in st.session_state:

    st.divider()

    st.header(
        "🔎 Ask Your Research Question"
    )

    question = st.text_input(
        "Enter your question",
        placeholder=(
            "Example: What techniques are "
            "used for sentiment analysis?"
        )
    )

    top_k = st.slider(
        "Number of retrieved passages",
        3,
        10,
        TOP_K_RETRIEVAL
    )

    if st.button(
        "🔍 Search & Answer",
        type="primary"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

            st.stop()

        chunks = st.session_state[
            "chunks"
        ]

        hybrid_engine = st.session_state[
            "hybrid_engine"
        ]

        texts = [
            item["text"]
            for item in chunks
        ]

        semantic_scores, semantic_indices = (
            embedding_engine.search(
                question,
                top_k
            )
        )

        tfidf_scores = (
            hybrid_engine.search_tfidf(
                question
            )
        )

        selected_indices = list(
            set(
                semantic_indices.tolist()
            )
        )

        final_scores = []

        for index in selected_indices:

            semantic_score = 0

            positions = np.where(
                semantic_indices == index
            )[0]

            if len(positions) > 0:

                semantic_score = (
                    semantic_scores[
                        positions[0]
                    ]
                )

            combined_score = (
                0.65 * semantic_score
                +
                0.35 * tfidf_scores[index]
            )

            final_scores.append(
                (
                    index,
                    combined_score
                )
            )

        final_scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        if not final_scores:

            st.warning(
                "This information could not be found "
                "in the uploaded research papers."
            )

            st.stop()

        best_relevance = final_scores[0][1]

        if best_relevance < RELEVANCE_THRESHOLD:

            st.warning(
                "This information could not be found "
                "in the uploaded research papers."
            )

            st.info(
                "Please ask a question related to "
                "the uploaded research papers."
            )

            st.stop()

        selected = final_scores[
            :TOP_K_FINAL
        ]

        retrieved_chunks = []

        for index, score in selected:

            item = chunks[index].copy()

            item[
                "retrieval_score"
            ] = float(score)

            retrieved_chunks.append(
                item
            )

        with st.spinner(
            "Finding the answer..."
        ):

            answer = qa_engine.answer(
                question,
                retrieved_chunks
            )

        st.subheader(
            "💡 Answer"
        )

        if answer:

            st.success(
                answer["answer"]
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "QA Confidence",
                    f"{answer['score']:.2f}"
                )

            with col2:

                st.metric(
                    "Source Page",
                    answer["page"]
                )

            with col3:

                st.write("📄 Source")

                st.write(
                    answer["source"]
                )

        else:

            st.warning(
                "No answer found."
            )

        st.divider()

        st.subheader(
            "🧠 Named Entities"
        )

        combined_text = " ".join(
            item["text"]
            for item in retrieved_chunks
        )

        entities = (
            ner_engine.extract_entities(
                combined_text
            )
        )

        if entities:

            grouped = {}

            for entity in entities:

                label = entity["label"]

                if label not in grouped:

                    grouped[label] = set()

                grouped[label].add(
                    entity["text"]
                )

            columns = st.columns(4)

            column_number = 0

            for label, values in grouped.items():

                with columns[
                    column_number % 4
                ]:

                    st.markdown(
                        f"**{label}**"
                    )

                    for value in list(values)[:10]:

                        st.write(
                            f"• {value}"
                        )

                column_number += 1

        else:

            st.info(
                "No named entities detected."
            )

        st.divider()

        st.subheader(
            "📑 Retrieved Sources"
        )

        for rank, item in enumerate(
            retrieved_chunks,
            start=1
        ):

            with st.expander(
                f"{rank}. {item['source']} "
                f"— Page {item['page']}"
            ):

                st.write(
                    item["text"]
                )

                st.write(
                    "Relevance Score: "
                    f"{item['retrieval_score']:.4f}"
                )