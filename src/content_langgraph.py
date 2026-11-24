# LangGraph playlist (CampusX) — concepts + simple code

LG_SETUP = '''from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")'''

CHAT_STATE = '''from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]'''

LANGGRAPH = [
dict(id="lg-00", yt="yC36gN-rqjo", dur="16:58", title="Agentic AI using LangGraph (Playlist Intro)",
 concepts=[
  ("Why this playlist", "The industry moved from simple LLM apps → <b>agentic systems</b>. LangGraph is the leading framework to build them in a controlled, production-ready way."),
  ("Curriculum", "Foundations of agentic AI → LangGraph fundamentals (state, nodes, edges, workflows) → advanced (persistence, memory, HITL, streaming, tools, MCP, subgraphs, observability) → projects / advanced RAG."),
  ("Prerequisites", "Python, LangChain basics (models, prompts, tools, structured output). That's why the LangChain playlist came first."),
 ],
 code=[], remember=["LangGraph is built ON LangChain; you still use LangChain models/tools inside LangGraph nodes."]),

dict(id="lg-01", yt="xdA0pGDiUPE", dur="1:02:44", title="Generative AI vs Agentic AI",
 concepts=[
  ("GenAI", "AI that creates new content by learning data patterns. Traditional AI <b>predicts/classifies</b>; GenAI <b>generates</b>."),
  ("Running example: an HR hiring assistant", "Shows the evolution in 4 chatbots:"),
  ("Chatbot 1 — plain LLM", "Answers general questions (\"how to write a JD?\"). Problems: <b>reactive</b>, no company context, generic answers."),
  ("Chatbot 2 — RAG based", "Adds company documents (policies, past JDs). Problem: still only <b>talks</b>, can't act (post a job, schedule interviews)."),
  ("Chatbot 3 — tool augmented", "Can call tools (post on LinkedIn, send emails). Problem: the <b>human must drive every step</b>; no memory of the overall goal, no adaptation."),
  ("Chatbot 4 — Agentic AI", "Given a goal (\"hire a backend engineer\"), it <b>plans</b>, uses tools, monitors progress (few applicants → widen the search), and asks for human approval at key points. <b>Proactive + autonomous.</b>"),
 ],
 code=[], remember=["GenAI = reactive content creation. Agentic AI = proactive goal completion (plan + act + adapt)."]),

dict(id="lg-02", yt="GWnSsjT4V68", dur="1:00:25", title="What is Agentic AI?",
 concepts=[
  ("Definition", "Software that takes a <b>goal</b> from the user and works toward it <b>with minimal human guidance</b>: it plans, takes actions, and adapts to changes."),
  ("Autonomy", "Makes decisions on its own. Must be <b>controlled</b>: limit scope/permissions, human-in-the-loop for risky actions, override buttons, guardrails."),
  ("Goal oriented", "Every action is directed at a goal; goals can have constraints and priorities; status is tracked (often in a JSON/state)."),
  ("Planning", "Breaks the goal into steps: generate multiple plans → evaluate (efficiency, tools, cost, risk) → pick the best."),
  ("Reasoning", "Interpreting information and making decisions during planning <b>and</b> execution (which tool, what args, handle errors)."),
  ("Adaptability", "Changes the plan when tools fail, results are unexpected, or the goal changes."),
  ("Context awareness", "Remembers the task state, conversation, tool outputs, user preferences → via <b>short-term and long-term memory</b>."),
  ("5 components", "<b>Brain</b> (LLM: reasoning, planning), <b>Orchestrator</b> (runs the steps, branches, loops, retries — LangGraph's job), <b>Tools</b> (act on the world), <b>Memory</b> (short + long term), <b>Supervisor</b> (HITL approvals, guardrails, escalations)."),
 ],
 code=[], remember=["6 traits: Autonomy, Goal-oriented, Planning, Reasoning, Adaptability, Context-aware.",
                    "5 parts: Brain, Orchestrator, Tools, Memory, Supervisor."]),

dict(id="lg-03", yt="31qyMKNB2RA", dur="1:27:29", title="LangChain vs LangGraph",
 concepts=[
  ("LangChain is good at", "Simple linear flows: prompt → LLM → parser, simple RAG, single tool calls."),
  ("Example: automated hiring workflow", "Create JD → approve? (loop back if not) → post → wait 7 days → enough applicants? (if not, modify & repost) → shortlist → interview → offer. Lots of <b>branches, loops and waiting</b>."),
  ("1. Control flow complexity", "LangChain needs lots of Python <b>glue code</b> (while loops, if/else) outside the chain. LangGraph: <b>conditional edges and loops are native</b>."),
  ("2. State handling", "LangChain is mostly stateless; you track variables yourself. LangGraph has a shared, typed <b>state object</b> that every node reads/updates."),
  ("3. Event-driven execution", "Waiting days for applicants = pause & resume. LangGraph supports this via <b>checkpointers + interrupts</b>."),
  ("4. Fault tolerance", "If step 5 crashes, LangGraph <b>resumes from the last checkpoint</b> instead of restarting."),
  ("5. Human in the loop", "Approval steps that may take hours. LangGraph: <code>interrupt()</code> + resume."),
  ("6. Nested workflows", "<b>Subgraphs</b> = a graph as a node → modular, reusable, multi-agent."),
  ("7. Observability", "Glue code is invisible to LangSmith; in LangGraph every node/edge is traced."),
 ],
 code=[], remember=["LangChain = building blocks for LLM apps. LangGraph = orchestration engine for stateful, multi-step, looping, branching workflows. Use both together."]),

dict(id="lg-04", yt="D5KhiCDM9XQ", dur="51:52", title="LangGraph Core Concepts",
 concepts=[
  ("LangGraph", "An <b>orchestration framework</b> that represents an LLM workflow as a <b>graph</b>: each node = a task (LLM call, tool, decision), edges = what runs next. Supports parallel, loops, branching, memory, resumability."),
  ("Workflow patterns", "<b>Prompt chaining</b> (sequential steps) · <b>Routing</b> (pick a path based on input) · <b>Parallelization</b> (split into independent subtasks, then merge) · <b>Orchestrator–workers</b> (orchestrator decides subtasks dynamically, workers do them) · <b>Evaluator–optimizer</b> (generate → critique → improve loop)."),
  ("Nodes", "Plain Python functions: <code>def node(state) -> dict</code>."),
  ("Edges", "Normal edges (A → B), conditional edges (choose next node with a function), parallel edges (A → B, A → C), loops."),
  ("State", "A shared memory (TypedDict / Pydantic) that flows through the graph. Every node receives the current state and returns <b>updates</b> (a partial dict)."),
  ("Reducers", "Decide <b>how an update is merged</b> into a state key. Default = <b>replace</b>. <code>operator.add</code> = append lists. <code>add_messages</code> = append/merge chat messages by ID. Needed when parallel nodes write the same key."),
  ("Execution model", "Inspired by Google <b>Pregel</b>: define graph → <code>compile()</code> → <code>invoke(initial_state)</code>. Execution runs in <b>super-steps</b>: nodes that received a message run (possibly in parallel), send updates along edges, and the run stops when no node is active."),
 ],
 code=[("Reducer cheat sheet", '''import operator
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    topic: str                                     # default: overwrite
    scores: Annotated[list[int], operator.add]     # [1] + [2] -> [1, 2]
    messages: Annotated[list, add_messages]        # append, update same-id msgs''')],
 remember=["Graph = Nodes (work) + Edges (flow) + State (shared memory) + Reducers (merge rules)."]),

dict(id="lg-05", yt="bAWujyAl1Kk", dur="49:13", title="Sequential Workflows",
 concepts=[
  ("5 steps to build any graph", "1) define <b>state</b> (TypedDict) → 2) write <b>node functions</b> → 3) <code>StateGraph(State)</code> + <code>add_node</code> → 4) <code>add_edge</code> from START ... to END → 5) <code>compile()</code> and <code>invoke()</code>."),
  ("BMI workflow", "Non-LLM example: calculate_bmi → label_bmi. Shows LangGraph is just a workflow engine."),
  ("Simple LLM workflow", "One node that calls the LLM (question → answer)."),
  ("Prompt chaining", "Title → outline → blog → rating; each node uses the previous node's output from state."),
  ("Visualise", "<code>workflow.get_graph().draw_mermaid_png()</code> or just show <code>workflow</code> in Jupyter."),
 ],
 code=[("Prompt chaining: outline → blog", LG_SETUP + '''

class BlogState(TypedDict):
    title: str
    outline: str
    content: str

def create_outline(state: BlogState):
    out = llm.invoke(f"Create a detailed outline for a blog on {state['title']}").content
    return {"outline": out}                    # return only what you change

def create_blog(state: BlogState):
    out = llm.invoke(f"Write a blog using this outline:\\n{state['outline']}").content
    return {"content": out}

graph = StateGraph(BlogState)
graph.add_node("create_outline", create_outline)
graph.add_node("create_blog", create_blog)
graph.add_edge(START, "create_outline")
graph.add_edge("create_outline", "create_blog")
graph.add_edge("create_blog", END)
workflow = graph.compile()

final = workflow.invoke({"title": "Rise of AI in India"})
print(final["content"])''')],
 remember=["Node returns a <b>partial dict</b> of updates; LangGraph merges it into state."]),

dict(id="lg-06", yt="O6ryuSpqdOw", dur="59:29", title="Parallel Workflows",
 concepts=[
  ("Parallel edges", "Add several edges from the same node (START → A, START → B, START → C). They run in the <b>same super-step</b>, then meet at a join node."),
  ("Batsman example (no LLM)", "Strike rate, balls-per-boundary, boundary % computed in parallel → summary."),
  ("Golden rule", "In parallel nodes, <b>return only the keys you changed</b>. Returning the full state makes all branches write every key → <code>InvalidUpdateError</code>."),
  ("UPSC essay evaluator", "3 parallel LLM evaluators (language, analysis, clarity) each returning structured output (feedback + score) → final node averages scores and summarises feedback."),
  ("Reducer for shared key", "All three write to <code>individual_scores</code>, so it must be <code>Annotated[list[int], operator.add]</code> to collect them instead of overwriting."),
 ],
 code=[("Fan-out / fan-in with a reducer", LG_SETUP + '''
import operator
from pydantic import BaseModel, Field

class Eval(BaseModel):
    feedback: str
    score: int = Field(ge=0, le=10)

judge = llm.with_structured_output(Eval)

class EssayState(TypedDict):
    essay: str
    scores: Annotated[list[int], operator.add]     # collects from all branches
    avg: float

def make_eval(aspect):
    def node(state: EssayState):
        r = judge.invoke(f"Evaluate the {aspect} of this essay:\\n{state['essay']}")
        return {"scores": [r.score]}
    return node

def final(state: EssayState):
    return {"avg": sum(state["scores"]) / len(state["scores"])}

g = StateGraph(EssayState)
for a in ["language", "analysis", "clarity"]:
    g.add_node(a, make_eval(a))
    g.add_edge(START, a)          # fan-out
    g.add_edge(a, "final")        # fan-in
g.add_node("final", final)
g.add_edge("final", END)
print(g.compile().invoke({"essay": "India in the age of AI ..."}))''')],
 remember=["Parallel writes to the same key → need a reducer."]),

dict(id="lg-07", yt="I-dvZqTz-Wc", dur="47:38", title="Conditional Workflows",
 concepts=[
  ("Conditional edge", "<code>add_conditional_edges(source, router_fn)</code>: after <code>source</code> runs, <code>router_fn(state)</code> returns the <b>name of the next node</b>."),
  ("Type hint the router", "<code>-> Literal[\"a\", \"b\"]</code> lets LangGraph draw the graph correctly. Or pass a mapping dict: <code>{\"approved\": END, \"retry\": \"optimize\"}</code>."),
  ("Quadratic equation example", "Compute discriminant → route to real_roots / repeated_roots / no_real_roots."),
  ("LLM review handling", "Classify review sentiment (structured output) → positive: thank-you reply; negative: run diagnosis (issue type, tone, urgency) → tailored reply."),
 ],
 code=[("Router with structured output", LG_SETUP + '''
from typing import Literal
from pydantic import BaseModel

class Sentiment(BaseModel):
    sentiment: Literal["positive", "negative"]

class ReviewState(TypedDict):
    review: str
    sentiment: str
    reply: str

def find_sentiment(state):
    s = llm.with_structured_output(Sentiment).invoke(f"Sentiment of: {state['review']}")
    return {"sentiment": s.sentiment}

def route(state) -> Literal["positive_reply", "negative_reply"]:
    return "positive_reply" if state["sentiment"] == "positive" else "negative_reply"

def positive_reply(state): return {"reply": llm.invoke(f"Thank the user for: {state['review']}").content}
def negative_reply(state): return {"reply": llm.invoke(f"Apologise and help with: {state['review']}").content}

g = StateGraph(ReviewState)
g.add_node("find_sentiment", find_sentiment)
g.add_node("positive_reply", positive_reply)
g.add_node("negative_reply", negative_reply)
g.add_edge(START, "find_sentiment")
g.add_conditional_edges("find_sentiment", route)
g.add_edge("positive_reply", END)
g.add_edge("negative_reply", END)
app = g.compile()''')],
 remember=["Router function returns a node NAME (string), not state."]),

dict(id="lg-08", yt="7CbSqrovcsE", dur="37:14", title="Iterative Workflows (Loops)",
 concepts=[
  ("Loop", "A conditional edge that can point <b>back</b> to an earlier node. This is the <b>evaluator–optimizer</b> pattern."),
  ("X/Twitter post generator", "<b>generate</b> (funny tweet) → <b>evaluate</b> (strict critic LLM, structured: approved / needs_improvement + feedback) → if not approved → <b>optimize</b> using feedback → evaluate again."),
  ("Stop condition", "Always cap loops: <code>iteration &gt;= max_iteration</code> → stop. Otherwise infinite loop / cost explosion. (LangGraph also has a <code>recursion_limit</code>, default 25.)"),
  ("History with reducers", "<code>tweet_history</code> and <code>feedback_history</code> use <code>operator.add</code> to keep every version."),
  ("Different LLMs per role", "generator / evaluator / optimizer can be different models (e.g. a stronger evaluator)."),
 ],
 code=[("Generate → evaluate → optimize loop", '''def route_evaluation(state):
    if state["evaluation"] == "approved" or state["iteration"] >= state["max_iteration"]:
        return "approved"
    return "needs_improvement"

g = StateGraph(TweetState)
g.add_node("generate", generate_tweet)
g.add_node("evaluate", evaluate_tweet)      # uses llm.with_structured_output(TweetEvaluation)
g.add_node("optimize", optimize_tweet)      # returns {"tweet": ..., "iteration": state["iteration"] + 1}

g.add_edge(START, "generate")
g.add_edge("generate", "evaluate")
g.add_conditional_edges("evaluate", route_evaluation,
                        {"approved": END, "needs_improvement": "optimize"})
g.add_edge("optimize", "evaluate")          # <-- the loop

app = g.compile()
app.invoke({"topic": "Indian Railways", "iteration": 1, "max_iteration": 5})''')],
 remember=["Every loop needs a max-iteration exit."]),

dict(id="lg-09", yt="51Ve2tE3Zns", dur="36:38", title="Build a Chatbot with LangGraph",
 concepts=[
  ("State with messages", "<code>messages: Annotated[list[BaseMessage], add_messages]</code> — every turn appends to the conversation."),
  ("add_messages vs operator.add", "<code>operator.add</code> blindly concatenates lists. <code>add_messages</code> also converts dicts/tuples to message objects and <b>replaces messages with the same ID</b> (needed for edits/deletes)."),
  ("Graph", "START → chat_node → END. chat_node sends all messages to the LLM and returns <code>{\"messages\": [response]}</code>."),
  ("Problem", "Without persistence, every <code>invoke</code> starts fresh → bot forgets. Fix in the next video (checkpointer)."),
 ],
 code=[("Basic chatbot", LG_SETUP + "\n" + CHAT_STATE + '''

def chat_node(state: ChatState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

g = StateGraph(ChatState)
g.add_node("chat_node", chat_node)
g.add_edge(START, "chat_node")
g.add_edge("chat_node", END)
chatbot = g.compile()

out = chatbot.invoke({"messages": [HumanMessage(content="Hi, I am Satya")]})
print(out["messages"][-1].content)''')],
 remember=["<code>MessagesState</code> is a built-in shortcut for exactly this ChatState."]),

dict(id="lg-10", yt="_IPP7_Bi8uA", dur="58:14", title="Persistence & Time Travel",
 concepts=[
  ("Persistence", "Saving the graph's state <b>to storage</b> so it can be resumed later. Normally state is lost when the run ends; with persistence it's saved <b>after every super-step</b> (not just the final state)."),
  ("Checkpointer", "The object that saves those snapshots: <code>InMemorySaver</code> (dev), <code>SqliteSaver</code>, <code>PostgresSaver</code> (prod). Pass via <code>graph.compile(checkpointer=...)</code>."),
  ("Checkpoint", "One saved snapshot of state at a super-step (has a <code>checkpoint_id</code>)."),
  ("Thread", "A separate conversation / run, identified by <code>thread_id</code> in <code>config={\"configurable\": {\"thread_id\": \"1\"}}</code>. Each thread has its own history."),
  ("get_state / get_state_history", "Read the latest snapshot, or all snapshots of a thread."),
  ("Benefits", "<b>Short-term memory</b> (chat remembers), <b>fault tolerance</b> (resume after crash by invoking with <code>None</code>), <b>human-in-the-loop</b> (pause/resume), <b>time travel</b>."),
  ("Time travel", "Replay from an old <code>checkpoint_id</code>, or <code>update_state</code> at an old checkpoint (e.g. change topic pizza → samosa) and re-run from there — creates a new branch."),
 ],
 code=[("Checkpointer, threads, time travel (from your 6_persistence)", '''from langgraph.checkpoint.memory import InMemorySaver

workflow = graph.compile(checkpointer=InMemorySaver())

config1 = {"configurable": {"thread_id": "1"}}
workflow.invoke({"topic": "pizza"}, config=config1)

workflow.get_state(config1)                 # latest snapshot
list(workflow.get_state_history(config1))   # all snapshots (newest first)

# time travel: replay from an old checkpoint
old = {"configurable": {"thread_id": "1", "checkpoint_id": "<id>"}}
workflow.invoke(None, old)

# edit the past, then continue from there
workflow.update_state(old, {"topic": "samosa"})
workflow.invoke(None, old)

# fault tolerance: after a crash, resume the same thread
workflow.invoke(None, config1)''')],
 remember=["No thread_id in config → error when a checkpointer is set.",
           "<code>invoke(None, config)</code> = resume, don't add new input."]),

dict(id="lg-11", yt="voZAgDmO-rk", dur="32:28", title="Chatbot UI with Streamlit",
 concepts=[
  ("Backend / frontend split", "<code>langgraph_backend.py</code> builds + compiles the graph (with checkpointer). <code>streamlit_frontend.py</code> handles the UI and imports <code>chatbot</code>."),
  ("st.chat_message / st.chat_input", "Streamlit's built-in chat bubbles and input box."),
  ("st.session_state", "Streamlit <b>reruns the whole script on every interaction</b>, so normal variables reset. <code>session_state</code> is a dict that survives reruns → store <code>message_history</code> there for display."),
  ("Two memories", "The UI history (session_state, for displaying) and the graph memory (checkpointer + thread_id, for the LLM)."),
 ],
 code=[("Minimal Streamlit chat", '''import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "thread-1"}}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

for m in st.session_state["message_history"]:          # re-draw old messages
    with st.chat_message(m["role"]):
        st.text(m["content"])

user_input = st.chat_input("Type here")
if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    res = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)
    ai = res["messages"][-1].content
    st.session_state["message_history"].append({"role": "assistant", "content": ai})
    with st.chat_message("assistant"):
        st.text(ai)''')],
 remember=["Run with <code>streamlit run streamlit_frontend.py</code>."]),

dict(id="lg-12", yt="D1PcZaeQ2eg", dur="25:00", title="Streaming",
 concepts=[
  ("Streaming", "Sending the response <b>token by token</b> as it's generated instead of waiting for the full answer."),
  ("Why", "Lower perceived latency (first token fast), feels human/ChatGPT-like, user can cancel early, better for long outputs, shows tool progress in agents."),
  ("graph.stream()", "<code>stream_mode=\"messages\"</code> yields <code>(message_chunk, metadata)</code> tuples token by token. Other modes: <code>\"values\"</code> (full state after each step), <code>\"updates\"</code> (only the changes per node), <code>\"custom\"</code>."),
  ("Streamlit", "<code>st.write_stream(generator)</code> renders the chunks live and returns the full text."),
 ],
 code=[("Stream tokens into the UI", '''with st.chat_message("assistant"):
    ai_message = st.write_stream(
        chunk.content
        for chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages",
        )
    )
# Gemini note: chunk.content can be a list -> use chunk.content[0]["text"] (as in your code)''')],
 remember=["values = full state · updates = per-node diff · messages = LLM tokens."]),

dict(id="lg-13", yt="N2nVG2MGWJ8", dur="39:40", title="Resume Chat (Multiple Conversations)",
 concepts=[
  ("Goal", "ChatGPT-like sidebar: start a <b>New Chat</b>, see all past chats, click one to resume it."),
  ("Key idea", "Each conversation = a separate <b>thread_id</b>. Generate it with <code>uuid.uuid4()</code>."),
  ("Pieces", "<code>generate_thread_id()</code>, <code>reset_chat()</code> (new thread + clear UI), <code>add_thread()</code> (store id in <code>session_state['chat_threads']</code>), <code>load_conversation(thread_id)</code> (read messages from the checkpointer via <code>chatbot.get_state(config).values['messages']</code>)."),
  ("Convert messages", "Checkpointer gives HumanMessage/AIMessage objects → convert to <code>{role, content}</code> dicts for the UI."),
  ("Task for you", "Show a title (LLM-generated summary) instead of the raw uuid — you did this with <code>generate_summary()</code>."),
 ],
 code=[("Thread helpers", '''import uuid

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    tid = generate_thread_id()
    st.session_state["thread_id"] = tid
    st.session_state["chat_threads"].append(tid)
    st.session_state["message_history"] = []

def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

if st.sidebar.button("New Chat"):
    reset_chat()
for tid in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(tid)):
        st.session_state["thread_id"] = tid
        msgs = load_conversation(tid)
        st.session_state["message_history"] = [
            {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content}
            for m in msgs]''')],
 remember=["New chat = new thread_id. Resume chat = same thread_id + get_state()."]),

dict(id="lg-14", yt="c6a47iX5JkU", dur="28:48", title="LangGraph + SQLite (Database)",
 concepts=[
  ("Problem", "<code>InMemorySaver</code> loses everything when the app restarts."),
  ("SqliteSaver", "Stores checkpoints in a SQLite file. <code>sqlite3.connect(..., check_same_thread=False)</code> because Streamlit uses multiple threads."),
  ("List all threads", "<code>checkpointer.list(None)</code> returns all checkpoints of all threads → collect unique <code>thread_id</code>s to rebuild the sidebar after restart."),
 ],
 code=[("Swap memory → SQLite", '''import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver     # pip install langgraph-checkpoint-sqlite

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    threads = set()
    for cp in checkpointer.list(None):                   # None = all threads
        threads.add(cp.config["configurable"]["thread_id"])
    return list(threads)''')],
 remember=["Only the checkpointer line changes — the graph stays the same."]),

dict(id="lg-15", yt="4FFspU4riHk", dur="2:07:40", title="LangSmith Crash Course (Observability)",
 concepts=[
  ("Why", "LLM apps are non-deterministic black boxes: a job-screening app suddenly takes 7 minutes, or a RAG bot gives wrong answers. You need to see <b>what happened inside</b>."),
  ("Observability", "Ability to understand the internal state of a system from its outputs (logs, metrics, traces)."),
  ("LangSmith", "LangChain's platform for tracing, debugging, testing, evaluating and monitoring LLM apps. Works with any framework."),
  ("What it traces", "Inputs/outputs of every step, prompts, intermediate steps, latency, <b>token usage and cost</b>, errors, metadata/tags, user feedback."),
  ("Core concepts", "<b>Project</b> (collection of traces) → <b>Trace</b> (one full execution of the app) → <b>Run</b> (one step inside, e.g. prompt/LLM/parser). Nested runs = spans."),
  ("@traceable", "Trace any normal Python function (e.g. PDF loading, splitting in a RAG app) that isn't a LangChain runnable."),
  ("Other features", "Monitoring & alerts dashboards, <b>datasets + evaluations</b> (run app on a test set, score with evaluators/LLM-as-judge), <b>prompt hub</b> / playground, annotation queues for human feedback."),
 ],
 code=[("Turn on tracing (no code changes needed for LangChain/LangGraph)", '''# .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=lsv2_...
LANGCHAIN_PROJECT=my-rag-app'''),
  ("Trace custom functions + add tags/metadata", '''from langsmith import traceable

@traceable(name="load_pdf", tags=["indexing"])
def load_pdf(path):
    return PyPDFLoader(path).load()

config = {"run_name": "qa_chain", "tags": ["v2", "gemini"], "metadata": {"user": "u1"}}
chain.invoke({"question": "..."}, config=config)''')],
 remember=["Project → Trace → Run.", "Only env vars needed for LangChain/LangGraph; @traceable for plain functions."]),

dict(id="lg-16", yt="ikzN6byFNWw", dur="21:40", title="Observability in LangGraph",
 concepts=[
  ("Integration", "Set the LangSmith env vars → every graph invocation becomes a trace, every node a run."),
  ("Threads in LangSmith", "Pass <code>thread_id</code> in config (plus metadata) → LangSmith groups all turns of one conversation into a <b>Thread</b> view."),
  ("Per-project naming", "<code>os.environ['LANGCHAIN_PROJECT'] = 'chat-bot-dashboard_v2'</code> (as in your backend)."),
 ],
 code=[("Group conversation turns", '''CONFIG = {
    "configurable": {"thread_id": thread_id},
    "metadata": {"thread_id": thread_id},
    "run_name": "chat_turn",
}
chatbot.invoke({"messages": [HumanMessage(content=q)]}, config=CONFIG)''')],
 remember=["thread_id in metadata → LangSmith 'Threads' tab shows full conversations."]),

dict(id="lg-17", yt="_UuUigoM9MA", dur="34:20", title="Tools in LangGraph",
 concepts=[
  ("Plan", "Give the chatbot tools: web search (DuckDuckGo), calculator, stock price (Alpha Vantage API)."),
  ("bind_tools", "<code>llm_with_tools = llm.bind_tools(tools)</code> so the LLM can request tools."),
  ("ToolNode", "Prebuilt node that <b>executes the tool calls</b> in the last AIMessage and returns ToolMessages. Node name must be <code>\"tools\"</code> for <code>tools_condition</code>."),
  ("tools_condition", "Prebuilt router: if the last AIMessage has <code>tool_calls</code> → go to <code>\"tools\"</code>, else → END."),
  ("The loop", "chat_node → (tools_condition) → tools → back to chat_node → ... until no more tool calls. This is a <b>ReAct agent</b> built by hand."),
 ],
 code=[("Tool-calling chatbot (from your 11_Tools)", LG_SETUP + "\n" + CHAT_STATE + '''
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

@tool
def calculator(a: float, b: float, op: str) -> float:
    """Do add, sub, mul or div on two numbers."""
    return {"add": a + b, "sub": a - b, "mul": a * b, "div": a / b}[op]

tools = [DuckDuckGoSearchRun(), calculator]
llm_with_tools = llm.bind_tools(tools)

def chat_node(state: ChatState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

g = StateGraph(ChatState)
g.add_node("chat_node", chat_node)
g.add_node("tools", ToolNode(tools))
g.add_edge(START, "chat_node")
g.add_conditional_edges("chat_node", tools_condition)   # tools or END
g.add_edge("tools", "chat_node")                        # loop back
chatbot = g.compile(checkpointer=checkpointer)''')],
 remember=["Prebuilt shortcut: <code>from langgraph.prebuilt import create_react_agent</code> / <code>langchain.agents.create_agent</code>."]),

dict(id="lg-18", yt="yZGjVA4uDc4", dur="44:31", title="MCP Client with LangGraph",
 concepts=[
  ("Problem with plain tools", "Every app re-implements tools for GitHub, Slack, DBs... and they <b>break</b> when the external API changes. N apps × M services = lots of brittle glue."),
  ("MCP", "<b>Model Context Protocol</b> (by Anthropic): a standard way to expose tools/resources/prompts. The <b>server</b> owns the tools (maintained by the service provider), the <b>client</b> (your app) just connects and lists them. Like USB-C for AI tools."),
  ("Transports", "<code>stdio</code> = server runs as a local subprocess. <code>streamable_http</code> (or SSE) = remote server over HTTP."),
  ("Why async", "MCP adapter libraries are <b>async-only</b> → nodes become <code>async def</code>, use <code>await llm.ainvoke()</code>, <code>await graph.ainvoke()</code>, <code>AsyncSqliteSaver</code>."),
  ("async basics", "<code>async def</code> = a function that may wait. <code>await</code> = wait here, let other work run meanwhile. <code>asyncio.run(main())</code> starts the event loop."),
  ("Streamlit + async", "Streamlit is sync, so your backend runs a dedicated event loop in a background thread and submits coroutines with <code>asyncio.run_coroutine_threadsafe</code>."),
 ],
 code=[("MCP server (FastMCP)", '''from fastmcp import FastMCP
mcp = FastMCP("calculator")

@mcp.tool()
async def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b

if __name__ == "__main__":
    mcp.run()                 # stdio by default'''),
  ("MCP client in LangGraph", '''import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({
    "calculator": {"transport": "stdio", "command": "python", "args": ["mcp_server.py"]},
    "expense":    {"transport": "streamable_http", "url": "https://.../mcp"},
})

async def build_graph():
    tools = await client.get_tools()          # MCP tools -> LangChain tools
    llm_with_tools = llm.bind_tools(tools)

    async def chat_node(state: ChatState):
        return {"messages": [await llm_with_tools.ainvoke(state["messages"])]}

    g = StateGraph(ChatState)
    g.add_node("chat_node", chat_node)
    g.add_node("tools", ToolNode(tools))
    g.add_edge(START, "chat_node")
    g.add_conditional_edges("chat_node", tools_condition)
    g.add_edge("tools", "chat_node")
    return g.compile()

async def main():
    app = await build_graph()
    out = await app.ainvoke({"messages": [HumanMessage("What is 23 + 19?")]})
    print(out["messages"][-1].content)

asyncio.run(main())''')],
 remember=["MCP = tools live on the server; your agent just connects. Client side = async."]),

dict(id="lg-19", yt="E1qP9Xsnmik", dur="37:12", title="RAG using LangGraph",
 concepts=[
  ("Why RAG", "Outdated knowledge, private documents, hallucination reduction. Give the LLM <b>relevant context</b> instead of pasting whole documents."),
  ("Approach", "Make RAG a <b>tool</b>: <code>rag_tool(query)</code> retrieves chunks from the uploaded PDF. The agent decides when to use it (and still uses other tools like stock price)."),
  ("Per-thread documents", "Each chat thread can upload its own PDF → store a retriever per thread in a dict <code>{thread_id: retriever}</code>; pass the thread_id to the tool."),
  ("Ingestion", "Uploaded bytes → temp file → PyPDFLoader → RecursiveCharacterTextSplitter → FAISS.from_documents → as_retriever."),
  ("Agentic RAG", "Retrieval as a tool the agent <b>chooses</b> to call (vs. always retrieving in a fixed chain)."),
 ],
 code=[("RAG as a tool", '''from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

docs = PyPDFLoader("notes.pdf").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
retriever = FAISS.from_documents(chunks, emb).as_retriever(search_kwargs={"k": 4})

@tool
def rag_tool(query: str) -> dict:
    """Retrieve relevant info from the uploaded PDF. Use for questions about the document."""
    result = retriever.invoke(query)
    return {"query": query,
            "context": [d.page_content for d in result],
            "metadata": [d.metadata for d in result]}

tools = [rag_tool, search_tool, calculator]     # then same ToolNode graph as before''')],
 remember=["Tool docstring tells the LLM WHEN to use the RAG tool."]),

dict(id="lg-20", yt="xxqZzVZ4gE0", dur="40:04", title="Human in the Loop (HITL)",
 concepts=[
  ("HITL", "Pausing the agent so a <b>human can approve, edit, or reject</b> before it continues."),
  ("Why", "Accuracy, <b>accountability</b>, safety for irreversible actions (send money, emails, delete data, buy stocks), compliance, trust."),
  ("Patterns", "Approve/reject an action · edit state/tool args · review a tool call · validate human input · multi-turn clarification."),
  ("interrupt()", "Call <code>interrupt(payload)</code> inside a node → graph <b>pauses</b>, state is saved, the payload shows up in <code>result[\"__interrupt__\"]</code>."),
  ("Command(resume=...)", "Resume by invoking with <code>Command(resume=value)</code> on the <b>same thread</b>; <code>interrupt()</code> returns that value and the node continues (the node re-runs from its start)."),
  ("Requirement", "A <b>checkpointer</b> is mandatory (state must be saved while waiting)."),
  ("Tool-chatbot example", "Ask approval inside a sensitive tool (e.g. <code>purchase_stock</code>) before executing."),
 ],
 code=[("Approve before answering (from your 14_hitl)", LG_SETUP + "\n" + CHAT_STATE + '''
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage

def chat_node(state: ChatState):
    decision = interrupt({"question": state["messages"][-1].content,
                          "instruction": "Approve? yes/no"})
    if decision["approved"] == "no":
        return {"messages": [AIMessage(content="Not approved.")]}
    return {"messages": [llm.invoke(state["messages"])]}

g = StateGraph(ChatState)
g.add_node("chat", chat_node)
g.add_edge(START, "chat"); g.add_edge("chat", END)
app = g.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "1234"}}
r = app.invoke({"messages": [("user", "Explain gradient descent")]}, config)
print(r["__interrupt__"][0].value)                 # paused here

final = app.invoke(Command(resume={"approved": "yes"}), config)
print(final["messages"][-1].content)''')],
 remember=["interrupt() pauses · Command(resume=...) continues · needs checkpointer + same thread_id."]),

dict(id="lg-21", yt="wcHcocpAoX4", dur="22:47", title="Subgraphs",
 concepts=[
  ("Subgraph", "A compiled graph used as a <b>node inside another graph</b>."),
  ("Why", "Complex workflows get huge; subgraphs give <b>modularity, reusability, maintainability</b>, team ownership, and are the base of <b>multi-agent</b> systems (each agent = a subgraph)."),
  ("Way 1 — different state (isolated)", "Subgraph has its own state schema. Call it <b>inside a node function</b>: map parent state → subgraph input, invoke, map output back."),
  ("Way 2 — shared state", "Subgraph uses the <b>same keys</b> as the parent → add the compiled subgraph <b>directly as a node</b>: <code>add_node(\"translate\", subgraph)</code>."),
  ("Example", "Parent: answer the question in English → subgraph: translate to Hindi."),
  ("Persistence", "Give the checkpointer only to the parent; it propagates to subgraphs. Subgraph runs appear nested in LangSmith."),
 ],
 code=[("Both ways", '''# Way 1: isolated state -> call inside a node
class SubState(TypedDict):
    input_text: str
    translated_text: str
# ... build & compile -> subgraph

def translate_answer(state: ParentState):
    out = subgraph.invoke({"input_text": state["answer_eng"]})
    return {"answer_hin": out["translated_text"]}
parent.add_node("translate", translate_answer)

# Way 2: shared state -> add compiled graph directly
sub = StateGraph(ParentState)          # same keys as parent
sub.add_node("translate_text", translate_text)
sub.add_edge(START, "translate_text"); sub.add_edge("translate_text", END)
parent.add_node("translate", sub.compile())''')],
 remember=["Different schema → wrap in a function. Same schema → add directly."]),

dict(id="lg-22", yt="DcPKJrOF9Wo", dur="57:44", title="How LLMs \"Remember\" (Memory theory)",
 concepts=[
  ("LLMs are stateless", "At inference the model only sees the current input. It has no memory between calls; the weights don't change."),
  ("Context window", "Max tokens the model can see in one call. Everything it 'remembers' must fit here. <b>In-context learning</b>: it uses whatever we put in the prompt."),
  ("Short-term memory (STM)", "Re-sending the <b>conversation history</b> each turn (within a thread/session). Implemented with a checkpointer in LangGraph."),
  ("STM limits", "Context overflow, cost and latency grow with length, 'lost in the middle', lost after the session ends."),
  ("Long-term memory (LTM)", "Information that persists <b>across sessions/threads</b>, stored outside the model and fetched when relevant."),
  ("3 types of LTM", "<b>Episodic</b> (past events/experiences: \"last week we debugged X\"), <b>Semantic</b> (facts about the user/world: \"user is a Python dev\"), <b>Procedural</b> (how to do things: rules, instructions, refined system prompt)."),
  ("LTM pipeline", "<b>Create/extract</b> memories (LLM decides what's worth saving) → <b>store</b> (DB / vector store) → <b>retrieve</b> relevant ones (semantic search) → <b>inject</b> into the prompt. Plus update/delete stale ones."),
  ("Tools", "LangGraph Store, Mem0, Zep, Letta (MemGPT), LangMem."),
 ],
 code=[], remember=["STM = within a thread (checkpointer). LTM = across threads (Store).",
                    "Episodic = events · Semantic = facts · Procedural = how-to."]),

dict(id="lg-23", yt="FSBkTI1QuvY", dur="52:46", title="Short-Term Memory in LangGraph",
 concepts=[
  ("STM = checkpointer + thread", "Same thread_id → history is reloaded every turn; new thread_id → fresh memory."),
  ("Production persistence", "InMemorySaver dies on restart → use <b>PostgresSaver</b> (Postgres via Docker). Call <code>checkpointer.setup()</code> once to create tables."),
  ("Context overflow", "Long chats exceed the context window / cost too much. 3 strategies:"),
  ("1. Trimming", "<code>trim_messages(strategy=\"last\", max_tokens=N)</code> → send only the latest messages that fit. Simple, but <b>old info is lost</b> (e.g. the user's name)."),
  ("2. Deletion", "Permanently remove old messages from state with <code>RemoveMessage(id=...)</code> (works because of <code>add_messages</code> reducer)."),
  ("3. Summarization", "When messages exceed a limit, an LLM <b>summarises</b> old messages into a <code>summary</code> key, delete them, keep the last few verbatim; inject the summary as a system message. Keeps the gist with few tokens."),
 ],
 code=[("Postgres checkpointer", '''# docker-compose: postgres:16, port 5442:5432
from langgraph.checkpoint.postgres import PostgresSaver
DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()                       # first time only
    graph = builder.compile(checkpointer=checkpointer)
    graph.invoke({"messages": [{"role": "user", "content": "Hi, I am Satya"}]},
                 {"configurable": {"thread_id": "t1"}})'''),
  ("Trimming", '''from langchain_core.messages.utils import trim_messages, count_tokens_approximately

def call_model(state: MessagesState):
    msgs = trim_messages(state["messages"], strategy="last",
                         token_counter=count_tokens_approximately, max_tokens=150)
    return {"messages": [llm.invoke(msgs)]}'''),
  ("Deletion", '''from langchain_core.messages import RemoveMessage

def delete_old(state: MessagesState):
    if len(state["messages"]) > 10:
        return {"messages": [RemoveMessage(id=m.id) for m in state["messages"][:6]]}
    return {}'''),
  ("Summarization", '''class ChatState(MessagesState):
    summary: str

def summarize(state: ChatState):
    prompt = (f"Existing summary:\\n{state['summary']}\\nExtend it with the new messages above."
              if state["summary"] else "Summarize the conversation above.")
    s = llm.invoke(state["messages"] + [HumanMessage(content=prompt)])
    return {"summary": s.content,
            "messages": [RemoveMessage(id=m.id) for m in state["messages"][:-2]]}

def chat(state: ChatState):
    msgs = ([{"role": "system", "content": f"Summary so far: {state['summary']}"}]
            if state["summary"] else []) + state["messages"]
    return {"messages": [llm.invoke(msgs)]}

builder.add_conditional_edges("chat", lambda s: len(s["messages"]) > 6,
                              {True: "summarize", False: END})''')],
 remember=["Trim = don't send (still stored). Delete = remove from state. Summarize = compress."]),

dict(id="lg-24", yt="KrXBcokM3Tc", dur="1:05:35", title="Long-Term Memory in LangGraph",
 concepts=[
  ("Store", "LangGraph's LTM component (separate from the checkpointer). Saves JSON <b>items</b> under a <b>namespace</b> tuple + <b>key</b>: <code>store.put((\"user\", \"u1\"), \"1\", {\"data\": ...})</code>."),
  ("Namespaces", "Like folders: <code>(\"user\", user_id, \"details\")</code> keeps each user's memories separate and shared across all their threads."),
  ("Operations", "<code>put</code>, <code>get(ns, key)</code>, <code>search(ns)</code> (all), <code>search(ns, query=..., limit=k)</code> (semantic), <code>delete</code>."),
  ("Semantic search", "Create the store with an embedding index: <code>InMemoryStore(index={\"embed\": emb, \"dims\": ...})</code> → search memories by meaning."),
  ("Using it in nodes", "<code>graph.compile(store=store)</code>; node signature <code>def node(state, config, *, store: BaseStore)</code>; get <code>user_id</code> from <code>config[\"configurable\"]</code>."),
  ("Memory extraction", "A <b>remember</b> node: LLM with structured output (<code>MemoryDecision{should_write, memories[{text, is_new}]}</code>) reads the latest message + existing memories and saves only new, atomic facts."),
  ("Chat node", "Loads the user's memories → puts them in the system prompt → personalised replies."),
  ("Production", "<code>PostgresStore</code> instead of <code>InMemoryStore</code> (<code>store.setup()</code> once)."),
 ],
 code=[("Store basics", '''from langgraph.store.memory import InMemoryStore

store = InMemoryStore(index={"embed": emb, "dims": 768})     # index optional
ns = ("user", "u1")
store.put(ns, "1", {"data": "User likes examples in Python"})
store.put(ns, "2", {"data": "User is learning LangGraph"})

store.get(ns, "1").value
for item in store.search(ns, query="what is the user learning?", limit=2):
    print(item.value)'''),
  ("Remember node + chat node", '''import uuid
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore

def remember(state: MessagesState, config: RunnableConfig, *, store: BaseStore):
    ns = ("user", config["configurable"]["user_id"], "details")
    existing = "\\n".join(i.value["data"] for i in store.search(ns)) or "(empty)"
    d = memory_extractor.invoke([SystemMessage(MEMORY_PROMPT.format(user_details_content=existing)),
                                 state["messages"][-1]])
    if d.should_write:
        for m in d.memories:
            if m.is_new:
                store.put(ns, str(uuid.uuid4()), {"data": m.text})
    return {}

def chat(state: MessagesState, config: RunnableConfig, *, store: BaseStore):
    ns = ("user", config["configurable"]["user_id"], "details")
    mem = "\\n".join(i.value["data"] for i in store.search(ns))
    sys = SystemMessage(f"Personalise using what you know about the user:\\n{mem}")
    return {"messages": [llm.invoke([sys] + state["messages"])]}

# START -> remember -> chat -> END
graph = builder.compile(store=store, checkpointer=checkpointer)
graph.invoke({"messages": [...]}, {"configurable": {"user_id": "u1", "thread_id": "t9"}})''')],
 remember=["Checkpointer → per thread (STM). Store → per user, across threads (LTM)."]),

dict(id="lg-25", yt="Ou_v9lk0rxg", dur="1:20:04", title="Project: Blog-Writing Agent (Planning Agent)",
 concepts=[
  ("Planning agent", "Instead of writing the blog in one shot, it first <b>plans</b> (outline with sections, goals, word counts), then executes each part, then assembles."),
  ("Orchestrator–worker pattern", "<b>Orchestrator</b> makes a plan (structured output: list of tasks). <b>Workers</b> write each section <b>in parallel</b>. <b>Reducer/synthesizer</b> merges sections into the final blog."),
  ("Send API", "Dynamic fan-out: the number of workers is unknown until runtime → a conditional edge returns <code>[Send(\"worker\", payload) for each task]</code>."),
  ("Stage 2 — research", "A <b>router</b> decides if the topic needs fresh info → <b>Tavily</b> web search → research-aware planning."),
  ("Stage 3 — images", "Decide where images help, generate them, and place them with reducer logic."),
  ("Stage 4 — UI", "Streamlit frontend to enter a topic and view/download the blog."),
 ],
 code=[("Orchestrator–worker with Send", LG_SETUP + '''
import operator
from langgraph.types import Send
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    brief: str
class Plan(BaseModel):
    tasks: list[Task]

class State(TypedDict):
    topic: str
    plan: Plan
    sections: Annotated[list[str], operator.add]   # workers append here
    final: str

def orchestrator(state):
    return {"plan": llm.with_structured_output(Plan).invoke(f"Plan a blog on {state['topic']}")}

def fan_out(state):
    return [Send("worker", {"task": t}) for t in state["plan"].tasks]

def worker(payload):
    t = payload["task"]
    return {"sections": [llm.invoke(f"Write section '{t.title}': {t.brief}").content]}

def reducer(state):
    return {"final": "\\n\\n".join(state["sections"])}

g = StateGraph(State)
g.add_node("orchestrator", orchestrator)
g.add_node("worker", worker)
g.add_node("reducer", reducer)
g.add_edge(START, "orchestrator")
g.add_conditional_edges("orchestrator", fan_out, ["worker"])
g.add_edge("worker", "reducer")
g.add_edge("reducer", END)
app = g.compile()''')],
 remember=["Static parallel = fixed edges. Dynamic parallel (N unknown) = Send API."]),

dict(id="lg-26", yt="41XDn81nR5c", dur="1:15:09", title="Corrective RAG (CRAG)",
 concepts=[
  ("Problem: blind trust", "Traditional RAG always trusts whatever the retriever returns. For out-of-distribution questions (e.g. recent AI news against an ML-books DB), it retrieves irrelevant chunks and the LLM <b>hallucinates</b>."),
  ("CRAG idea", "Add a <b>retrieval evaluator</b> that grades retrieved docs, then corrects the retrieval before generating."),
  ("3 cases", "<b>Correct</b> (score above upper threshold) → use docs after <b>knowledge refinement</b>. <b>Incorrect</b> (all below lower threshold) → discard, do <b>web search</b>. <b>Ambiguous</b> → combine refined docs + web search."),
  ("Knowledge refinement", "Split docs into small <b>strips</b> (sentences), keep only strips the grader marks relevant, recompose → less noise."),
  ("Query rewriting", "Before web search, rewrite the question into a good search query."),
 ],
 code=[("CRAG graph skeleton", '''class CragState(TypedDict):
    question: str
    docs: list
    verdict: str          # CORRECT / INCORRECT / AMBIGUOUS
    web_docs: list
    answer: str

class DocScore(BaseModel):
    score: float          # 0..1 relevance

def retrieve(s): return {"docs": retriever.invoke(s["question"])}

def grade(s):
    scores = [llm.with_structured_output(DocScore)
                 .invoke(f"Relevance of doc to '{s['question']}':\\n{d.page_content}").score
              for d in s["docs"]]
    if any(x > 0.7 for x in scores):   v = "CORRECT"
    elif all(x < 0.3 for x in scores): v = "INCORRECT"
    else:                              v = "AMBIGUOUS"
    return {"verdict": v}

def refine(s): ...        # split into sentences, keep relevant strips
def web_search(s): ...    # rewrite query -> Tavily
def generate(s): ...      # answer ONLY from refined + web context

g.add_edge(START, "retrieve"); g.add_edge("retrieve", "grade")
g.add_conditional_edges("grade", lambda s: s["verdict"],
    {"CORRECT": "refine", "INCORRECT": "web_search", "AMBIGUOUS": "refine"})
# AMBIGUOUS: refine -> web_search -> generate''')],
 remember=["CRAG = grade retrieval → Correct: refine · Incorrect: web search · Ambiguous: both."]),

dict(id="lg-27", yt="BbO_XaEjzaA", dur="1:08:40", title="Self-RAG",
 concepts=[
  ("3 problems of traditional RAG", "1) <b>Unnecessary retrieval</b> (retrieves even for \"hi\" or general knowledge), 2) <b>blind trust</b> in documents, 3) <b>no answer verification</b>."),
  ("Self-RAG", "Self-reflective RAG: the LLM <b>critiques itself</b> at each step."),
  ("4 questions it asks", "1) Do I need retrieval? 2) Are the retrieved docs relevant? 3) Is my answer <b>supported</b> by the docs (no hallucination)? 4) Is the answer <b>useful</b> for the question?"),
  ("Flow", "decide_retrieval → (no: answer directly) / (yes: retrieve → filter relevant docs → generate) → check support → if not supported: <b>revise</b> answer (loop, capped) → check usefulness → if not useful: <b>rewrite query</b> and retrieve again."),
  ("vs CRAG", "CRAG focuses on fixing <b>retrieval</b> (fallback to web). Self-RAG adds <b>generation checks</b> (hallucination + usefulness) and decides whether to retrieve at all."),
 ],
 code=[("Self-RAG routing skeleton", '''class YesNo(BaseModel):
    decision: Literal["yes", "no"]
judge = llm.with_structured_output(YesNo)

def decide_retrieval(s):
    d = judge.invoke(f"Does answering need external documents? Q: {s['question']}")
    return {"need_retrieval": d.decision == "yes"}

def is_supported(s):
    d = judge.invoke(f"Is every claim in the answer supported by the context?\\n"
                     f"Context: {s['context']}\\nAnswer: {s['answer']}")
    return "supported" if d.decision == "yes" or s["revisions"] >= 2 else "revise"

def is_useful(s):
    d = judge.invoke(f"Does this answer the question '{s['question']}'?\\n{s['answer']}")
    return "end" if d.decision == "yes" or s["rewrites"] >= 2 else "rewrite_query"

g.add_conditional_edges("decide_retrieval", lambda s: "retrieve" if s["need_retrieval"] else "direct_answer")
g.add_edge("retrieve", "filter_docs"); g.add_edge("filter_docs", "generate")
g.add_conditional_edges("generate", is_supported, {"supported": "check_useful", "revise": "revise"})
g.add_edge("revise", "generate")
g.add_conditional_edges("check_useful", is_useful, {"end": END, "rewrite_query": "rewrite_query"})
g.add_edge("rewrite_query", "retrieve")''')],
 remember=["Self-RAG: Retrieve? → Relevant? → Supported? → Useful?"]),

dict(id="lg-28", yt=None, dur="your notebook", title="AI Agent Evaluation",
 concepts=[
  ("Why evaluate agents", "Agents are non-deterministic, multi-step and use tools — a correct-looking answer can come from a wrong path. You need tests before shipping and monitoring after."),
  ("1. Final answer correctness", "Does the answer contain/match the expected result? (exact match, keywords, or LLM-as-judge for open answers)."),
  ("2. Tool selection", "Did it call the <b>right tools</b> (compare with expected set, e.g. <code>Counter(used) == Counter(expected)</code>)?"),
  ("3. Trajectory", "Did it call them in the <b>right order</b> (the full path of steps)? Strict match or subset/unordered match."),
  ("4. Latency", "Correct but too slow = bad production agent. Track per test and p50/p95 in production."),
  ("5. Safety & reliability", "Refuses harmful requests, no forbidden content, handles unknown/invalid inputs gracefully (\"I don't know\" instead of inventing)."),
  ("Eval dataset", "List of test cases: question, expected answer keywords, expected tools, expected trajectory, max latency, type (normal / safety / reliability)."),
  ("LLM-as-a-judge", "Use an LLM with a rubric (correct, relevant, helpful, no invented facts) to grade open-ended answers. Watch out for judge bias; keep the rubric strict and use a strong model."),
  ("Offline vs online", "<b>Offline</b> (before deploy): regression tests, known-answer datasets, tool/trajectory tests, prompt-injection suites, latency benchmarks. <b>Online</b> (after deploy): production traces, user feedback, task success, latency percentiles, tool failure rate, safety incidents. Mature teams do both."),
 ],
 code=[("Mini evaluation harness", '''import time
from collections import Counter

def run_agent(q):
    t = time.perf_counter()
    res = agent.invoke({"messages": [{"role": "user", "content": q}]})
    tools = [c["name"] for m in res["messages"] for c in (getattr(m, "tool_calls", None) or [])]
    return {"answer": res["messages"][-1].content, "tools": tools,
            "latency": time.perf_counter() - t}

tests = [{"q": "Price of the GenAI course for 3 people?", "expect": ["300"],
          "tools": ["get_course_price", "multiply"], "max_s": 10}]

for t in tests:
    r = run_agent(t["q"])
    checks = {
        "answer":     any(e in r["answer"] for e in t["expect"]),
        "tools":      Counter(r["tools"]) == Counter(t["tools"]),
        "trajectory": r["tools"] == t["tools"],
        "latency":    r["latency"] <= t["max_s"],
    }
    print(t["q"], checks, f"score={100*sum(checks.values())/len(checks):.0f}%")'''),
  ("LLM-as-a-judge", '''def llm_as_judge(question, answer):
    prompt = f"""Evaluate the answer.
QUESTION: {question}
ANSWER: {answer}
Criteria: correct, relevant, helpful, no invented facts.
Return: VERDICT: PASS or FAIL / REASON: <one line>"""
    return judge_llm.invoke(prompt).content''')],
 remember=["Agent eval = Answer + Tools + Trajectory + Latency + Safety.", "Offline before deploy, online after."]),

dict(id="lg-29", yt=None, dur="your notebook", title="Guardrails",
 concepts=[
  ("Guardrails", "Checks that keep an agent safe and on-policy: <b>input guardrails</b> run before the agent (block jailbreaks, PII, off-topic), <b>output guardrails</b> run after (block unsafe/incorrect content, leaked secrets)."),
  ("Use cases", "PII protection, prompt-injection defence, blocking harmful content, enforcing business rules, compliance (health/finance), approval for risky tool calls."),
  ("Deterministic guardrails", "Rules: regex, keyword lists, allow/deny lists, length limits. <b>Fast, cheap, predictable</b>, but miss paraphrases."),
  ("Model-based guardrails", "An LLM/classifier judges content (SAFE/UNSAFE). <b>Understands meaning</b>, but slower, costs money, can be wrong. Best: combine both."),
  ("Middleware (LangChain 1.x)", "<code>create_agent(..., middleware=[...])</code>. Hooks: <code>before_agent</code>, <code>before_model</code>, <code>after_model</code>, <code>after_agent</code> (and wrap tool calls)."),
  ("PIIMiddleware", "Detects email, credit_card, ip, mac_address, url (or custom regex). Strategies: <b>redact</b> (replace with [REDACTED_EMAIL]), <b>mask</b> (****-5100), <b>hash</b>, <b>block</b> (raise error). <code>apply_to_input</code> / <code>apply_to_output</code>."),
  ("HumanInTheLoopMiddleware", "<code>interrupt_on={\"send_email\": True, \"search\": False}</code> → pauses before chosen tools; resume with <code>Command(resume={\"decisions\": [{\"type\": \"approve\"}]})</code> or <code>reject</code>/<code>edit</code>. Needs a checkpointer."),
  ("Custom middleware", "Subclass <code>AgentMiddleware</code>; in <code>before_agent</code> check the input and return <code>{\"messages\": [...], \"jump_to\": \"end\"}</code> to stop early (decorate with <code>@hook_config(can_jump_to=[\"end\"])</code>). <code>after_agent</code> for output checks."),
  ("Layered guardrails", "Stack middlewares in order: content filter → PII on input → HITL for risky tools → PII on output → safety check on output. (Healthcare bot example: block emergencies/diagnosis requests, add disclaimers.)"),
 ],
 code=[("Deterministic vs model-based", '''import re
def deterministic_guardrail(text: str) -> bool:          # True = block
    return bool(re.search(r"\\b(hack|exploit|malware)\\b", text, re.I))

def model_based_guardrail(text: str) -> str:
    prompt = f"Is this request harmful or unsafe? Answer only SAFE or UNSAFE.\\n{text}"
    return model.invoke(prompt).content.strip()'''),
  ("Built-in middlewares", '''from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware, HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

agent = create_agent(
    model=llm, tools=[search_web, send_email],
    checkpointer=InMemorySaver(),
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
        PIIMiddleware("api_key", detector=r"sk-[a-zA-Z0-9]{32}", strategy="block"),
        HumanInTheLoopMiddleware(interrupt_on={"send_email": True, "search_web": False}),
    ],
)
cfg = {"configurable": {"thread_id": "1"}}
agent.invoke({"messages": [{"role": "user", "content": "Email team@x.com the Q4 results"}]}, cfg)
agent.invoke(Command(resume={"decisions": [{"type": "approve"}]}), cfg)'''),
  ("Custom input filter middleware", '''from typing import Any
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime

class ContentFilterMiddleware(AgentMiddleware):
    def __init__(self, banned_keywords: list[str]):
        super().__init__()
        self.banned = [k.lower() for k in banned_keywords]

    @hook_config(can_jump_to=["end"])
    def before_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        text = str(state["messages"][-1].content).lower()
        if any(k in text for k in self.banned):
            return {"messages": [{"role": "assistant",
                                  "content": "I can't help with that request."}],
                    "jump_to": "end"}
        return None''')],
 remember=["Input guardrails before, output guardrails after. Rules (fast) + LLM checks (smart) together.",
           "PII strategies: redact · mask · hash · block."]),
]
