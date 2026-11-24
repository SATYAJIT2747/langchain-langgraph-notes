# Easy standalone examples + key arguments, shown ABOVE the lecture code.
# EASY[id] = {"keys": [(name, meaning)], "easy": [(title, code)]}

H = r'''from dotenv import load_dotenv; load_dotenv()          # reads GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")
'''

EASY = {

"lc-03": {
 "keys": [("ChatGoogleGenerativeAI(model=)", "which LLM to use"),
          ("temperature", "randomness (0 = same answer every time)"),
          ("max_output_tokens", "max answer length"),
          ("llm.invoke(text)", "ask once, get AIMessage"),
          (".content", "the reply text"),
          ("embed_query(text)", "one text → one vector"),
          ("embed_documents([texts])", "many texts → many vectors")],
 "easy": [("Ask an LLM", r'''from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    temperature=0,            # 0 = factual, 1 = creative
    max_output_tokens=100,    # short answers
)
print(llm.invoke("Capital of Odisha?").content)'''),
  ("Text → vector", r'''from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import GoogleGenerativeAIEmbeddings

emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
v = emb.embed_query("I love cricket")
print(len(v), v[:5])          # vector size + first 5 numbers''')]},

"lc-04": {
 "keys": [("PromptTemplate.from_template(str)", "template with {blanks}"),
          ("template.invoke({...})", "fill the blanks"),
          ("input_variables", "names of the blanks"),
          ("SystemMessage / HumanMessage / AIMessage", "bot role / user / bot reply"),
          ("ChatPromptTemplate([(role, text)])", "multi-message template"),
          ("MessagesPlaceholder(variable_name=)", "slot for chat history")],
 "easy": [("Fill a template", H + r'''from langchain_core.prompts import PromptTemplate

t = PromptTemplate.from_template("Explain {topic} to a {level} in 2 lines")
prompt = t.invoke({"topic": "RAG", "level": "child"})
print(llm.invoke(prompt).content)'''),
  ("Chat template with history slot", H + r'''from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

t = ChatPromptTemplate([
    ("system", "You are a {role}"),
    MessagesPlaceholder("history"),        # past messages go here
    ("human", "{question}"),
])
prompt = t.invoke({"role": "math teacher",
                   "history": [("human", "My name is Satya"), ("ai", "Hi Satya!")],
                   "question": "What is my name?"})
print(llm.invoke(prompt).content)''')]},

"lc-05": {
 "keys": [("BaseModel", "Pydantic class = schema"),
          ("Field(description=)", "hint for the LLM"),
          ("Field(gt=, lt=, ge=, le=)", "number limits (validation)"),
          ("Optional[x] = None", "may be missing"),
          ("Literal['a','b']", "only these values"),
          ("llm.with_structured_output(Schema)", "LLM returns that schema"),
          (".model_dump()", "Pydantic object → dict")],
 "easy": [("Get a Python object back", H + r'''from pydantic import BaseModel, Field
from typing import Literal

class Movie(BaseModel):
    title: str
    rating: float = Field(ge=0, le=10, description="rating out of 10")
    mood: Literal["happy", "sad"]

m = llm.with_structured_output(Movie).invoke("3 Idiots is a fun movie, I give it 9")
print(m.title, m.rating, m.mood)          # 3 Idiots 9.0 happy''')]},

"lc-06": {
 "keys": [("StrOutputParser()", "AIMessage → plain string"),
          ("JsonOutputParser()", "text → dict (no schema)"),
          ("PydanticOutputParser(pydantic_object=)", "text → validated object"),
          ("parser.get_format_instructions()", "tells LLM the output format"),
          ("partial_variables={...}", "pre-filled template blank")],
 "easy": [("String parser (most used)", H + r'''from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

chain = PromptTemplate.from_template("One fact about {x}") | llm | StrOutputParser()
print(chain.invoke({"x": "Mars"}))        # plain string, no .content needed'''),
  ("JSON parser", H + r'''from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

p = JsonOutputParser()
t = PromptTemplate(template="Give name and age of a fictional person.\n{fmt}",
                   input_variables=[],
                   partial_variables={"fmt": p.get_format_instructions()})
print((t | llm | p).invoke({}))           # {'name': ..., 'age': ...}''')]},

"lc-07": {
 "keys": [("a | b | c", "run in sequence"),
          ("RunnableParallel({k: chain})", "run together → dict"),
          ("RunnableBranch((cond, chain), default)", "if / else"),
          ("RunnablePassthrough.assign(k=chain)", "keep input + add a key"),
          ("chain.get_graph().print_ascii()", "draw the chain")],
 "easy": [("Sequential: topic → joke → explain", H + r'''from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
P, S = PromptTemplate.from_template, StrOutputParser()

chain = P("Joke about {topic}") | llm | S | P("Explain this joke: {joke}") | llm | S
print(chain.invoke({"topic": "exams"}))   # string passes into {joke}'''),
  ("Conditional: positive vs negative", H + r'''from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from pydantic import BaseModel
from typing import Literal
P, S = PromptTemplate.from_template, StrOutputParser()

class Mood(BaseModel):
    sentiment: Literal["positive", "negative"]

classify = P("Sentiment of: {text}") | llm.with_structured_output(Mood)

chain = RunnablePassthrough.assign(mood=classify) | RunnableBranch(
    (lambda x: x["mood"].sentiment == "positive", P("Thank the user for: {text}") | llm | S),
    P("Apologise for: {text}") | llm | S,           # default branch
)
print(chain.invoke({"text": "Delivery was late and box was broken"}))''')]},

"lc-08": {
 "keys": [("invoke(x)", "one input"),
          ("batch([x1, x2])", "many inputs in parallel"),
          ("stream(x)", "output piece by piece"),
          ("ainvoke / abatch / astream", "async versions")],
 "easy": [("Same 3 methods on any runnable", H + r'''from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = PromptTemplate.from_template("1-line joke on {t}") | llm | StrOutputParser()

print(chain.invoke({"t": "AI"}))
print(chain.batch([{"t": "cats"}, {"t": "dogs"}]))
for piece in chain.stream({"t": "Python"}):
    print(piece, end="", flush=True)''')]},

"lc-09": {
 "keys": [("RunnableSequence(a, b)", "same as a | b"),
          ("RunnableParallel({...})", "same input to many"),
          ("RunnablePassthrough()", "returns input unchanged"),
          ("RunnableLambda(fn)", "python function as a step"),
          ("RunnableBranch(...)", "if / elif / else")],
 "easy": [("All primitives without an LLM", r'''from langchain_core.runnables import (RunnableLambda, RunnableParallel,
                                      RunnablePassthrough, RunnableBranch)

double = RunnableLambda(lambda x: x * 2)
plus1  = RunnableLambda(lambda x: x + 1)

print((double | plus1).invoke(5))                                  # 11  (sequence)
print(RunnableParallel(d=double, same=RunnablePassthrough()).invoke(5))  # {'d': 10, 'same': 5}

sign = RunnableBranch((lambda x: x > 0, RunnableLambda(lambda x: "positive")),
                      RunnableLambda(lambda x: "not positive"))
print(sign.invoke(-3))                                             # not positive''')]},

"lc-10": {
 "keys": [("Document(page_content, metadata)", "text + info about it"),
          (".load()", "all docs at once (list)"),
          (".lazy_load()", "one by one (generator)"),
          ("DirectoryLoader(path, glob, loader_cls)", "folder, file pattern, which loader"),
          ("encoding='utf-8'", "avoid unicode errors")],
 "easy": [("Load a text file you just created", r'''from langchain_community.document_loaders import TextLoader

open("notes.txt", "w", encoding="utf-8").write("LangChain helps build LLM apps.")

docs = TextLoader("notes.txt", encoding="utf-8").load()
print(len(docs))                 # 1
print(docs[0].page_content)      # the text
print(docs[0].metadata)          # {'source': 'notes.txt'}'''),
  ("Web page", r'''from langchain_community.document_loaders import WebBaseLoader
docs = WebBaseLoader("https://en.wikipedia.org/wiki/LangChain").load()
print(docs[0].page_content[:300])''')]},

"lc-11": {
 "keys": [("chunk_size", "max characters per chunk"),
          ("chunk_overlap", "text shared between neighbours"),
          ("separator", "where to cut (length splitter)"),
          ("split_text(str)", "string → list of strings"),
          ("split_documents(docs)", "Documents → smaller Documents"),
          ("from_language(Language.X)", "code-aware splitting")],
 "easy": [("Recursive splitter on a string", r'''from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """LangChain is a framework.

It has loaders, splitters and retrievers.
RAG uses all of them together."""

splitter = RecursiveCharacterTextSplitter(chunk_size=40, chunk_overlap=5)
for c in splitter.split_text(text):
    print(repr(c))''')]},

"lc-12": {
 "keys": [("Chroma.from_documents(docs, emb)", "create + insert"),
          ("persist_directory", "save to disk folder"),
          ("collection_name", "like a table name"),
          ("similarity_search(q, k=)", "top k similar docs"),
          ("similarity_search_with_score", "docs + distance (lower = closer)"),
          ("filter={...}", "search only matching metadata"),
          ("as_retriever()", "turn into a retriever")],
 "easy": [("Tiny vector store", r'''from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
docs = [Document(page_content="Virat Kohli is a batsman", metadata={"team": "RCB"}),
        Document(page_content="Bumrah is a fast bowler",  metadata={"team": "MI"})]

vs = Chroma.from_documents(docs, emb, collection_name="ipl")
print(vs.similarity_search("who bowls fast?", k=1))
print(vs.similarity_search("player", k=2, filter={"team": "RCB"}))''')]},

"lc-13": {
 "keys": [("retriever.invoke(query)", "get relevant docs"),
          ("search_kwargs={'k': n}", "how many docs"),
          ("search_type='mmr'", "relevant + diverse"),
          ("lambda_mult", "1 = relevance, 0 = diversity"),
          ("MultiQueryRetriever.from_llm", "LLM makes many queries"),
          ("ContextualCompressionRetriever", "keep only relevant sentences")],
 "easy": [("Similarity vs MMR", r'''from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
texts = ["Python is a language", "Python is easy to learn",
         "Python is popular for AI", "Java runs on the JVM"]
vs = FAISS.from_texts(texts, emb)

normal = vs.as_retriever(search_kwargs={"k": 2})
mmr    = vs.as_retriever(search_type="mmr", search_kwargs={"k": 2, "lambda_mult": 0.3})
print(normal.invoke("python"))     # two very similar python docs
print(mmr.invoke("python"))        # more varied results''')]},

"lc-15": {
 "keys": [("FAISS.from_texts / from_documents", "build vector index"),
          ("as_retriever(search_kwargs={'k':})", "top-k fetcher"),
          ("RunnableParallel(context=..., question=...)", "build prompt inputs"),
          ("RunnablePassthrough()", "pass the question as is"),
          ("format_docs", "docs → one string")],
 "easy": [("Smallest possible RAG", H + r'''from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
facts = ["Our office is in Bhubaneswar.", "Office hours are 10am to 6pm.", "We have 40 employees."]
retriever = FAISS.from_texts(facts, emb).as_retriever(search_kwargs={"k": 2})

prompt = PromptTemplate.from_template("Answer only from context.\nContext: {context}\nQ: {question}")
fmt = lambda docs: "\n".join(d.page_content for d in docs)

rag = {"context": retriever | fmt, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
print(rag.invoke("When does the office open?"))''')]},

"lc-16": {
 "keys": [("@tool", "function → tool"),
          ("docstring", "tool description for LLM (required)"),
          ("type hints", "tool input schema"),
          ("tool.name / .description / .args", "what the LLM sees"),
          ("tool.invoke({...})", "run the tool")],
 "easy": [("Make and run a tool", r'''from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

print(add.name, "|", add.description, "|", add.args)
print(add.invoke({"a": 2, "b": 3}))       # 5''')]},

"lc-17": {
 "keys": [("llm.bind_tools([tools])", "tell LLM the tools"),
          ("ai_msg.tool_calls", "[{name, args, id}] LLM wants to call"),
          ("tool.invoke(tool_call)", "run it → ToolMessage"),
          ("ToolMessage", "tool result sent back"),
          ("InjectedToolArg", "arg filled by us, not LLM")],
 "easy": [("The full tool-calling loop", H + r'''from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

@tool
def square(n: int) -> int:
    """Return n squared."""
    return n * n

llm_t = llm.bind_tools([square])
msgs = [HumanMessage("What is 12 squared?")]

ai = llm_t.invoke(msgs); msgs.append(ai)      # 1. LLM asks for the tool
for call in ai.tool_calls:
    msgs.append(square.invoke(call))          # 2. we run it (ToolMessage)
print(llm_t.invoke(msgs).content)             # 3. LLM writes final answer''')]},

"lc-18": {
 "keys": [("create_agent(model, tools, system_prompt)", "ready-made ReAct agent (new API)"),
          ("create_react_agent(llm, tools, prompt)", "agent brain (classic)"),
          ("AgentExecutor(agent, tools, verbose)", "runs the loop (classic)"),
          ("verbose=True", "print thought/action/observation"),
          ("result['messages'][-1]", "final answer")],
 "easy": [("Agent in 10 lines", H + r'''from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather of a city."""
    return f"32°C and sunny in {city}"

agent = create_agent(model=llm, tools=[get_weather], system_prompt="Be brief")
res = agent.invoke({"messages": [{"role": "user", "content": "Weather in Puri?"}]})
print(res["messages"][-1].content)''')]},

"lc-19": {
 "keys": [("ollama pull / run", "download / chat"),
          ("ollama list / ps", "installed / running"),
          ("ChatOllama(model=)", "local model in LangChain"),
          ("localhost:11434", "Ollama's local API")],
 "easy": [("Local model in LangChain", r'''# terminal first:  ollama pull llama3.2
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3.2", temperature=0)
print(llm.invoke("Say hi in Odia").content)''')]},

"lg-04": {
 "keys": [("StateGraph(State)", "create graph with this state"),
          ("add_node(name, fn)", "add a step"),
          ("add_edge(a, b)", "a then b"),
          ("START / END", "entry / exit"),
          ("compile()", "make it runnable"),
          ("Annotated[list, operator.add]", "reducer: append instead of replace")],
 "easy": [("See a reducer in action (no LLM)", r'''import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END

class S(TypedDict):
    nums: Annotated[list[int], operator.add]     # remove Annotated -> error on parallel

g = StateGraph(S)
g.add_node("a", lambda s: {"nums": [1]})
g.add_node("b", lambda s: {"nums": [2]})
g.add_edge(START, "a"); g.add_edge(START, "b")   # a and b run in parallel
g.add_edge("a", END);   g.add_edge("b", END)
print(g.compile().invoke({"nums": []}))           # {'nums': [1, 2]}''')]},

"lg-05": {
 "keys": [("TypedDict state", "shared data of the graph"),
          ("node returns dict", "only the keys it updates"),
          ("invoke(initial_state)", "run with starting values"),
          ("get_graph().draw_mermaid_png()", "picture of the graph")],
 "easy": [("2-step workflow (no LLM)", r'''from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class S(TypedDict):
    name: str
    greeting: str
    shout: str

def greet(s): return {"greeting": f"Hello {s['name']}"}
def loud(s):  return {"shout": s["greeting"].upper() + "!"}

g = StateGraph(S)
g.add_node("greet", greet); g.add_node("loud", loud)
g.add_edge(START, "greet"); g.add_edge("greet", "loud"); g.add_edge("loud", END)
print(g.compile().invoke({"name": "Satya"}))''')]},

"lg-06": {
 "keys": [("add_edge(START, x) many times", "fan-out (parallel)"),
          ("many edges into one node", "fan-in (waits for all)"),
          ("return only changed keys", "avoid InvalidUpdateError"),
          ("operator.add reducer", "collect results from branches")],
 "easy": [("Parallel math (no LLM)", r'''from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class S(TypedDict):
    n: int
    sq: int
    cube: int
    total: int

g = StateGraph(S)
g.add_node("square", lambda s: {"sq": s["n"] ** 2})
g.add_node("cube",   lambda s: {"cube": s["n"] ** 3})
g.add_node("sum",    lambda s: {"total": s["sq"] + s["cube"]})
g.add_edge(START, "square"); g.add_edge(START, "cube")     # parallel
g.add_edge("square", "sum"); g.add_edge("cube", "sum")     # join
g.add_edge("sum", END)
print(g.compile().invoke({"n": 3}))     # sq 9, cube 27, total 36''')]},

"lg-07": {
 "keys": [("add_conditional_edges(src, fn)", "fn decides next node"),
          ("router returns node name", "a string, not state"),
          ("-> Literal['a','b']", "lets graph draw branches"),
          ("path map {'x': 'node'}", "map router output → node")],
 "easy": [("Even / odd router (no LLM)", r'''from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class S(TypedDict):
    n: int
    msg: str

def route(s) -> Literal["even", "odd"]:
    return "even" if s["n"] % 2 == 0 else "odd"

g = StateGraph(S)
g.add_node("even", lambda s: {"msg": "even number"})
g.add_node("odd",  lambda s: {"msg": "odd number"})
g.add_conditional_edges(START, route)
g.add_edge("even", END); g.add_edge("odd", END)
print(g.compile().invoke({"n": 7}))''')]},

"lg-08": {
 "keys": [("edge back to earlier node", "creates a loop"),
          ("iteration / max_iteration", "stop condition"),
          ("{'ok': END, 'retry': 'node'}", "exit or loop"),
          ("recursion_limit", "safety cap (default 25)")],
 "easy": [("Loop until done (no LLM)", r'''from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class S(TypedDict):
    count: int

g = StateGraph(S)
g.add_node("inc", lambda s: {"count": s["count"] + 1})
g.add_edge(START, "inc")
g.add_conditional_edges("inc", lambda s: "stop" if s["count"] >= 5 else "again",
                        {"stop": END, "again": "inc"})        # loop back
print(g.compile().invoke({"count": 0}))      # {'count': 5}'''),
  ("Write → check → rewrite (LLM)", H + r'''from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class S(TypedDict):
    topic: str
    tweet: str
    tries: int

def write(s):  return {"tweet": llm.invoke(f"Short funny tweet on {s['topic']}").content,
                       "tries": s["tries"] + 1}
def check(s):
    ok = llm.invoke(f"Is this tweet funny? answer yes or no only:\n{s['tweet']}").content
    return "done" if "yes" in ok.lower() or s["tries"] >= 3 else "rewrite"

g = StateGraph(S)
g.add_node("write", write)
g.add_edge(START, "write")
g.add_conditional_edges("write", check, {"done": END, "rewrite": "write"})
print(g.compile().invoke({"topic": "Mondays", "tries": 0}))''')]},

"lg-09": {
 "keys": [("MessagesState", "built-in state with messages list"),
          ("add_messages", "append / replace by id"),
          ("return {'messages': [reply]}", "reply is appended")],
 "easy": [("Chatbot using MessagesState", H + r'''from langgraph.graph import StateGraph, START, END, MessagesState

def chat(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

g = StateGraph(MessagesState)
g.add_node("chat", chat)
g.add_edge(START, "chat"); g.add_edge("chat", END)
bot = g.compile()

out = bot.invoke({"messages": [("user", "Hi, I'm Satya")]})
print(out["messages"][-1].content)''')]},

"lg-10": {
 "keys": [("compile(checkpointer=InMemorySaver())", "save state each step"),
          ("{'configurable': {'thread_id': ..}}", "which conversation"),
          ("get_state(config)", "latest snapshot"),
          ("get_state_history(config)", "all snapshots"),
          ("invoke(None, config)", "resume, no new input"),
          ("update_state(config, {...})", "edit past state")],
 "easy": [("Memory across invokes + threads", H + r'''from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver

g = StateGraph(MessagesState)
g.add_node("chat", lambda s: {"messages": [llm.invoke(s["messages"])]})
g.add_edge(START, "chat"); g.add_edge("chat", END)
bot = g.compile(checkpointer=InMemorySaver())

t1 = {"configurable": {"thread_id": "1"}}
t2 = {"configurable": {"thread_id": "2"}}
bot.invoke({"messages": [("user", "My name is Satya")]}, t1)
print(bot.invoke({"messages": [("user", "My name?")]}, t1)["messages"][-1].content)  # Satya
print(bot.invoke({"messages": [("user", "My name?")]}, t2)["messages"][-1].content)  # doesn't know

print(len(list(bot.get_state_history(t1))), "checkpoints in thread 1")''')]},

"lg-11": {
 "keys": [("st.chat_input()", "input box at bottom"),
          ("st.chat_message(role)", "chat bubble"),
          ("st.session_state", "survives reruns"),
          ("streamlit run app.py", "start the app")],
 "easy": [("Whole chatbot UI in one file (app.py)", H + r'''import streamlit as st
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver

@st.cache_resource                      # build graph only once
def get_bot():
    g = StateGraph(MessagesState)
    g.add_node("chat", lambda s: {"messages": [llm.invoke(s["messages"])]})
    g.add_edge(START, "chat"); g.add_edge("chat", END)
    return g.compile(checkpointer=InMemorySaver())

bot, cfg = get_bot(), {"configurable": {"thread_id": "1"}}
st.session_state.setdefault("history", [])

for role, text in st.session_state.history:
    st.chat_message(role).write(text)

if q := st.chat_input("Ask..."):
    st.chat_message("user").write(q)
    a = bot.invoke({"messages": [("user", q)]}, cfg)["messages"][-1].content
    st.chat_message("assistant").write(a)
    st.session_state.history += [("user", q), ("assistant", a)]''')]},

"lg-12": {
 "keys": [("graph.stream(input, config, stream_mode=)", "yield output while running"),
          ("stream_mode='messages'", "LLM tokens (chunk, metadata)"),
          ("stream_mode='updates'", "what each node changed"),
          ("stream_mode='values'", "full state after each step"),
          ("st.write_stream(gen)", "show tokens live in Streamlit")],
 "easy": [("Stream tokens in the terminal", H + r'''from langgraph.graph import StateGraph, START, END, MessagesState

g = StateGraph(MessagesState)
g.add_node("chat", lambda s: {"messages": [llm.invoke(s["messages"])]})
g.add_edge(START, "chat"); g.add_edge("chat", END)
bot = g.compile()

for chunk, meta in bot.stream({"messages": [("user", "Write 5 lines on rain")]},
                              stream_mode="messages"):
    print(chunk.content, end="", flush=True)''')]},

"lg-13": {
 "keys": [("uuid.uuid4()", "new unique thread id"),
          ("new chat", "new thread_id"),
          ("open old chat", "same thread_id + get_state"),
          ("get_state(cfg).values['messages']", "saved conversation")],
 "easy": [("Many conversations = many thread ids (terminal)", H + r'''import uuid
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver

g = StateGraph(MessagesState)
g.add_node("chat", lambda s: {"messages": [llm.invoke(s["messages"])]})
g.add_edge(START, "chat"); g.add_edge("chat", END)
bot = g.compile(checkpointer=InMemorySaver())

chat_a, chat_b = str(uuid.uuid4()), str(uuid.uuid4())
cfg = lambda tid: {"configurable": {"thread_id": tid}}

bot.invoke({"messages": [("user", "Let's talk about cricket")]}, cfg(chat_a))
bot.invoke({"messages": [("user", "Let's talk about cooking")]}, cfg(chat_b))

# "resume" chat A: load its messages
for m in bot.get_state(cfg(chat_a)).values["messages"]:
    print(type(m).__name__, ":", m.content[:60])''')]},

"lg-14": {
 "keys": [("sqlite3.connect(file, check_same_thread=False)", "DB file, allow multi-thread"),
          ("SqliteSaver(conn)", "checkpoints saved in SQLite"),
          ("checkpointer.list(None)", "all checkpoints of all threads")],
 "easy": [("Memory that survives restart (run twice)", H + r'''import sqlite3
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.sqlite import SqliteSaver

saver = SqliteSaver(sqlite3.connect("memory.db", check_same_thread=False))

g = StateGraph(MessagesState)
g.add_node("chat", lambda s: {"messages": [llm.invoke(s["messages"])]})
g.add_edge(START, "chat"); g.add_edge("chat", END)
bot = g.compile(checkpointer=saver)

cfg = {"configurable": {"thread_id": "me"}}
msg = input("You: ")                   # 1st run: "I am Satya", 2nd run: "Who am I?"
print(bot.invoke({"messages": [("user", msg)]}, cfg)["messages"][-1].content)''')]},

"lg-15": {
 "keys": [("LANGCHAIN_TRACING_V2=true", "turn tracing on"),
          ("LANGCHAIN_API_KEY", "LangSmith key"),
          ("LANGCHAIN_PROJECT", "project name in dashboard"),
          ("@traceable", "trace a normal function"),
          ("config tags / metadata / run_name", "labels to filter traces")],
 "easy": [("Trace a plain function", r'''import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "demo"
# os.environ["LANGCHAIN_API_KEY"] = "lsv2_..."   (keep in .env)

from langsmith import traceable

@traceable(name="clean_text")
def clean(text: str) -> str:
    return text.strip().lower()

clean("  Hello LangSmith  ")      # appears as a run in the 'demo' project''')]},

"lg-16": {
 "keys": [("config['metadata']", "extra info on the trace"),
          ("thread_id in metadata", "groups turns into a Thread")],
 "easy": [("Label a graph run", r'''config = {
    "configurable": {"thread_id": "t1"},     # memory
    "metadata": {"thread_id": "t1", "user": "satya"},   # LangSmith grouping
    "tags": ["chatbot", "v1"],
    "run_name": "chat_turn",
}
# bot.invoke({"messages": [("user", "hi")]}, config)''')]},

"lg-17": {
 "keys": [("llm.bind_tools(tools)", "LLM knows the tools"),
          ("ToolNode(tools)", "node that runs tool calls"),
          ("tools_condition", "tool call? → 'tools' else END"),
          ("add_edge('tools', 'chat')", "loop back with result"),
          ("create_react_agent(llm, tools)", "all of this prebuilt")],
 "easy": [("Tool agent graph", H + r'''from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [multiply]
llm_t = llm.bind_tools(tools)

g = StateGraph(MessagesState)
g.add_node("chat", lambda s: {"messages": [llm_t.invoke(s["messages"])]})
g.add_node("tools", ToolNode(tools))
g.add_edge(START, "chat")
g.add_conditional_edges("chat", tools_condition)
g.add_edge("tools", "chat")
app = g.compile()
print(app.invoke({"messages": [("user", "What is 23*47?")]})["messages"][-1].content)'''),
  ("Same thing, prebuilt", H + r'''from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

app = create_react_agent(llm, [multiply])        # chat + ToolNode + loop, done
print(app.invoke({"messages": [("user", "23*47?")]})["messages"][-1].content)''')]},

"lg-18": {
 "keys": [("FastMCP(name)", "create MCP server"),
          ("@mcp.tool()", "expose a function"),
          ("MultiServerMCPClient({...})", "connect to servers"),
          ("transport 'stdio'", "local subprocess server"),
          ("transport 'streamable_http' + url", "remote server"),
          ("await client.get_tools()", "MCP tools → LangChain tools"),
          ("async / await / asyncio.run", "MCP is async-only")],
 "easy": [("server.py", r'''from fastmcp import FastMCP
mcp = FastMCP("math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

if __name__ == "__main__":
    mcp.run()'''),
  ("client.py", H + r'''import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def main():
    client = MultiServerMCPClient(
        {"math": {"transport": "stdio", "command": "python", "args": ["server.py"]}})
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    out = await agent.ainvoke({"messages": [("user", "What is 41 + 1?")]})
    print(out["messages"][-1].content)

asyncio.run(main())''')]},

"lg-19": {
 "keys": [("@tool rag_tool(query)", "retrieval as a tool"),
          ("docstring", "when LLM should use it"),
          ("retriever.invoke(query)", "fetch chunks"),
          ("agent decides", "retrieve only if needed")],
 "easy": [("Agentic RAG in ~15 lines", H + r'''from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
retriever = FAISS.from_texts(["Leave policy: 24 paid leaves per year.",
                              "WFH allowed on Fridays."], emb).as_retriever()

@tool
def company_policy(query: str) -> str:
    """Search company HR policies."""
    return "\n".join(d.page_content for d in retriever.invoke(query))

agent = create_react_agent(llm, [company_policy])
print(agent.invoke({"messages": [("user", "How many paid leaves do I get?")]})["messages"][-1].content)''')]},

"lg-20": {
 "keys": [("interrupt(payload)", "pause + send payload to user"),
          ("result['__interrupt__']", "see why it paused"),
          ("Command(resume=value)", "continue with human answer"),
          ("checkpointer + same thread_id", "required to resume")],
 "easy": [("Pause for approval (no LLM)", r'''from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

class S(TypedDict):
    amount: int
    status: str

def pay(s):
    ok = interrupt(f"Approve payment of ₹{s['amount']}? (yes/no)")
    return {"status": "paid" if ok == "yes" else "cancelled"}

g = StateGraph(S)
g.add_node("pay", pay); g.add_edge(START, "pay"); g.add_edge("pay", END)
app = g.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "1"}}

r = app.invoke({"amount": 500}, cfg)
print(r["__interrupt__"][0].value)               # question for human
print(app.invoke(Command(resume="yes"), cfg))    # {'amount': 500, 'status': 'paid'}''')]},

"lg-21": {
 "keys": [("compiled graph as node", "shared state keys"),
          ("subgraph.invoke inside a node", "different state keys"),
          ("map in / map out", "parent keys ↔ subgraph keys")],
 "easy": [("Subgraph (no LLM)", r'''from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# child graph: its own state
class Child(TypedDict):
    text: str
    out: str
c = StateGraph(Child)
c.add_node("upper", lambda s: {"out": s["text"].upper()})
c.add_edge(START, "upper"); c.add_edge("upper", END)
child = c.compile()

# parent graph
class Parent(TypedDict):
    question: str
    answer: str

def call_child(s):                                  # different keys -> map them
    return {"answer": child.invoke({"text": s["question"]})["out"]}

p = StateGraph(Parent)
p.add_node("child", call_child)
p.add_edge(START, "child"); p.add_edge("child", END)
print(p.compile().invoke({"question": "hello"}))   # answer: HELLO''')]},

"lg-23": {
 "keys": [("trim_messages(strategy='last', max_tokens=)", "send only recent msgs"),
          ("count_tokens_approximately", "cheap token counter"),
          ("RemoveMessage(id=m.id)", "delete msg from state"),
          ("summary key + system msg", "compressed old history"),
          ("PostgresSaver.from_conn_string(uri)", "production checkpointer"),
          ("checkpointer.setup()", "create tables (first time)")],
 "easy": [("Trim before calling the LLM", H + r'''from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages.utils import trim_messages, count_tokens_approximately

def chat(s: MessagesState):
    recent = trim_messages(s["messages"], strategy="last", max_tokens=100,
                           token_counter=count_tokens_approximately)
    return {"messages": [llm.invoke(recent)]}

g = StateGraph(MessagesState)
g.add_node("chat", chat); g.add_edge(START, "chat"); g.add_edge("chat", END)
bot = g.compile(checkpointer=InMemorySaver())'''),
  ("Delete old messages (no LLM)", r'''from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import RemoveMessage, AIMessage

def reply(s):   return {"messages": [AIMessage("ok")]}
def cleanup(s): return {"messages": [RemoveMessage(id=m.id) for m in s["messages"][:-2]]}

g = StateGraph(MessagesState)
g.add_node("reply", reply); g.add_node("cleanup", cleanup)
g.add_edge(START, "reply"); g.add_edge("reply", "cleanup"); g.add_edge("cleanup", END)
out = g.compile().invoke({"messages": [("user", "a"), ("user", "b"), ("user", "c")]})
print([m.content for m in out["messages"]])      # only last 2 kept''')]},

"lg-24": {
 "keys": [("InMemoryStore() / PostgresStore", "long-term memory DB"),
          ("namespace tuple", "folder, e.g. ('user', 'u1')"),
          ("store.put(ns, key, dict)", "save"),
          ("store.get(ns, key)", "read one"),
          ("store.search(ns, query=, limit=)", "find (semantic if indexed)"),
          ("compile(store=store)", "give store to nodes"),
          ("node(state, config, *, store)", "access store in node")],
 "easy": [("Store basics (no LLM)", r'''from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
ns = ("user", "satya")
store.put(ns, "food", {"data": "likes biryani"})
store.put(ns, "lang", {"data": "codes in Python"})

print(store.get(ns, "food").value)              # {'data': 'likes biryani'}
for item in store.search(ns):
    print(item.key, item.value)'''),
  ("Use memory inside a graph", H + r'''from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore
from langchain_core.runnables import RunnableConfig

store = InMemoryStore()
store.put(("user", "u1"), "1", {"data": "User's name is Satya, preparing for interviews"})

def chat(s: MessagesState, config: RunnableConfig, *, store: BaseStore):
    uid = config["configurable"]["user_id"]
    facts = "\n".join(i.value["data"] for i in store.search(("user", uid)))
    return {"messages": [llm.invoke([("system", f"Known about user:\n{facts}")] + s["messages"])]}

g = StateGraph(MessagesState)
g.add_node("chat", chat); g.add_edge(START, "chat"); g.add_edge("chat", END)
app = g.compile(store=store)
print(app.invoke({"messages": [("user", "Who am I?")]},
                 {"configurable": {"user_id": "u1"}})["messages"][-1].content)''')]},

"lg-25": {
 "keys": [("Send(node, payload)", "start one worker with its own input"),
          ("return [Send(...) for ...]", "dynamic number of workers"),
          ("add_conditional_edges(src, fn, ['worker'])", "where Sends can go"),
          ("operator.add on results", "collect worker outputs")],
 "easy": [("Send API (no LLM)", r'''import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

class S(TypedDict):
    words: list[str]
    results: Annotated[list[str], operator.add]

def fan_out(s):
    return [Send("worker", {"w": w}) for w in s["words"]]     # one worker per word

g = StateGraph(S)
g.add_node("worker", lambda p: {"results": [p["w"].upper()]})
g.add_conditional_edges(START, fan_out, ["worker"])
g.add_edge("worker", END)
print(g.compile().invoke({"words": ["rag", "agent", "graph"], "results": []}))''')]},

"lg-26": {
 "keys": [("grade docs", "is each doc relevant?"),
          ("CORRECT", "use docs (refined)"),
          ("INCORRECT", "web search instead"),
          ("AMBIGUOUS", "docs + web search"),
          ("rewrite query", "better search query")],
 "easy": [("Mini CRAG", H + r'''from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.tools import DuckDuckGoSearchRun

emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
retriever = FAISS.from_texts(["Bias is error from wrong assumptions.",
                              "Variance is error from sensitivity to data."], emb).as_retriever(search_kwargs={"k": 2})

class S(TypedDict):
    q: str
    context: str
    answer: str

def retrieve_and_grade(s):
    good = [d.page_content for d in retriever.invoke(s["q"])
            if "yes" in llm.invoke(f"Is this relevant to '{s['q']}'? yes/no\n{d.page_content}").content.lower()]
    return {"context": "\n".join(good)}

def web(s):      return {"context": DuckDuckGoSearchRun().invoke(s["q"])}
def generate(s): return {"answer": llm.invoke(f"Context:\n{s['context']}\nQ: {s['q']}").content}

g = StateGraph(S)
g.add_node("retrieve", retrieve_and_grade); g.add_node("web", web); g.add_node("generate", generate)
g.add_edge(START, "retrieve")
g.add_conditional_edges("retrieve", lambda s: "generate" if s["context"] else "web")  # no good docs -> web
g.add_edge("web", "generate"); g.add_edge("generate", END)
print(g.compile().invoke({"q": "What is variance in ML?"})["answer"])''')]},

"lg-27": {
 "keys": [("need retrieval?", "skip RAG for simple questions"),
          ("relevant?", "filter docs"),
          ("supported?", "answer grounded in docs"),
          ("useful?", "answer solves the question"),
          ("loop caps", "max revisions / rewrites")],
 "easy": [("Mini Self-RAG", H + r'''from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
retriever = FAISS.from_texts(["Our refund window is 7 days.", "Shipping is free above ₹499."], emb).as_retriever()
yes = lambda prompt: "yes" in llm.invoke(prompt + "\nAnswer yes or no only.").content.lower()

class S(TypedDict):
    q: str
    context: str
    answer: str
    tries: int

def decide(s):   return "retrieve" if yes(f"Does '{s['q']}' need company documents?") else "generate"
def retrieve(s): return {"context": "\n".join(d.page_content for d in retriever.invoke(s["q"]))}
def generate(s): return {"answer": llm.invoke(f"Context:\n{s.get('context','')}\nQ: {s['q']}").content,
                         "tries": s["tries"] + 1}
def supported(s):
    if not s.get("context") or s["tries"] >= 2: return "end"
    return "end" if yes(f"Is this answer fully supported by context?\n{s['context']}\n{s['answer']}") else "retry"

g = StateGraph(S)
g.add_node("retrieve", retrieve); g.add_node("generate", generate)
g.add_conditional_edges(START, decide)
g.add_edge("retrieve", "generate")
g.add_conditional_edges("generate", supported, {"end": END, "retry": "generate"})
print(g.compile().invoke({"q": "How many days for refund?", "tries": 0})["answer"])''')]},

"lg-28": {
 "keys": [("test case", "question + expected answer/tools"),
          ("answer check", "contains expected?"),
          ("tool check", "right tools used?"),
          ("trajectory", "right order of tools"),
          ("latency", "time.perf_counter() difference"),
          ("LLM-as-judge", "LLM grades open answers")],
 "easy": [("Tiny agent test", H + r'''import time
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

agent = create_agent(model=llm, tools=[add])

tests = [{"q": "What is 20 + 22?", "expect": "42", "tools": ["add"]}]
for t in tests:
    start = time.perf_counter()
    out = agent.invoke({"messages": [("user", t["q"])]})
    secs = time.perf_counter() - start
    used = [c["name"] for m in out["messages"] for c in getattr(m, "tool_calls", [])]
    answer = out["messages"][-1].content
    print({"answer_ok": t["expect"] in str(answer), "tools_ok": used == t["tools"],
           "fast": secs < 10})''')]},

"lg-29": {
 "keys": [("before_agent / after_agent", "check input / output"),
          ("PIIMiddleware(type, strategy=)", "find personal data"),
          ("strategy redact / mask / hash / block", "remove / hide / hash / stop"),
          ("apply_to_input / apply_to_output", "where to check"),
          ("HumanInTheLoopMiddleware(interrupt_on=)", "approval before tools"),
          ("jump_to: 'end'", "stop the agent early")],
 "easy": [("Simplest guardrail: wrap the call", H + r'''import re

BLOCK = re.compile(r"\b(hack|password|malware)\b", re.I)

def safe_ask(q: str) -> str:
    if BLOCK.search(q):                                  # input guardrail
        return "Sorry, I can't help with that."
    answer = llm.invoke(q).content
    answer = re.sub(r"\S+@\S+", "[EMAIL]", answer)       # output guardrail (redact)
    return answer

print(safe_ask("How to hack wifi?"))
print(safe_ask("Write a sample support email with an email address"))'''),
  ("Built-in PII middleware", H + r'''from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(model=llm, tools=[], middleware=[
    PIIMiddleware("email", strategy="redact", apply_to_input=True),
    PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
])
out = agent.invoke({"messages": [("user", "My mail is a@b.com, card 5105-1051-0510-5100")]})
print(out["messages"][0].content)     # PII hidden before reaching the LLM''')]},

"ex-02": {
 "keys": [("BM25Retriever", "keyword search"),
          ("EnsembleRetriever(retrievers, weights)", "combine (hybrid)"),
          ("CrossEncoder.predict(pairs)", "re-rank score"),
          ("HyDE", "search with a fake answer")],
 "easy": [("Hybrid = keyword + vector", r'''from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

texts = ["Error E42 means payment timeout", "Payments fail when the bank is slow",
         "Refunds take 7 days"]
emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

hybrid = EnsembleRetriever(
    retrievers=[BM25Retriever.from_texts(texts), FAISS.from_texts(texts, emb).as_retriever()],
    weights=[0.5, 0.5])
print(hybrid.invoke("E42"))''')]},

"ex-04": {
 "keys": [("Command(goto=, update=)", "jump to node + update state"),
          ("supervisor", "decides who works next"),
          ("worker agents", "specialists")],
 "easy": [("Supervisor with Command (simple)", H + r'''from typing import Literal
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Command

def supervisor(s) -> Command[Literal["math", "poet", "__end__"]]:
    if len(s["messages"]) > 1:                     # someone already answered
        return Command(goto=END)
    q = s["messages"][-1].content
    return Command(goto="math" if any(ch.isdigit() for ch in q) else "poet")

def math(s): return Command(goto="supervisor",
                            update={"messages": [llm.invoke("Solve: " + s["messages"][0].content)]})
def poet(s): return Command(goto="supervisor",
                            update={"messages": [llm.invoke("Write 2 poetic lines on: " + s["messages"][0].content)]})

g = StateGraph(MessagesState)
g.add_node("supervisor", supervisor); g.add_node("math", math); g.add_node("poet", poet)
g.add_edge(START, "supervisor")
print(g.compile().invoke({"messages": [("user", "12*12")]})["messages"][-1].content)''')]},

"ex-06": {
 "keys": [(".with_retry(stop_after_attempt=)", "retry on errors"),
          (".with_fallbacks([backup])", "use backup model"),
          ("set_llm_cache(InMemoryCache())", "reuse same answers"),
          ("InMemoryRateLimiter(requests_per_second=)", "slow down calls"),
          ("config={'recursion_limit': n}", "cap graph steps")],
 "easy": [("Retry + fallback", r'''from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

main   = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")
backup = ChatGoogleGenerativeAI(model="gemini-flash-latest")

llm = main.with_retry(stop_after_attempt=3).with_fallbacks([backup])
print(llm.invoke("hi").content)''')]},
}
