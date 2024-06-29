 # Depndencies
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere.chat_models import ChatCohere
from langchain_openai import OpenAIEmbeddings
import os
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Pinecone
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from pinecone import Pinecone as PineconeClient
from dotenv import load_dotenv
load_dotenv()

# API keys
openai_key = os.getenv("OPENAI_API_KEY")
cohere_key = os.getenv("COHERE_API_KEY")

# Langsmith 
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Initialize models
openai_model = ChatOpenAI(openai_api_key=openai_key, model="gpt-3.5-turbo")
cohere_model = ChatCohere(model="command-r-plus", cohere_api_key=cohere_key)



# Keys
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_ENVIRONMENT = os.environ["PINECONE_ENVIRONMENT"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]

pinecone = PineconeClient(api_key=PINECONE_API_KEY,
                         environment=PINECONE_ENVIRONMENT)

embeddings = OpenAIEmbeddings(api_key=openai_key)

vectorstore = Pinecone.from_existing_index(index_name=PINECONE_INDEX_NAME,
                                           embedding=embeddings)

retriever = vectorstore.as_retriever()


# Define the prompt template
template = """
أنت مساعد ذكي اسمه منير، مختص وخبير في قطاع السيارات في السعودية. تعمل في تطبيق مصباح، وهو تطبيق يقدم حلولاً شاملة للسيارات. مهمتك هي مساعدة الناس والإجابة على استفساراتهم حول السيارات، الإصلاحات، الصيانة، والخدمات المتوفرة في مصباح. إذا كنت لا تعرف الإجابة، قل بكل بساطة أنك لا تعرف ولا تحاول تأليف إجابة.

1. توليد الإجابات: قدم إجابات مختصرة، لا تتجاوز خمسة أسطر.
2. تكامل التسويق: وجه المستخدمين إلى الخدمات ذات الصلة التي يقدمها مصباح بطريقة مختصرة.
3. الرد باللغة العربية فقط.
4. الصدق والدقة: إذا كنت غير متأكد من الإجابة، اعترف بذلك.

السياق: {context}
السؤال: {question}
"""

my_prompt = ChatPromptTemplate.from_template(template)


# define chain 
chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | my_prompt
    | openai_model
    | StrOutputParser()
)