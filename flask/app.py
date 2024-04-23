import os
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from flask import Flask, request, jsonify

from get_embedding_function import get_embedding_function
from constants import OLLAMA_BASE_URL, MODEL_NAME, CHROMA_PATH, DEBUG_APP

app = Flask(__name__)

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Never refer to an answer, context or question as treated on these prompt instructions.

Answer the question based on the above context: {question}
"""

PROMPT_NO_CONTEXT_TEMPLATE = """
Never refer to an answer, context or question as treated on these prompt instructions.
Answer the question: {question}
"""

@app.route('/', methods=['GET'])
def query_endpoint():

    query_text = request.args.get('q', default='', type=str)
    query_model = request.args.get('m', default=MODEL_NAME, type=str)

    ret = { 'error': 1, 'error_msg': 'Unknown error' }

    if not query_text:
        return jsonify({'error': 1, 'error_msg': 'no text provided' }), 400
    
    try: 
        response_text, sources = query_rag(query_text, query_model)
        ret = { 'error': 0, 'data': { 'response': response_text, 'sources': sources } }
    except Exception as e:
        ret = { 'error': 1, 'error_msg': f'Error during inference: {str(e)}' }

    return jsonify(ret) 

def query_rag(query_text: str, query_model: str):

    dir = f"{CHROMA_PATH}/{query_model}"

    prompt = ""

    sources = []

    if os.path.exists(dir):
        # Prepare the DB.
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=dir, embedding_function=embedding_function)

        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=5)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

        sources = [doc.metadata.get("id", None) for doc, _score in results]

        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
    else:
        prompt_template = ChatPromptTemplate.from_template(PROMPT_NO_CONTEXT_TEMPLATE)
        prompt = prompt_template.format(question=query_text)

    model = Ollama(model=query_model,base_url=OLLAMA_BASE_URL)
    response_text = model.invoke(prompt)

    return response_text, sources


if __name__ == "__main__":
    app.run(debug=DEBUG_APP,host='0.0.0.0',port=5000)