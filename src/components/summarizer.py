import os
from dotenv import load_dotenv
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from src.logger import logging


def get_summary_from_openai(text):
    try :
        load_dotenv()

        openai.api_key = os.environ.get("OPENAI_API_KEY")
            
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"]
        )

        texts = text_splitter.split_text(text)

        docs = [Document(page_content=t) for t in texts]

        llm =  OpenAI()
        chain = load_summarize_chain(llm, chain_type="map_reduce")

        output_summary = chain.run(docs)

        return output_summary
    except Exception as e:
        logging.debug(f"Failed to get summary from openai : {str(e)}")
        return 
