from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from flask import Flask, session, request, render_template
from flask_session import Session
import os

app = Flask(__name__)


def __init_index(directory_path):
    PERSIST_DIR = "./storage"
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader(directory_path).load_data()
        result = VectorStoreIndex.from_documents(documents)
        # store it for later
        result.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        result = load_index_from_storage(storage_context)
    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_conversation', methods=['POST'])
def make_query():
    if 'vec_index' in session:
        vec_index = session['vec_index']
    else:
        docpath = os.path.join(os.getcwd(), "docs")
        vec_index = __init_index(docpath)
        session['vec_index'] = vec_index
    text = request.form['text_qry']
    query_engine = vec_index.as_query_engine()
    response = query_engine.query(text)

    return str(response)


if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] = "{value of openapikey}"
    app.secret_key = 'ssisdhid'
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    app.run("0.0.0.0", 5000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
