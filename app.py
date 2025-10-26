import streamlit as st
from exa_py import Exa
from cerebras.cloud.sdk import Cerebras
import json

# Page configuration
st.set_page_config(
    page_title="Cerebras Deep Research",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
    }
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        color: #ff6b35;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
    }
    .example-card {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #333;
        cursor: pointer;
        transition: all 0.3s;
        height: 100%;
    }
    .example-card:hover {
        border-color: #ff6b35;
        transform: translateY(-2px);
    }
    .source-card {
        background-color: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #ff6b35;
        margin-bottom: 1rem;
    }
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    .api-input {
        background-color: #2a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'sources' not in st.session_state:
    st.session_state.sources = []
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []
if 'exa_api_key' not in st.session_state:
    st.session_state.exa_api_key = ""
if 'cerebras_api_key' not in st.session_state:
    st.session_state.cerebras_api_key = ""

# Sidebar for API Keys and Settings
with st.sidebar:
    st.markdown("### 🔑 API Keys")
    
    exa_key = st.text_input(
        "Exa API Key",
        type="password",
        value=st.session_state.exa_api_key,
        placeholder="Enter your Exa API key...",
        help="Get your free API key at https://exa.ai"
    )
    if exa_key:
        st.session_state.exa_api_key = exa_key
    else:
        st.markdown("[Get API Key →](https://exa.ai/?utm_source=cerebras-research)")
    
    cerebras_key = st.text_input(
        "Cerebras API Key",
        type="password",
        value=st.session_state.cerebras_api_key,
        placeholder="Enter your Cerebras API key...",
        help="Get your free API key at https://cloud.cerebras.ai"
    )
    if cerebras_key:
        st.session_state.cerebras_api_key = cerebras_key
    else:
        st.markdown("[Get API Key →](https://cloud.cerebras.ai?utm_source=exademo)")
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    research_mode = st.selectbox(
        "Research Mode",
        ["Enhanced Research (2-Layer)", "Multi-Agent Research", "Basic Research"]
    )
    
    num_sources = st.slider("Number of Sources", 3, 10, 5)
    
    st.markdown("---")
    st.markdown("### 📚 About")
    st.markdown("""
    This AI-powered research assistant:
    - 🔍 Searches the web intelligently
    - 📊 Analyzes multiple sources
    - 💡 Provides structured insights
    - ⚡ Completes in under 60 seconds
    """)

# Helper Functions
def search_web(exa, query, num=5):
    """Search the web using Exa's auto search"""
    result = exa.search_and_contents(
        query,
        type="auto",
        num_results=num,
        text={"max_characters": 1000}
    )
    return result.results

def ask_ai(client, prompt):
    """Get AI response from Cerebras"""
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-4-scout-17b-16e-instruct",
        max_tokens=600,
        temperature=0.2
    )
    return chat_completion.choices[0].message.content

def deeper_research_topic(exa, client, query, num_sources):
    """Two-layer research for better depth"""
    st.session_state.activity_log.append(f"🔍 Starting research: {query}")
    
    # Layer 1: Initial search
    with st.spinner("🔍 Layer 1: Initial search..."):
        results = search_web(exa, query, num_sources)
        sources = []
        for result in results:
            if result.text and len(result.text) > 200:
                sources.append({"title": result.title, "content": result.text, "url": result.url})
        
        st.session_state.activity_log.append(f"📊 Layer 1: Found {len(sources)} sources")
    
    if not sources:
        return {"summary": "No sources found", "insights": []}
    
    # Get follow-up query
    with st.spinner("🤔 Analyzing and planning follow-up..."):
        context1 = f"Research query: {query}\n\nSources:\n"
        for i, source in enumerate(sources[:4], 1):
            context1 += f"{i}. {source['title']}: {source['content'][:300]}...\n\n"
        
        follow_up_prompt = f"""{context1}
Based on these sources, what's the most important follow-up question that would deepen our understanding of "{query}"?
Respond with just a specific search query (no explanation):"""
        
        follow_up_query = ask_ai(client, follow_up_prompt).strip().strip('"')
        st.session_state.activity_log.append(f"🎯 Layer 2 focus: {follow_up_query}")
    
    # Layer 2: Follow-up search
    with st.spinner(f"🔍 Layer 2: Investigating '{follow_up_query}'..."):
        follow_results = search_web(exa, follow_up_query, 4)
        for result in follow_results:
            if result.text and len(result.text) > 200:
                sources.append({
                    "title": f"[Follow-up] {result.title}",
                    "content": result.text,
                    "url": result.url
                })
        
        st.session_state.activity_log.append(f"📚 Total sources: {len(sources)}")
    
    # Final synthesis
    with st.spinner("🧠 Synthesizing findings..."):
        all_context = f"Research query: {query}\nFollow-up: {follow_up_query}\n\nAll Sources:\n"
        for i, source in enumerate(sources[:7], 1):
            all_context += f"{i}. {source['title']}: {source['content'][:300]}...\n\n"
        
        final_prompt = f"""{all_context}
Provide a comprehensive analysis:

SUMMARY: [3-4 sentences covering key findings from both research layers]

INSIGHTS:
- [insight 1]
- [insight 2]
- [insight 3]
- [insight 4]

DEPTH GAINED: [1 sentence on how the follow-up search enhanced understanding]"""
        
        response = ask_ai(client, final_prompt)
        st.session_state.activity_log.append("✅ Research complete")
    
    st.session_state.sources = sources
    return {"query": query, "sources": len(sources), "response": response}

