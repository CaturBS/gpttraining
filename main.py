from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage

import os
import gradio as gr


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




@app.route('/send_conversation', methods=['POST'])
def make_query(text:str):
    docpath = os.path.join(os.getcwd(), "docs")
    vec_index = __init_index(docpath)
    query_engine = vec_index.as_query_engine()
    response = query_engine.query(text)
    print(response)
    return str(response)


if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] = "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"
    iface = gr.Interface(fn=make_query,
                         inputs=gr.components.Textbox(lines=7, placeholder="Enter your question here"),
                         outputs="text",
                         title="Chat-chatan test",
                         description="Chat tentang 'fifth discipline'",
                         )
    iface.launch(share=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
