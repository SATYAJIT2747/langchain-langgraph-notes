# LangChain playlist (CampusX) — concepts + simple code
# Each video: id, yt, dur, title, concepts [(term, html)], code [(title, code)], remember [str]

SETUP = '''# one-time setup used in almost every snippet below
# pip install langchain langchain-core langchain-community langchain-google-genai python-dotenv
from dotenv import load_dotenv
load_dotenv()                       # reads GOOGLE_API_KEY from .env

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0.7)'''

LANGCHAIN = [
dict(id="lc-00a", yt="pSVk-5WemQ0", dur="50:15", title="GenAI Roadmap for Beginners",
 concepts=[
  ("Generative AI", "AI that <b>creates new content</b> (text, images, code, audio) that looks like human-made data, instead of only classifying or predicting a label."),
  ("Where it is used", "Customer support bots, content writing, education/tutors, software dev (Copilot-style), and images/video."),
  ("Two perspectives", "<b>Builder side</b> = making foundation models (transformers, pre-training, fine-tuning, optimization, evaluation). <b>User side</b> = using those models to build apps (prompting, RAG, agents, LLMOps). This course is mostly the <b>user side</b>."),
  ("User-side roadmap", "LLM basics → prompt engineering → <b>LangChain</b> → RAG → fine-tuning → agents (<b>LangGraph</b>) → LLMOps → multimodal."),
 ],
 code=[], remember=["You don't train LLMs here; you build applications on top of them."]),

dict(id="lc-00b", yt="_3ezSpJw2E8", dur="15:19", title="Generative AI using LangChain (Playlist Intro)",
 concepts=[
  ("What is LangChain", "An <b>open-source framework</b> to build LLM-powered applications. It gives ready building blocks (models, prompts, chains, retrievers, tools…) so you don't write glue code yourself."),
  ("Why LangChain first", "Most real GenAI apps (chatbots, RAG, agents) need several pieces wired together. LangChain is the standard way to wire them, and LangGraph is built on top of it."),
  ("Focus of the playlist", "Understanding fundamentals + latest LangChain syntax (LCEL / runnables) instead of old deprecated chains."),
 ],
 code=[], remember=["LangChain = toolkit for building LLM apps. LangGraph = LangChain's big brother for agents/workflows."]),

dict(id="lc-01", yt="nlz9j-r0U9U", dur="37:44", title="Introduction to LangChain",
 concepts=[
  ("Why we need LangChain", "Example app: <i>chat with a PDF</i>. You must: load the PDF → split into chunks → create embeddings → store in a DB → find relevant chunks for the question → send chunks + question to the LLM. Doing all of this from scratch (and switching providers) is painful. LangChain gives each step as a component."),
  ("Semantic search", "Search by <b>meaning</b>, not exact words. Text is converted into vectors (embeddings); the closest vectors are the most similar texts."),
  ("Benefits", "<b>Concept of chains</b> (pipe components together), <b>model-agnostic</b> (swap OpenAI ↔ Gemini ↔ Claude with one line), complete ecosystem (loaders, splitters, vector stores), memory & state handling."),
  ("What you can build", "Conversational chatbots, AI knowledge assistants, AI agents, workflow automation, summarization / research helpers."),
  ("Alternatives", "LlamaIndex (strong for RAG/indexing), Haystack."),
 ],
 code=[], remember=["The PDF-chat pipeline: Load → Split → Embed → Store → Retrieve → LLM. This is RAG and comes back later."]),

dict(id="lc-02", yt="-xSJA8-o6Eg", dur="53:24", title="LangChain Components",
 concepts=[
  ("6 components", "<b>Models, Prompts, Chains, Indexes, Memory, Agents.</b>"),
  ("Models", "A common interface to talk to any LLM. Two kinds: <b>Language models</b> (text in → text out) and <b>Embedding models</b> (text in → vector out)."),
  ("Prompts", "The input you send to an LLM. Output depends heavily on it, so LangChain gives templates (dynamic, role-based, few-shot)."),
  ("Chains", "Connect components into a pipeline; output of one step becomes input of the next. Can be sequential, parallel or conditional."),
  ("Indexes", "Connect your LLM to <b>external knowledge</b> (PDFs, websites, DBs). Made of: document loader, text splitter, vector store, retriever."),
  ("Memory", "LLM API calls are <b>stateless</b> (they forget the last message). Memory keeps history: ConversationBufferMemory, BufferWindowMemory (last N), SummarizerMemory, custom."),
  ("Agents", "A chatbot that can <b>reason and take actions</b> using tools (e.g. a calculator or a weather API). Agent = LLM + reasoning + tools."),
 ],
 code=[], remember=["Mnemonic: <b>M-P-C-I-M-A</b> → Models, Prompts, Chains, Indexes, Memory, Agents."]),

dict(id="lc-03", yt="HdcLE8JuMrA", dur="1:42:03", title="LangChain Models",
 concepts=[
  ("Language models", "<b>LLMs</b> (old style: string in → string out) vs <b>Chat Models</b> (list of messages in → message out, have roles, support history). Use <b>chat models</b> nowadays."),
  ("temperature", "Controls randomness. <code>0</code>–0.3 → factual/deterministic (code, math). 0.7–1.5 → creative (stories, jokes)."),
  ("max_completion_tokens", "Limits how long the answer can be (cost control)."),
  ("Closed vs open source", "Closed (OpenAI, Claude, Gemini) = API, pay per token. Open source (Llama, Mistral, Qwen via HuggingFace) = free, private, customisable, but needs hardware and setup."),
  ("Using HF models", "Either through the <b>HuggingFace Inference API</b> (<code>HuggingFaceEndpoint</code>) or <b>locally</b> (<code>HuggingFacePipeline</code>), then wrap with <code>ChatHuggingFace</code>."),
  ("Embedding models", "Turn text into a vector of numbers. <code>embed_query(text)</code> → one vector, <code>embed_documents([texts])</code> → many vectors."),
  ("Document similarity demo", "Embed the documents and the query, then use <b>cosine similarity</b>; the highest score = the most relevant document. This is the core idea behind RAG."),
 ],
 code=[
  ("Chat model (any provider, same interface)", SETUP + '''

result = llm.invoke("What is the capital of India?")
print(result.content)

# swapping provider = one line change
# from langchain_openai import ChatOpenAI;            llm = ChatOpenAI(model="gpt-4o-mini")
# from langchain_anthropic import ChatAnthropic;      llm = ChatAnthropic(model="claude-...")'''),
  ("Open-source model via HuggingFace", '''from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

endpoint = HuggingFaceEndpoint(repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                               task="text-generation")      # needs HUGGINGFACEHUB_API_TOKEN
model = ChatHuggingFace(llm=endpoint)
print(model.invoke("What is the capital of India?").content)'''),
  ("Embeddings + document similarity", '''from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

docs = ["Virat Kohli is an Indian batsman.",
        "Jasprit Bumrah is a fast bowler.",
        "MS Dhoni is a former Indian captain."]
query = "Tell me about Bumrah"

doc_vecs  = emb.embed_documents(docs)     # list of vectors
query_vec = emb.embed_query(query)        # one vector

scores = cosine_similarity([query_vec], doc_vecs)[0]
best = scores.argmax()
print(docs[best], scores[best])'''),
 ],
 remember=["<code>llm.invoke()</code> returns an <b>AIMessage</b>; the text is in <code>.content</code>.",
           "Embeddings + cosine similarity = semantic search."]),

dict(id="lc-04", yt="3TGqlQxpuU0", dur="1:18:33", title="Prompts in LangChain",
 concepts=[
  ("Static vs dynamic prompts", "Static = the user types the whole prompt (risky, inconsistent). Dynamic = a fixed <b>template</b> with blanks that you fill (<code>{paper}</code>, <code>{style}</code>)."),
  ("PromptTemplate", "Template for <b>single-turn</b> text prompts. Why not plain f-strings? It gives <b>validation</b> (<code>validate_template=True</code>), <b>reusability</b> (save/load as JSON) and works in <b>chains</b> (it is a Runnable)."),
  ("Messages", "<code>SystemMessage</code> (sets the role/behaviour), <code>HumanMessage</code> (user), <code>AIMessage</code> (model reply). A chat history is just a list of these."),
  ("Simple chatbot with memory", "Keep a <code>chat_history</code> list; append the human message, invoke with the whole list, append the AI reply. That's how the bot 'remembers'."),
  ("ChatPromptTemplate", "Template for <b>multi-turn / role-based</b> prompts: a list of (role, text) with placeholders."),
  ("MessagesPlaceholder", "A slot inside a ChatPromptTemplate where you insert a <b>whole list of past messages</b> (chat history) at runtime."),
 ],
 code=[
  ("PromptTemplate", '''from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="Explain {topic} in {style} style, in {length}.",
    input_variables=["topic", "style", "length"],
)
prompt = template.invoke({"topic": "Attention", "style": "beginner", "length": "5 lines"})
print(llm.invoke(prompt).content)

template.save("template.json")   # reuse later with load_prompt("template.json")'''),
  ("Chatbot with message history", '''from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

chat_history = [SystemMessage(content="You are a helpful assistant")]

while True:
    user = input("You: ")
    if user == "exit": break
    chat_history.append(HumanMessage(content=user))
    reply = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=reply.content))
    print("AI:", reply.content)'''),
  ("ChatPromptTemplate + MessagesPlaceholder", '''from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_template = ChatPromptTemplate([
    ("system", "You are a helpful {domain} expert"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{query}"),
])

prompt = chat_template.invoke({
    "domain": "customer support",
    "chat_history": [HumanMessage("I want a refund for order #12"),
                     AIMessage("Your refund is initiated.")],
    "query": "Where is my refund?",
})'''),
 ],
 remember=["Use tuples <code>(\"system\", \"...{x}\")</code> in ChatPromptTemplate; passing <code>SystemMessage(content=\"{x}\")</code> objects will NOT fill the placeholder.",
           "PromptTemplate → single message; ChatPromptTemplate → list of role messages."]),

dict(id="lc-05", yt="y5EmRr1O1h4", dur="1:08:13", title="Structured Output",
 concepts=[
  ("What & why", "Making the LLM reply in a <b>fixed format (JSON / object)</b> instead of free text, so other code, databases or APIs can use it. Uses: data extraction (resume → JSON), API building, agents/tools (they need exact inputs)."),
  ("with_structured_output()", "For models that support it natively. Pass a schema: <code>llm.with_structured_output(Schema)</code>."),
  ("TypedDict", "Python type hints for a dict. Simple, but <b>no runtime validation</b>. Use <code>Annotated[str, \"description\"]</code> to guide the LLM, <code>Optional</code> for may-be-missing, <code>Literal</code> for fixed choices."),
  ("Pydantic", "Data validation library. <b>Validates and coerces types</b> at runtime, supports defaults, <code>Optional</code>, <code>EmailStr</code>, and <code>Field(description=..., ge=, le=)</code> constraints. Returns a Pydantic object."),
  ("JSON schema", "Plain JSON describing the structure. Use when working across languages (no Python classes). Returns a dict."),
  ("When to use what", "TypedDict → quick, Python-only, trust the data. <b>Pydantic → validation needed (most common)</b>. JSON schema → cross-language."),
  ("method", "<code>method=\"function_calling\"</code> (default for most providers) or <code>\"json_mode\"</code>. Models without structured-output support → use <b>output parsers</b> (next video)."),
 ],
 code=[
  ("Pydantic basics (validation)", '''from pydantic import BaseModel, Field
from typing import Optional

class Student(BaseModel):
    name: str = "Satya"                       # default value
    age: Optional[int] = None
    cgpa: float = Field(gt=0, lt=10, description="CGPA out of 10")

s = Student(age="22", cgpa=8.5)   # "22" is coerced to int 22
print(s.model_dump())             # -> dict
Student(cgpa=12)                  # ValidationError!'''),
  ("Structured output with Pydantic (most used)", '''from pydantic import BaseModel, Field
from typing import Literal, Optional

class Review(BaseModel):
    summary: str = Field(description="One line summary of the review")
    sentiment: Literal["pos", "neg"]
    pros: Optional[list[str]] = None

structured_llm = llm.with_structured_output(Review)
r = structured_llm.invoke("The phone is fast and the battery is great, but it heats up.")
print(r.sentiment, r.pros)        # attribute access'''),
  ("Same thing with TypedDict", '''from typing import TypedDict, Annotated

class Review(TypedDict):
    summary: Annotated[str, "One line summary"]
    sentiment: Annotated[str, "pos or neg"]

r = llm.with_structured_output(Review).invoke("Great camera, poor battery")
print(r["sentiment"])             # dict access'''),
 ],
 remember=["TypedDict → dict, no validation. Pydantic → object, validates. JSON schema → dict, any language."]),

dict(id="lc-06", yt="Op6PbJZ5b2Q", dur="53:13", title="Output Parsers",
 concepts=[
  ("Output parsers", "Classes that convert the raw LLM text into a usable format. They work with <b>any</b> model (even ones without structured-output support) and plug into chains."),
  ("StrOutputParser", "Returns just the <b>text</b> (<code>.content</code>). The most used parser; makes chaining LLM calls easy."),
  ("JsonOutputParser", "Forces JSON output via <code>parser.get_format_instructions()</code> in the prompt. Drawback: you <b>cannot enforce a schema</b>."),
  ("StructuredOutputParser", "JSON with a schema defined via <code>ResponseSchema</code> list. Drawback: <b>no data validation</b>. (Now in <code>langchain_classic</code>.)"),
  ("PydanticOutputParser", "Schema + <b>validation</b> using a Pydantic model. The strongest parser."),
  ("partial_variables", "Fill a template variable at creation time, e.g. <code>{format_instruction}</code> → the parser's format instructions."),
 ],
 code=[
  ("StrOutputParser in a chain", '''from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

t1 = PromptTemplate.from_template("Write a detailed report on {topic}")
t2 = PromptTemplate.from_template("Write a 5 line summary of:\\n{text}")

chain = t1 | llm | StrOutputParser() | t2 | llm | StrOutputParser()
print(chain.invoke({"topic": "black hole"}))'''),
  ("PydanticOutputParser (schema + validation)", '''from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(gt=18, description="Age of the person")
    city: str

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template="Generate a fictional {place} person.\\n{format_instruction}",
    input_variables=["place"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)

chain = template | llm | parser
print(chain.invoke({"place": "Indian"}))      # -> Person(name=..., age=..., city=...)'''),
  ("JsonOutputParser (no schema)", '''from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
template = PromptTemplate(
    template="Give 5 facts about {topic}\\n{format_instruction}",
    input_variables=["topic"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)
print((template | llm | parser).invoke({"topic": "black hole"}))   # -> dict'''),
 ],
 remember=["Str → text, Json → dict (no schema), Structured → dict with schema (no validation), Pydantic → validated object."]),

dict(id="lc-07", yt="5hjrPILA3-8", dur="54:01", title="Chains",
 concepts=[
  ("Why chains", "An LLM app has many steps (prompt → LLM → parse → ...). Chains connect them so the <b>output of one step automatically becomes the input of the next</b>. You only call <code>invoke</code> once."),
  ("Pipe operator <code>|</code>", "This is <b>LCEL</b> syntax: <code>prompt | llm | parser</code>."),
  ("Simple chain", "prompt → model → parser."),
  ("Sequential chain", "Two LLM calls in a row: e.g. generate a report → summarise it."),
  ("Parallel chain", "Run independent chains at the same time with <code>RunnableParallel</code> (e.g. make notes and a quiz from the same text), then merge them."),
  ("Conditional chain", "Choose a branch based on a condition with <code>RunnableBranch</code> (e.g. positive feedback → thank-you reply, negative → apology). Use a Pydantic parser so the classifier output is reliable."),
  ("Visualise", "<code>chain.get_graph().print_ascii()</code> prints the chain diagram."),
 ],
 code=[
  ("Parallel chain", '''from langchain_core.runnables import RunnableParallel

notes_prompt = PromptTemplate.from_template("Make short notes from:\\n{text}")
quiz_prompt  = PromptTemplate.from_template("Make 5 Q&A from:\\n{text}")
merge_prompt = PromptTemplate.from_template("Merge into one doc:\\nNotes: {notes}\\nQuiz: {quiz}")
parser = StrOutputParser()

parallel = RunnableParallel({
    "notes": notes_prompt | llm | parser,
    "quiz":  quiz_prompt  | llm | parser,
})
chain = parallel | merge_prompt | llm | parser
print(chain.invoke({"text": "...some long text about SVM..."}))
chain.get_graph().print_ascii()'''),
  ("Conditional chain (sentiment → reply)", '''from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Literal

class Feedback(BaseModel):
    sentiment: Literal["positive", "negative"]

p = PydanticOutputParser(pydantic_object=Feedback)
classify = PromptTemplate(
    template="Classify the sentiment:\\n{feedback}\\n{fmt}",
    input_variables=["feedback"],
    partial_variables={"fmt": p.get_format_instructions()},
) | llm | p

pos = PromptTemplate.from_template("Write a thank-you reply to: {feedback}")
neg = PromptTemplate.from_template("Write an apology reply to: {feedback}")

branch = RunnableBranch(
    (lambda x: x.sentiment == "positive", pos | llm | parser),
    (lambda x: x.sentiment == "negative", neg | llm | parser),
    RunnableLambda(lambda x: "could not find sentiment"),   # default
)
# NOTE: branch receives the Feedback object, so feedback text must be passed along
# (simplest: rebuild the dict) -> see RunnablePassthrough in Runnables part 2'''),
 ],
 remember=["Sequential = <code>|</code>, Parallel = <code>RunnableParallel</code>, Conditional = <code>RunnableBranch</code>."]),

dict(id="lc-08", yt="u3b-W1NgYa4", dur="1:16:22", title="Runnables — Part 1 (Why they exist)",
 concepts=[
  ("The problem", "Early LangChain components each had <b>different methods</b>: LLM → <code>predict()</code>, PromptTemplate → <code>format()</code>, retriever → <code>get_relevant_documents()</code>. So the team kept writing special chain classes (LLMChain, RetrievalQA, SequentialChain...). Too many chains, hard to learn, hard to maintain."),
  ("The fix: Runnable", "A <b>common interface</b>. Every component is a <b>unit of work</b> with the same methods: <code>invoke()</code> (one input), <code>batch()</code> (many inputs), <code>stream()</code> (token by token)."),
  ("Composable", "Because they share an interface, any runnable can be connected to another; a chain of runnables is itself a runnable. Like LEGO blocks."),
  ("Code demo idea", "He builds a fake 'NakliLLM' and 'NakliPromptTemplate' that both inherit an abstract <code>Runnable</code> class with <code>invoke</code>, then a <code>RunnableConnector</code> that runs a list of runnables one after another. That's exactly what <code>|</code> does internally."),
 ],
 code=[
  ("Mini Runnable from scratch (the idea behind |)", '''from abc import ABC, abstractmethod

class Runnable(ABC):
    @abstractmethod
    def invoke(self, x): ...

class FakePrompt(Runnable):
    def __init__(self, template): self.template = template
    def invoke(self, x): return self.template.format(**x)

class FakeLLM(Runnable):
    def invoke(self, prompt): return {"response": f"Answer to: {prompt}"}

class Connector(Runnable):                # == chain
    def __init__(self, steps): self.steps = steps
    def invoke(self, x):
        for step in self.steps:
            x = step.invoke(x)
        return x

chain = Connector([FakePrompt("Tell me about {topic}"), FakeLLM()])
print(chain.invoke({"topic": "cricket"}))'''),
  ("invoke / batch / stream", '''chain = PromptTemplate.from_template("Joke about {t}") | llm | StrOutputParser()

chain.invoke({"t": "AI"})                       # one
chain.batch([{"t": "AI"}, {"t": "cats"}])       # many in parallel
for chunk in chain.stream({"t": "AI"}):         # token-by-token
    print(chunk, end="")'''),
 ],
 remember=["Runnable = standard interface (invoke/batch/stream) → anything can connect to anything."]),

dict(id="lc-09", yt="47nc0n-e4_w", dur="54:26", title="Runnables — Part 2 (Types + LCEL)",
 concepts=[
  ("Two categories", "<b>Task-specific runnables</b> = core components converted to runnables (ChatModel, PromptTemplate, Retriever...). <b>Runnable primitives</b> = building blocks to define <b>how</b> they connect (sequence, parallel, branch...)."),
  ("RunnableSequence", "Runs runnables <b>one after another</b>. <code>RunnableSequence(a, b, c)</code> == <code>a | b | c</code>."),
  ("RunnableParallel", "Runs several runnables on the <b>same input</b> at once; returns a dict <code>{key: output}</code>."),
  ("RunnablePassthrough", "Returns the input <b>unchanged</b>. Used to carry a value forward (e.g. keep the joke while also explaining it)."),
  ("RunnableLambda", "Wrap <b>any Python function</b> as a runnable (e.g. word count, cleaning text, formatting docs)."),
  ("RunnableBranch", "if/elif/else for chains: list of <code>(condition, runnable)</code> + a default."),
  ("LCEL", "<b>LangChain Expression Language</b> — the declarative <code>|</code> syntax for sequences. Most common pattern in modern LangChain."),
 ],
 code=[
  ("Sequence + Passthrough + Lambda (from your runnable_lambda.py)", '''from langchain_core.runnables import (RunnableSequence, RunnableParallel,
                                      RunnablePassthrough, RunnableLambda)

joke_chain = PromptTemplate.from_template("Write a joke about {topic}") | llm | StrOutputParser()

parallel = RunnableParallel({
    "joke": RunnablePassthrough(),                          # keep joke as-is
    "word_count": RunnableLambda(lambda t: len(t.split())), # any python fn
})

final = joke_chain | parallel
print(final.invoke({"topic": "AI"}))   # {'joke': '...', 'word_count': 23}'''),
  ("Branch: summarise only if long (from runnable_branch.py)", '''from langchain_core.runnables import RunnableBranch

report = PromptTemplate.from_template("Write a detailed report on {topic}") | llm | StrOutputParser()
summarise = PromptTemplate.from_template("Summarize:\\n{text}") | llm | StrOutputParser()

branch = RunnableBranch(
    (lambda x: len(x.split()) > 300, summarise),   # condition, runnable
    RunnablePassthrough(),                          # default
)
print((report | branch).invoke({"topic": "Russia vs Ukraine"}))'''),
 ],
 remember=["Sequence |  ·  Parallel {dict}  ·  Passthrough = same input  ·  Lambda = python fn  ·  Branch = if/else."]),

dict(id="lc-10", yt="bL92ALSZ2Cg", dur="56:44", title="Document Loaders",
 concepts=[
  ("RAG (quick)", "Retrieval-Augmented Generation: give the LLM extra knowledge from <b>your</b> documents at question time. Components: loaders → splitters → vector store → retriever."),
  ("Document object", "Every loader returns a list of <code>Document(page_content=..., metadata={...})</code>."),
  ("TextLoader", "Loads a .txt file into one Document."),
  ("PyPDFLoader", "<b>One Document per page</b>; metadata has source + page. Works only for text PDFs. Scanned/complex PDFs → PDFPlumber, UnstructuredPDFLoader, PyMuPDF, AmazonTextract."),
  ("DirectoryLoader", "Load all files in a folder via a <code>glob</code> + <code>loader_cls</code>."),
  ("load vs lazy_load", "<code>load()</code> = eager, returns a list (all in memory). <code>lazy_load()</code> = <b>generator</b>, one document at a time — use for many/large files."),
  ("WebBaseLoader", "Loads text from a web page (requests + BeautifulSoup). Good for static pages; JS-heavy pages → SeleniumURLLoader."),
  ("CSVLoader", "<b>One Document per row</b>."),
  ("Custom loader", "Inherit <code>BaseLoader</code> and implement <code>load</code>/<code>lazy_load</code> if your source isn't supported."),
 ],
 code=[
  ("All loaders in one place", '''from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, DirectoryLoader, WebBaseLoader, CSVLoader)

docs = TextLoader("cricket.txt", encoding="utf-8").load()
docs = PyPDFLoader("dl-curriculum.pdf").load()          # 1 doc per page
docs = CSVLoader(file_path="data.csv").load()           # 1 doc per row
docs = WebBaseLoader("https://example.com").load()

loader = DirectoryLoader(path="books", glob="*.pdf", loader_cls=PyPDFLoader)
for doc in loader.lazy_load():            # generator, memory friendly
    print(doc.metadata)

print(docs[0].page_content, docs[0].metadata)'''),
  ("Loader + chain", '''docs = TextLoader("cricket.txt").load()
prompt = PromptTemplate.from_template("Summarize this poem:\\n{poem}")
chain = prompt | llm | StrOutputParser()
print(chain.invoke({"poem": docs[0].page_content}))'''),
 ],
 remember=["Loader output is always <code>list[Document]</code> → page_content + metadata."]),

dict(id="lc-11", yt="SEWS9P4ODmc", dur="59:01", title="Text Splitters",
 concepts=[
  ("Why split", "LLMs and embedding models have <b>context limits</b>; smaller chunks give <b>better embeddings</b>, <b>better semantic search</b>, and cheaper processing."),
  ("chunk_size / chunk_overlap", "Size of each chunk and how much neighbouring chunks share (overlap keeps context across boundaries; ~10–20% is common)."),
  ("1. Length based", "<code>CharacterTextSplitter</code> — cut every N characters. Fast, but cuts words/sentences in the middle."),
  ("2. Text-structure based ⭐", "<code>RecursiveCharacterTextSplitter</code> — tries separators in order: <code>\"\\n\\n\"</code> (paragraph) → <code>\"\\n\"</code> (line) → <code>\" \"</code> (word) → <code>\"\"</code> (char). Keeps paragraphs/sentences together. <b>Most used.</b>"),
  ("3. Document-structure based", "For code/markdown/HTML: <code>RecursiveCharacterTextSplitter.from_language(Language.PYTHON, ...)</code> splits on <code>class</code>, <code>def</code>, etc. <code>MarkdownHeaderTextSplitter</code> splits on headers."),
  ("4. Semantic meaning based", "<code>SemanticChunker</code> embeds sentences and splits where the <b>meaning changes</b> (similarity drops beyond a threshold, e.g. standard deviation). Experimental."),
 ],
 code=[
  ("The splitters", '''from langchain_text_splitters import (CharacterTextSplitter,
    RecursiveCharacterTextSplitter, Language)

# 1. length based
s1 = CharacterTextSplitter(chunk_size=200, chunk_overlap=0, separator="")
chunks = s1.split_documents(docs)          # docs from a loader

# 2. recursive (default choice)
s2 = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = s2.split_text(long_text)          # for plain strings

# 3. code / markdown aware
s3 = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=300, chunk_overlap=0)

# 4. semantic
from langchain_experimental.text_splitter import SemanticChunker
s4 = SemanticChunker(emb, breakpoint_threshold_type="standard_deviation",
                     breakpoint_threshold_amount=1)'''),
 ],
 remember=["<code>split_text(str)</code> for strings, <code>split_documents(list[Document])</code> for loader output.",
           "Default pick: RecursiveCharacterTextSplitter."]),

dict(id="lc-12", yt="k13WK0bxQP0", dur="50:31", title="Vector Stores",
 concepts=[
  ("Why", "Example: movie recommender. Keyword matching fails; you need <b>meaning</b> → embeddings. Then you need to store millions of vectors and search them fast → vector store."),
  ("Vector store", "System to <b>store and retrieve embeddings</b>. Features: storage (memory/disk), <b>similarity search</b>, <b>indexing</b> (ANN like HNSW for speed), CRUD."),
  ("Vector store vs Vector DB", "Vector store = lightweight library (FAISS). Vector <b>database</b> = full DB features too: distributed, backups, auth, ACID (Pinecone, Milvus, Weaviate, Qdrant). Every vector DB is a vector store, not vice-versa."),
  ("In LangChain", "All stores share one interface: <code>from_documents</code>, <code>add_documents</code>, <code>similarity_search</code>, <code>as_retriever</code> — so switching Chroma ↔ FAISS ↔ Pinecone is easy."),
  ("Chroma", "Lightweight, open source, good for local dev. Hierarchy: tenant → database → <b>collection</b> → documents (embedding + text + metadata)."),
 ],
 code=[
  ("Chroma CRUD + search (from your chroma_dem.ipynb)", '''from langchain_chroma import Chroma
from langchain_core.documents import Document

docs = [Document(page_content="Hubble captured galaxy images", metadata={"topic": "Astronomy"}),
        Document(page_content="Mars is the Red Planet",        metadata={"topic": "Mars"})]

vs = Chroma(embedding_function=emb, persist_directory="my_chroma_db",
            collection_name="sample")
ids = vs.add_documents(docs)

vs.get(include=["documents", "metadatas", "embeddings"])        # view
vs.similarity_search("Tell me about Hubble", k=2)
vs.similarity_search_with_score("Tell me about Hubble", k=2)     # lower = closer
vs.similarity_search("planet", filter={"topic": "Mars"})         # metadata filter
vs.update_document(document_id=ids[0], document=Document(page_content="..."))
vs.delete(ids=[ids[1]])'''),
  ("One-liner: create + insert", '''vs = Chroma.from_documents(documents=docs, embedding=emb, collection_name="sample")
# Chroma() = empty store, Chroma.from_documents() = store + insert now
# FAISS works the same: from langchain_community.vectorstores import FAISS'''),
 ],
 remember=["Chroma score is a distance → <b>smaller is more similar</b>."]),

dict(id="lc-13", yt="pJdMxwXBsk0", dur="51:10", title="Retrievers",
 concepts=[
  ("Retriever", "Takes a <b>query</b> and returns relevant <b>Documents</b> from a data source. Retrievers are <b>runnables</b> → <code>retriever.invoke(query)</code> and they plug into chains."),
  ("Types", "By <b>data source</b> (Wikipedia, vector store, archive) and by <b>search strategy</b> (MMR, multi-query, contextual compression...)."),
  ("WikipediaRetriever", "Searches Wikipedia API and returns article text. (It's a retriever, not a tool, because it only fetches docs.)"),
  ("Vector store retriever", "<code>vs.as_retriever(search_kwargs={\"k\": 3})</code> — plain similarity search."),
  ("MMR", "<b>Maximal Marginal Relevance</b>: picks results that are relevant <b>and different from each other</b>, avoiding 3 copies of the same idea. <code>lambda_mult</code>: 1 = pure relevance, 0 = max diversity."),
  ("MultiQueryRetriever", "LLM rewrites an <b>ambiguous query into several queries</b>, retrieves for each, merges unique results. Good for vague questions."),
  ("ContextualCompressionRetriever", "Retrieves docs then uses an LLM to <b>keep only the relevant sentences</b> from each doc. Good when docs are long and mixed-topic."),
  ("More", "ParentDocumentRetriever, SelfQueryRetriever, EnsembleRetriever (hybrid BM25 + vectors), TimeWeighted..."),
 ],
 code=[
  ("All retrievers (from your all_Retrievers.ipynb)", '''from langchain_community.retrievers import WikipediaRetriever
wiki = WikipediaRetriever(top_k_results=2, lang="en")
docs = wiki.invoke("Generative AI")

# plain similarity
retriever = vs.as_retriever(search_kwargs={"k": 2})

# MMR (diverse results)
retriever = vs.as_retriever(search_type="mmr",
                            search_kwargs={"k": 3, "lambda_mult": 0.5})

# Multi-query
from langchain_classic.retrievers import MultiQueryRetriever
mq = MultiQueryRetriever.from_llm(retriever=vs.as_retriever(), llm=llm)
docs = mq.invoke("how to improve my health?")

# Contextual compression
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
cc = ContextualCompressionRetriever(
        base_compressor=LLMChainExtractor.from_llm(llm),
        base_retriever=vs.as_retriever(search_kwargs={"k": 2}))
docs = cc.invoke("Explain photosynthesis")'''),
 ],
 remember=["Vague query → MultiQuery. Duplicate-ish results → MMR. Long noisy docs → Contextual Compression."]),

dict(id="lc-14", yt="X0btK9X0Xnk", dur="59:24", title="RAG — What & How it works",
 concepts=[
  ("Problems with plain LLMs", "1) No knowledge of <b>private</b> data, 2) <b>knowledge cutoff</b> (no recent info), 3) <b>hallucination</b>."),
  ("Fine-tuning?", "Training the model further on your data. Works but is <b>expensive</b>, needs ML expertise, and must be redone when data changes."),
  ("In-context learning", "LLMs can learn from examples/info <b>placed in the prompt</b> (emergent ability). RAG uses this: put relevant context in the prompt."),
  ("RAG", "<b>Retrieval + Augmented Generation</b>: fetch relevant chunks from an external knowledge base and give them to the LLM along with the question."),
  ("4 steps", "<b>1. Indexing</b> (load → split → embed → store) · <b>2. Retrieval</b> (find top-k chunks for the query) · <b>3. Augmentation</b> (prompt = context + question) · <b>4. Generation</b> (LLM answers using the context)."),
  ("Why RAG wins", "Cheap, uses up-to-date data, private data stays in your DB, less hallucination (answer only from context), no retraining."),
 ],
 code=[],
 remember=["Indexing happens once (offline); Retrieval → Augmentation → Generation happens per question."]),

dict(id="lc-15", yt="J5_-l7WIO_w", dur="46:15", title="Project: YouTube Chatbot (RAG)",
 concepts=[
  ("Problem", "Ask questions about a long YouTube video instead of watching it."),
  ("Plan", "Get transcript (youtube-transcript-api) → split → embed → FAISS → retriever → prompt → LLM."),
  ("Chain trick", "Use <code>RunnableParallel</code> to build <code>{context, question}</code>: <code>context = retriever | format_docs</code>, <code>question = RunnablePassthrough()</code>."),
  ("Improvements", "UI (Streamlit/Chrome plugin), evaluation (<b>RAGAS</b>, LangSmith), better indexing (translation, chunking), better retrieval (<b>query rewriting, multi-query, MMR, hybrid search, re-ranking</b>, compression), augmentation (prompt templating, grounding), generation (citations, guardrails), and later <b>agentic RAG</b>, memory, multimodal."),
 ],
 code=[
  ("Full RAG chain in ~20 lines", '''from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

# 1. Indexing
fetched = YouTubeTranscriptApi().fetch("Gfr50f6ZBvo", languages=["en"])
transcript = " ".join(s.text for s in fetched)
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).create_documents([transcript])
vs = FAISS.from_documents(chunks, emb)

# 2. Retrieval
retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# 3. Augmentation
prompt = PromptTemplate.from_template(
    "Answer ONLY from the transcript context. If not there, say you don't know.\\n"
    "{context}\\nQuestion: {question}")
format_docs = lambda docs: "\\n\\n".join(d.page_content for d in docs)

# 4. Generation
chain = (RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()})
         | prompt | llm | StrOutputParser())

print(chain.invoke("Can you summarize the video?"))'''),
 ],
 remember=["<code>create_documents([text])</code> splits raw strings into Document chunks."]),

dict(id="lc-16", yt="etnLX7m2MiA", dur="45:16", title="Tools",
 concepts=[
  ("Tool", "A Python function packaged so an LLM can <b>understand and call it</b>: it has a <b>name</b>, a <b>description</b>, and an <b>input schema</b>. LLMs can think (brain) but can't act; tools are the hands."),
  ("Built-in tools", "<code>DuckDuckGoSearchRun</code>, <code>WikipediaQueryRun</code>, <code>ShellTool</code>, <code>PythonREPLTool</code>, RequestsGetTool, Gmail, Slack, SQL..."),
  ("Custom tool — 3 ways", "1) <code>@tool</code> decorator (simplest; type hints + docstring are required), 2) <code>StructuredTool.from_function</code> with a Pydantic <code>args_schema</code> (strict input), 3) subclass <code>BaseTool</code> (full control, async)."),
  ("Inspect a tool", "<code>tool.name</code>, <code>tool.description</code>, <code>tool.args</code>, <code>tool.args_schema.model_json_schema()</code> — this schema is what the LLM sees."),
  ("Toolkit", "A <b>group of related tools</b> (e.g. a GitHub or Gmail toolkit). Just a class with <code>get_tools()</code>."),
 ],
 code=[
  ("Built-in + @tool + toolkit (from your tools.ipynb)", '''from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

search = DuckDuckGoSearchRun()
print(search.invoke("IPL 2026 news"))

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""          # docstring = description for the LLM
    return a * b

print(multiply.invoke({"a": 5, "b": 3}))
print(multiply.name, multiply.description, multiply.args)

class MathToolkit:
    def get_tools(self): return [multiply]'''),
  ("StructuredTool with Pydantic schema", '''from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class MultiplyInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

multiply_tool = StructuredTool.from_function(
    func=lambda a, b: a * b, name="multiply",
    description="Multiply two numbers", args_schema=MultiplyInput)'''),
 ],
 remember=["Tools are runnables too: <code>tool.invoke({...})</code>.",
           "Docstring missing → @tool raises an error. Write good descriptions; the LLM picks tools by them."]),

dict(id="lc-17", yt="EzYaFF7ahKw", dur="58:47", title="Tool Calling",
 concepts=[
  ("Tool binding", "Telling the LLM which tools exist: <code>llm_with_tools = llm.bind_tools([tool1, tool2])</code>. Only some models support this."),
  ("Tool calling", "The LLM <b>doesn't run the tool</b>. It returns an AIMessage with <code>.tool_calls</code> = <code>[{name, args, id}]</code> saying which tool to call with what arguments."),
  ("Tool execution", "<b>You (LangChain)</b> run it: <code>tool.invoke(tool_call)</code> returns a <code>ToolMessage</code>. Add it to the message list and call the LLM again to get the final answer."),
  ("Currency conversion example", "Tool 1 gets the conversion rate, tool 2 multiplies. The LLM should NOT guess the rate, so the rate arg is marked <code>Annotated[float, InjectedToolArg]</code> — the LLM leaves it out and <b>we inject it</b> from tool 1's result."),
  ("Is this an agent?", "<b>No</b> — we wrote the control flow (call tool 1, then tool 2) ourselves. An agent decides the steps <b>autonomously</b>."),
 ],
 code=[
  ("Bind → call → execute → answer", '''from langchain_core.messages import HumanMessage

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

llm_with_tools = llm.bind_tools([multiply])

messages = [HumanMessage("What is 8 times 7?")]
ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg)
print(ai_msg.tool_calls)      # [{'name': 'multiply', 'args': {'a': 8, 'b': 7}, 'id': '...'}]

for call in ai_msg.tool_calls:
    tool_msg = multiply.invoke(call)       # passing the whole call -> ToolMessage
    messages.append(tool_msg)

print(llm_with_tools.invoke(messages).content)   # "8 times 7 is 56"'''),
  ("InjectedToolArg (LLM must not fill this arg)", '''from langchain_core.tools import InjectedToolArg
from typing import Annotated

@tool
def convert(base_value: float, rate: Annotated[float, InjectedToolArg]) -> float:
    """Convert base currency value using the given conversion rate"""
    return base_value * rate

# later: when the LLM calls `convert`, we set the arg ourselves
# call["args"]["rate"] = rate_from_first_tool
# convert.invoke(call)'''),
 ],
 remember=["Flow: bind_tools → AIMessage.tool_calls → tool.invoke(call) → ToolMessage → LLM again."]),

dict(id="lc-18", yt="gm_lQG8fYjI", dur="1:12:47", title="Build an AI Agent",
 concepts=[
  ("AI agent", "An intelligent system that receives a <b>high-level goal</b>, then <b>plans, decides and executes steps by itself</b> using tools, adapting to results."),
  ("Characteristics", "Goal-driven, supports reasoning/planning, uses tools, context-aware, adaptive."),
  ("ReAct", "<b>Reasoning + Acting</b> pattern: loop of <b>Thought → Action → Observation</b> until it has the final answer. (Paper: Yao et al. 2022.)"),
  ("Agent vs AgentExecutor", "<b>Agent</b> = the LLM brain that decides the next action (Thought/Action). <b>AgentExecutor</b> = the runtime loop that actually runs the tool, feeds back the observation, and repeats."),
  ("Prompt", "Classic ReAct prompt pulled from the hub: <code>hub.pull(\"hwchase17/react\")</code>."),
  ("2026 note", "In LangChain 1.x, the classic <code>AgentExecutor</code> lives in <code>langchain_classic</code>; the new API is <code>create_agent</code> (built on LangGraph). Same idea."),
 ],
 code=[
  ("ReAct agent as taught (classic API)", '''from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic import hub
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    return f"It is 31°C and sunny in {city}"

prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm=llm, tools=[search, get_weather], prompt=prompt)
executor = AgentExecutor(agent=agent, tools=[search, get_weather], verbose=True)

print(executor.invoke({"input": "Capital of Odisha and its weather?"})["output"])'''),
  ("Same agent, LangChain 1.x style", '''from langchain.agents import create_agent

agent = create_agent(model=llm, tools=[search, get_weather],
                     system_prompt="You are a helpful assistant")
res = agent.invoke({"messages": [{"role": "user", "content": "Weather in Bhubaneswar?"}]})
print(res["messages"][-1].content)'''),
 ],
 remember=["ReAct = Thought → Action → Observation (repeat) → Final Answer.",
           "verbose=True shows the agent's thinking loop."]),

dict(id="lc-19", yt="YcAYmIFtA0o", dur="2:49:41", title="Ollama Masterclass (Local LLMs)",
 concepts=[
  ("Why local LLMs", "Proprietary APIs cost money, send data outside, need internet. Open-source LLMs (Llama, Qwen, Gemma, Mistral, DeepSeek) are now good enough."),
  ("Why open source is hard", "Downloading weights, matching hardware, quantisation formats, serving them — painful to do yourself."),
  ("Ollama", "A tool that <b>downloads, runs and serves open-source LLMs locally</b> with one command. Handles quantisation (GGUF), GPU/CPU, and exposes a REST API at <code>localhost:11434</code>."),
  ("Hardware", "Rule of thumb: model size (in params) × quantisation decides RAM/VRAM. 7–8B models in 4-bit ≈ 5–6 GB."),
  ("CLI", "<code>pull</code>, <code>run</code>, <code>list</code>, <code>ps</code>, <code>show</code>, <code>rm</code>, <code>stop</code>. Inside chat: <code>/set parameter temperature 0.2</code>, <code>/show info</code>."),
  ("Modelfile", "Create your own variant: base model + system prompt + parameters → <code>ollama create mybot -f Modelfile</code>."),
  ("Use from code", "Python <code>ollama</code> library, REST API, OpenAI-compatible endpoint, and LangChain's <code>ChatOllama</code>. Vision models accept images."),
 ],
 code=[
  ("CLI basics", '''ollama pull llama3.2          # download
ollama run llama3.2           # chat in terminal
ollama list                   # installed models
ollama ps                     # running models
ollama show llama3.2          # params, template, license
ollama rm llama3.2'''),
  ("Modelfile (custom model)", '''FROM llama3.2
PARAMETER temperature 0.3
SYSTEM "You are a strict DSA interviewer. Ask one question at a time."

# terminal: ollama create interviewer -f Modelfile && ollama run interviewer'''),
  ("Python + LangChain", '''import ollama
r = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": "Hi"}])
print(r["message"]["content"])

from langchain_ollama import ChatOllama       # pip install langchain-ollama
llm = ChatOllama(model="llama3.2", temperature=0)
print(llm.invoke("Explain RAG in 2 lines").content)   # drop-in for any chain'''),
 ],
 remember=["ChatOllama is a drop-in replacement for any chat model in the chains above."]),
]