def anthropic_multiagent_research(exa, client, query, num_sources):
    """Multi-agent research approach"""
    st.session_state.activity_log.append(f"🤖 Multi-agent research: {query}")
    
    # Task decomposition
    with st.spinner("👨‍💼 Planning and delegating to subagents..."):
        delegation_prompt = f"""You are a Lead Research Agent. Break down this complex query into 3 specialized subtasks for parallel execution: "{query}"

For each subtask, provide:
- Clear objective
- Specific search focus
- Expected output

SUBTASK 1: [Core/foundational aspects]
SUBTASK 2: [Recent developments/trends]
SUBTASK 3: [Applications/implications]

Make each subtask distinct to avoid overlap."""
        
        plan = ask_ai(client, delegation_prompt)
        st.session_state.activity_log.append("✓ Subtasks defined")
    
    # Parallel subagent execution
    subtask_searches = [
        f"{query} fundamentals principles",
        f"{query} latest developments",
        f"{query} applications real world"
    ]
    
    subagent_results = []
    sources = []
    
    for i, search_term in enumerate(subtask_searches, 1):
        with st.spinner(f"🤖 Subagent {i}: Researching {search_term}..."):
            results = search_web(exa, search_term, 2)
            agent_sources = []
            
            for result in results:
                if result.text and len(result.text) > 200:
                    source = {
                        "title": result.title,
                        "content": result.text[:300],
                        "url": result.url
                    }
                    agent_sources.append(source)
                    sources.append(source)
            
            subagent_results.append({
                "subtask": i,
                "search_focus": search_term,
                "sources": agent_sources
            })
            
            st.session_state.activity_log.append(f"🤖 Subagent {i} complete")
    
    # Synthesis
    with st.spinner("👨‍💼 Synthesizing parallel findings..."):
        synthesis_context = f"ORIGINAL QUERY: {query}\n\nSUBAGENT FINDINGS:\n"
        for result in subagent_results:
            synthesis_context += f"\nSubagent {result['subtask']} ({result['search_focus']}):\n"
            for source in result['sources'][:2]:
                synthesis_context += f"- {source['title']}: {source['content']}...\n"
        
        synthesis_prompt = f"""{synthesis_context}

As the Lead Agent, synthesize these parallel findings into a comprehensive report:

EXECUTIVE SUMMARY:
[2-3 sentences covering the most important insights across all subagents]

INTEGRATED FINDINGS:
• [Key finding from foundational research]
• [Key finding from recent developments]
• [Key finding from applications research]
• [Cross-cutting insight that emerged]

RESEARCH QUALITY:
- Sources analyzed: {len(sources)} across {len(subagent_results)} specialized agents
- Coverage: [How well the subtasks covered the topic]"""
        
        final_synthesis = ask_ai(client, synthesis_prompt)
        st.session_state.activity_log.append("✅ Multi-agent research complete")
    
    st.session_state.sources = sources
    return {"query": query, "sources": len(sources), "response": final_synthesis}

