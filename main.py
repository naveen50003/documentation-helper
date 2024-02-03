from typing import Set

from backend.core import run_llm, delete_records
from ingestion import ingest_docs
import streamlit as st
from streamlit_chat import message

if "isDeleteSuccess" not in st.session_state:
    st.session_state["isDeleteSuccess"] = False

def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"

    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

def clear_cache():
    records = delete_records()
    print(f"Delete records {len(records)}")
    if not len(records):
        st.session_state["user_prompt_history"] = []
        st.session_state["chat_answers_history"] = []
        st.session_state["chat_history"] = []
        st.session_state["isDeleteSuccess"] = True
        st.session_state.prompt= ''

def change_file_upload():
    st.toast('Uploading...')
    print("entered file change")

st.header("Chat with PDF Bot")
st.button("Clear Cache", type="primary", on_click=clear_cache)
pdf = st.file_uploader(label='Upload the PDF', type='pdf', on_change=change_file_upload)

if pdf:
    if "user_prompt_history" not in st.session_state:
        st.session_state["user_prompt_history"] = []

    if "chat_answers_history" not in st.session_state:
        st.session_state["chat_answers_history"] = []

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    st.text_input("Prompt", key="prompt",placeholder="Enter your prompt here...")
    ingestResponse = ingest_docs(pdf, st.session_state.prompt, st.session_state.isDeleteSuccess)
    if ingestResponse:
        toast = st.toast('Start searching...')
    print(st.session_state["isDeleteSuccess"])
    if st.session_state.prompt and (st.session_state["isDeleteSuccess"] == False):
        with st.spinner("Generating response..."):
            generated_response = run_llm(query=st.session_state.prompt, chat_history=st.session_state['chat_history'])
            # sources= set(
            #     [doc.metadata["source"] for doc in generated_response["source_documents"]]
            # )

            # formatted_response = (
            #     f"{generated_response['answer']} \n \n {create_sources_string(sources)}"
            # )

            formatted_response = (
                f"{generated_response['answer']}"
            )

            st.session_state["user_prompt_history"].append(st.session_state.prompt)
            st.session_state["chat_answers_history"].append(formatted_response)
            st.session_state["chat_history"].append((st.session_state.prompt, generated_response['answer']))
    if st.session_state["chat_answers_history"]:
        for generated_response, user_query in zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"]):
            message(user_query,is_user=True)
            message(generated_response)

