# from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferWindowMemory
import os
import gradio as gr
import random



class ConversationFactory:
    __conversation = None

    @staticmethod
    def get_conversation():
        if ConversationFactory.__conversation is None:
            embeddings = OpenAIEmbeddings()
            vectordb = Chroma(persist_directory=os.path.join(os.getcwd(), "chroma_db"), embedding_function=embeddings)
            ConversationFactory.__conversation = ConversationalRetrievalChain.from_llm(

                ChatOpenAI(temperature=0.6,model_name="gpt-3.5-turbo-16k",max_tokens=800),
                vectordb.as_retriever(),
                max_tokens_limit=6400,
                return_source_documents=False,
                verbose=True,
            )
        return ConversationFactory.__conversation



def make_query(message, history):
    memory = ConversationBufferWindowMemory(
        k=4
    )
    memory.chat_memory.clear()
    for hist in history:
        memory.chat_memory.add_user_message(hist[0])
        memory.chat_memory.add_ai_message(hist[0])
    conversation = ConversationFactory.get_conversation()
    result = conversation({"question": message, "chat_history": memory.chat_memory.messages})
    return result['answer']

if __name__ == '__main__':
    # os.environ["OPENAI_API_KEY"] = "_open_ai_key"
    # iface = gr.Interface(fn=make_query,
    #                      inputs=[gr.components.Textbox(lines=7, placeholder="Enter your question here")],
    #                      outputs=["text", gr.components.Highlight()],
    #                      title="Chat-chatan test",
    #                      description="Chat tentang 'fifth discipline'",
    #                      )
    # iface.launch(share=False,server_name="0.0.0.0", server_port=5000)
<<<<<<< HEAD
    chat_iface = gr.ChatInterface(
=======
    chatface = gr.ChatInterface(
>>>>>>> c02839c9513c1283a64b965e6281d8c219f5eb8a
        title="Chat-chatan test",
        description="Chat tentang 'fifth discipline'",
        fn=make_query
    )
<<<<<<< HEAD
    chat_iface.launch(share=False, server_name="0.0.0.0", server_port=5000)
=======
    chatface.launch(share=False,server_name="0.0.0.0", server_port=5000)
>>>>>>> c02839c9513c1283a64b965e6281d8c219f5eb8a

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