def basic_research(exa, client, query, num_sources):
    """Basic single-layer research"""
    st.session_state.activity_log.append(f"🔍 Basic research: {query}")
    
    with st.spinner("🔍 Searching sources..."):
        results = search_web(exa, query, num_sources)
        sources = []
        for result in results:
            if result.text and len(result.text) > 200:
                sources.append({"title": result.title, "content": result.text, "url": result.url})
    
    if not sources:
        return {"summary": "No sources found", "insights": []}
    
    with st.spinner("🧠 Analyzing sources..."):
        context = f"Research query: {query}\n\nSources:\n"
        for i, source in enumerate(sources[:4], 1):
            context += f"{i}. {source['title']}: {source['content'][:400]}...\n\n"
        
        prompt = f"""{context}

Based on these sources, provide:
1. A comprehensive summary (2-3 sentences)
2. Three key insights as bullet points

Format your response exactly like this:
SUMMARY: [your summary here]

INSIGHTS:
- [insight 1]
- [insight 2]
- [insight 3]"""
        
        response = ask_ai(client, prompt)
        st.session_state.activity_log.append("✅ Research complete")
    
    st.session_state.sources = sources
    return {"query": query, "sources": len(sources), "response": response}

# Main App
st.markdown('<div class="main-header">Cerebras Deep Research</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered research that goes deeper than search</div>', unsafe_allow_html=True)

# Example prompts
st.markdown("### 💡 Example Research Topics")
col1, col2, col3 = st.columns(3)

example_prompts = [
    "What are the most promising approaches to fusion energy?",
    "What are the latest developments in quantum computing?",
    "How can AI help solve climate change challenges?"
]

with col1:
    if st.button(example_prompts[0], use_container_width=True):
        st.session_state.query = example_prompts[0]

with col2:
    if st.button(example_prompts[1], use_container_width=True):
        st.session_state.query = example_prompts[1]

with col3:
    if st.button(example_prompts[2], use_container_width=True):
        st.session_state.query = example_prompts[2]

st.markdown("---")

# Search input
col1, col2 = st.columns([5, 1])
with col1:
    query = st.text_input(
        "research_query",
        placeholder="What would you like to research?",
        label_visibility="collapsed",
        value=st.session_state.get('query', '')
    )
with col2:
    search_button = st.button("🔍 Research", use_container_width=True, type="primary")

# Process research
if search_button and query:
    if not st.session_state.exa_api_key or not st.session_state.cerebras_api_key:
        st.error("⚠️ Please configure your API keys in the sidebar!")
    else:
        try:
            # Initialize clients
            exa = Exa(api_key=st.session_state.exa_api_key)
            client = Cerebras(api_key=st.session_state.cerebras_api_key)
            
            # Clear previous results
            st.session_state.activity_log = []
            st.session_state.sources = []
            
            # Perform research based on mode
            if research_mode == "Enhanced Research (2-Layer)":
                result = deeper_research_topic(exa, client, query, num_sources)
            elif research_mode == "Multi-Agent Research":
                result = anthropic_multiagent_research(exa, client, query, num_sources)
            else:
                result = basic_research(exa, client, query, num_sources)
            
            st.session_state.research_results = result
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please check your API keys and try again.")

# Display results in tabs
if st.session_state.research_results:
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📊 Results", "📚 Sources", "⚡ Activity"])
    
    with tab1:
        st.markdown("### 🎯 Research Results")
        st.markdown(st.session_state.research_results['response'])
        
        st.markdown("---")
        st.info(f"📊 Analyzed {st.session_state.research_results['sources']} sources")
    
    with tab2:
        st.markdown("### 📚 Sources")
        for i, source in enumerate(st.session_state.sources, 1):
            with st.expander(f"{i}. {source['title']}", expanded=False):
                st.markdown(f"**Content Preview:**\n\n{source['content'][:500]}...")
                if 'url' in source:
                    st.markdown(f"[🔗 Read full article]({source['url']})")
    
    with tab3:
        st.markdown("### ⚡ Activity Log")
        for log in st.session_state.activity_log:
            st.text(log)