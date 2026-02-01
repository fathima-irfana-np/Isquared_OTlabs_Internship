import nest_asyncio
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Fix for nested event loops in certain environments
nest_asyncio.apply()

def setup_rag(url):
    print(f"[*] Scraping and indexing: {url}...")
    # 1. Scrape
    loader = WebBaseLoader(url)
    docs = loader.load()
    
    # 2. Chunk
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    # 3. Embed & Store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 5})

def main():
    print("--- Instant Support Agent ---")
    url = input("Enter Support URL: ").strip()
    if not url: return

    try:
        retriever = setup_rag(url)
        llm = ChatOllama(model="phi:latest", temperature=0)
        
        template = """Answer based ONLY on the provided context:
        {context}
        Question: {question}
        Answer:"""
        prompt_template = ChatPromptTemplate.from_template(template)

        print("\n[!] Knowledge Base Ready. Type 'exit' to quit.")
        
        while True:
            question = input("\nUser: ").strip()
            if question.lower() in ['exit', 'quit']: break
            
            # Retrieval & Generation
            docs = retriever.invoke(question)
            context_text = "\n\n".join(doc.page_content for doc in docs)
            
            # Simple check for context presence
            if not context_text.strip():
                print("Agent: I couldn't find relevant information on the website.")
                continue

            chain = prompt_template | llm | StrOutputParser()
            response = chain.invoke({"context": context_text, "question": question})
            
            print(f"Agent: {response}")

    except Exception as e:
        print(f"Error: {e}\nEnsure Ollama is running (`ollama serve`).")

if __name__ == "__main__":
    main()










# import streamlit as st
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.chat_models import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

# # --- Page Configuration ---
# st.set_page_config(page_title="Instant Support Agent", page_icon="🟢", layout="wide")

# # --- Sidebar ---
# with st.sidebar:
#     st.header("🟢 Settings")
    
#     # Ollama Configuration
#     model_name = st.text_input("Ollama Model", value="phi:latest", help="Ensure this model is pulled in Ollama")
#     embedding_model = st.text_input("Embedding Model", value="nomic-embed-text", help="Model used for generating embeddings")
    
#     st.markdown("---")
    
#     # URL Input
#     url = st.text_input("Enter Support URL", placeholder="https://example.com/docs")
    
#     process_btn = st.button("Process Website")
    
#     if process_btn:
#         if not url:
#             st.error("Please enter a URL!")
#         else:
#             with st.spinner("Scraping and Indexing..."):
#                 try:
#                     # Clear chat history when processing new site
#                     if "messages" in st.session_state:
#                         st.session_state.messages = []
                    
#                     # 1. Scrape
#                     loader = WebBaseLoader(url)
#                     docs = loader.load()
                    
#                     # Show scraping info
#                     st.info(f"Found {len(docs)} page(s). Extracted {sum(len(d.page_content) for d in docs)} characters.")
                    
#                     # 2. Chunk
#                     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#                     splits = text_splitter.split_documents(docs)
                    
#                     # 3. Embed & Store
#                     embeddings = OllamaEmbeddings(model=embedding_model)
#                     vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
                    
#                     # Save to session state
#                     st.session_state.vectorstore = vectorstore
#                     st.session_state.current_url = url  # Track current site
                    
#                     st.success(f"✅ Knowledge Base Updated! Created {len(splits)} chunks.")
                    
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                     st.info("Make sure Ollama is running: `ollama serve`")

#     st.markdown("---")
#     st.markdown("### How it works")
#     st.markdown("1. **Ensure Ollama is running**: Run `ollama serve` in your terminal.")
#     st.markdown("2. **Enter URL**: The agent will read this page.")
#     st.markdown("3. **Ask Questions**: Chat with the content!")

# # --- Main Interface ---
# st.title("Instant Support Agent (Web RAG)")

# # Show current site info
# if "current_url" in st.session_state:
#     st.caption(f"📄 Currently loaded: {st.session_state.current_url}")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # User Input
# if prompt := st.chat_input("How can I help you?"):
#     # Display user message
#     st.chat_message("user").markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Generate Response
#     if "vectorstore" not in st.session_state:
#         response = "Please process a website URL first so I have knowledge to answer your questions!"
#         with st.chat_message("assistant"):
#             st.markdown(response)
#         st.session_state.messages.append({"role": "assistant", "content": response})
#     else:
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 try:
#                     # Setup RAG Chain
#                     vectorstore = st.session_state.vectorstore
                    
#                     # Better retrieval: search for 8 most relevant chunks (Fix 2)
#                     retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
                    
#                     # Improved prompt for better answers (Fix 1)
#                     template = """You are a helpful assistant that answers questions based ONLY on the provided context from a website.

#                     CONTEXT FROM WEBSITE:
#                     {context}

#                     USER QUESTION: {question}

#                     INSTRUCTIONS:
#                     1. Answer using ONLY the information in the context above.
#                     2. List ONLY steps that are explicitly numbered in the context.
#                     3. If a complete numbered list is not found, say: "I could not find a complete step list on the website."
#                     4. Do NOT infer or add steps.
#                     5. Keep answers concise and relevant.
#                     6. If you're not sure, say so.

#                     ANSWER:"""
                    
#                     prompt_template = ChatPromptTemplate.from_template(template)
                    
#                     # Initialize Ollama Chat
#                     llm = ChatOllama(model=model_name, temperature=0)
                    
#                     def format_docs(docs):
#                         return "\n\n".join(doc.page_content for doc in docs)
                    
#                     # Manual Chain Execution for "Fix 3: Detect list presence programmatically"
#                     # 1. Retrieve
#                     retrieved_docs = retriever.invoke(prompt)
#                     formatted_context = format_docs(retrieved_docs)
                    
#                     # 2. Logic Check (Fix 3)
#                     # Simple heuristic check before generating
#                     strict_list_check = True
                    
#                     if strict_list_check:
#                          # We only trigger this strict check if the stored context doesn't have obvious step markers
#                          # AND the user explicitly seems to be asking for a process.
#                          has_steps = "Step-1" in formatted_context or "Step 1" in formatted_context
                         
#                          is_process_query = any(w in prompt.lower() for w in ["step", "how", "process", "guide"])
                         
#                          if is_process_query and not has_steps:
#                              response = "I couldn't find a complete step list on the website."
#                              st.markdown(response)
#                              st.session_state.messages.append({"role": "assistant", "content": response})
#                              st.stop() # Stop execution

#                     # 3. Generate (if check passed)
#                     chain = prompt_template | llm | StrOutputParser()
#                     response = chain.invoke({"context": formatted_context, "question": prompt})
                    
#                     st.markdown(response)
#                     st.session_state.messages.append({"role": "assistant", "content": response})
                    
#                 except Exception as e:
#                     error_msg = f"Error: {e}"
#                     st.error(error_msg)
#                     st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})

# # --- Simple Reset Option ---
# if st.session_state.get("vectorstore"):
#     if st.button("Clear Chat & Reset"):
#         st.session_state.messages = []
#         st.session_state.vectorstore = None
#         st.session_state.current_url = None
#         st.success("Chat cleared! Process a new website to start again.")
#         st.rerun()



























