import streamlit as st
import time
import base64
from chatbot import Chatbot

@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception:
        return None

bg_image = get_base64_image("botim.jpg")

css = f"""
<style>
.stApp {{
    {"background-image: url('data:image/jpeg;base64," + bg_image + "');" if bg_image else "background: linear-gradient(118deg, #121326 45%, #2b315d 100%);"}
    background-blend-mode: overlay;
    background-size: cover;
    background-position: center;
    min-height: 100vh;
    position: relative;
}}
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background: linear-gradient(135deg, rgba(17,26,49,0.83) 66%, rgba(18,241,255,0.19) 120%);
    z-index: 0;
}}
.main-title {{
    font-family: 'Orbitron', 'Inter', serif;
    letter-spacing: 2px;
    font-size: 2.7rem;
    text-align: center;
    color: #62eaff; 
    margin: 30px 0 16px 0;
    text-shadow: 0 0 7px #23d3fb, 0 0 18px #3cf8ff, 0 0 35px #39d4e6;
    animation: flicker 2s linear infinite;
}}
@keyframes flicker {{
  0%,100% {{opacity:1;}}
  47%,53% {{opacity:0.86;}}
  49%,51% {{opacity:0.79;}}
}}
@keyframes popMe {{
    0% {{ transform: scale(0.78) translateY(38px) skewY(7deg); opacity:0; }}
    100% {{ transform: scale(1) translateY(0) skewY(0); opacity:1; }}
}}
.user-bubble, .assistant-bubble {{
    display:inline-block; font-size:1.10rem; line-height:1.65;
    padding: 14px 19px; max-width:81vw;
    border-radius: 1.4em 1.4em 0.6em 1.4em;
    margin-bottom:10px; position:relative;
    animation: popMe 0.55s cubic-bezier(.23,1.03,.51,.97) both;
    box-shadow: 0 4px 28px 2px #31e5ef4b;
}}
.user-bubble {{
    background: linear-gradient(99deg, #072060 55%, #50e8eeab 100%);
    color: #edfcfd;
    border-top-right-radius: 0.45em !important;
    margin-left: auto; margin-right:8px;
    box-shadow: 0 0 12px 2px #31ffaef5, 0 0 1px #b3affc;
}}
.assistant-bubble {{
    background: linear-gradient(88deg, #393bad 77%, #26ffe6 106%);
    color: #fff;
    border-top-left-radius: 0.5em !important;
    margin-right: auto; margin-left:8px;
    box-shadow: 0 0 11px #18ebe9, 0 0 1px #2947a7;
}}
.st-emotion-cache-13h13g7 {{
    padding: 0px !important;
}}
::-webkit-scrollbar {{width:0;height:0; background:transparent;}}

/* Suggestions buttons styling */
.suggestion-btn {{
    background: #0fffc1;
    border: none;
    border-radius: 18px;
    padding: 6px 14px;
    margin: 0 5px 10px 0;
    color: #023f44;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 0 15px #00ffdd9a;
    transition: background-color 0.3s ease;
    font-family: 'Inter', sans-serif;
}}
.suggestion-btn:hover {{
    background-color: #1affe0;
    box-shadow: 0 0 24px #00ffeecc;
}}
.suggestions-container {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 10px;
}}
.bottom-input-bar {{
    position: fixed;
    bottom: 0; left: 0; width: 100vw;
    background: rgba(17,26,49,0.89);
    z-index: 50;
    padding: 18px 0 14px 0;
    margin: 0; 
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        "<h3 style='color:#16ffe6; margin-bottom:-7px; text-shadow:0 0 8px #13fff5;'>🕓 Chat History</h3>",
        unsafe_allow_html=True
    )
    clear = st.button("🗑️ Clear History", use_container_width=True)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if clear:
        st.session_state.messages = []

    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            sender = "You" if msg["role"] == "user" else "Bot"
            bubble_color = "#1b3f93" if msg["role"] == "user" else "#19cdbb"
            st.markdown(
                f"""
                <div style='margin-bottom:8px;padding:7px 13px;
                            border-radius:12px;
                            background:linear-gradient(90deg,{bubble_color} 70%,#2a2f68 120%);
                            color:#e7fcfb;font-size:0.96rem;box-shadow: 0 0 8px #26f7ff66;'>
                    <span style='font-size:0.94em;opacity:0.67;'>{sender}:</span><br>
                    {msg['content']}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<span style='color:#9dd;opacity:0.7;'>No history yet. Start chatting!</span>",
            unsafe_allow_html=True
        )

st.markdown(
    "<div class='main-title'>AI Assistant <span style='color:#88f8da;filter:drop-shadow(0 0 12px #09ffe4)'>🤖</span></div>", 
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "input" not in st.session_state:
    st.session_state.input = ""
if "last_input" not in st.session_state:
    st.session_state.last_input = ""

suggestions = [
    "Tell me a joke", "What's the time?", "How are you?", "What's today's date?", "Help me"
]

st.markdown("<div class='suggestions-container'>", unsafe_allow_html=True)
clicked_suggestion = None
cols = st.columns(len(suggestions))
for i, sug in enumerate(suggestions):
    if cols[i].button(sug, key=f"sug_{i}"):
        clicked_suggestion = sug
st.markdown("</div>", unsafe_allow_html=True)
if clicked_suggestion:
    st.session_state.input = clicked_suggestion

st.markdown("<div style='margin-bottom:115px;'>", unsafe_allow_html=True)
for m in st.session_state.messages:
    sender = m["role"]
    bubble_cls = "user-bubble" if sender == "user" else "assistant-bubble"
    align = "right" if sender == "user" else "left"
    st.markdown(
        f"<div style='display:flex;justify-content:flex-{align};'><div class='{bubble_cls}'>{m['content']}</div></div>",
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="bottom-input-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns([10,1])
    with col1:
        input_text = st.text_input(
            "Type your message...", 
            value=st.session_state.input,
            key="chat_input_box",
            label_visibility="collapsed",
            placeholder="Type your message here..."
        )
    with col2:
        send_now = st.button("➡️", key="send_arrow", help="Send")
    st.markdown('</div>', unsafe_allow_html=True)

chatbot = Chatbot("intents.json")

send_triggered = (send_now or (input_text and input_text != st.session_state.last_input))
if send_triggered:
    msg = input_text.strip()
    if msg:
        st.session_state.last_input = msg
        st.session_state.input = ""

        st.session_state.messages.append({"role": "user", "content": msg})

        bot_placeholder = st.empty()
        sender = "assistant"
        bubble_cls = "assistant-bubble"
        align = "left"
        with bot_placeholder:
            st.markdown(
                f"<div style='display:flex;justify-content:flex-{align};'><div class='{bubble_cls}'>Bot is typing...▌</div></div>",
                unsafe_allow_html=True
            )
        time.sleep(0.6)
        bot_response = chatbot.get_response(msg) or "I'm not sure yet, but I'm learning! 🤖"
        typed_response = ""
        for char in bot_response:
            typed_response += char
            with bot_placeholder:
                st.markdown(
                    f"<div style='display:flex;justify-content:flex-left;'><div class='assistant-bubble'>{typed_response + '▌'}</div></div>",
                    unsafe_allow_html=True
                )
            time.sleep(0.012)
        with bot_placeholder:
            st.markdown(
                f"<div style='display:flex;justify-content:flex-left;'><div class='assistant-bubble'>{typed_response}</div></div>",
                unsafe_allow_html=True
            )
        st.session_state.messages.append({"role": "assistant", "content": typed_response})

st.session_state.input = input_text

st.markdown("""
    <div style="
        position:fixed; bottom:12px; right:25px; 
        font-family:'Orbitron',monospace; font-size:0.96rem;
        padding:5px 17px 4px 10px; background:rgba(38,255,242,0.13);
        color:#1ffbde;border-radius:17px;
        box-shadow:0 0 21px 5px #19fffaa8;
        border:1px solid #0fffc16b; z-index:10000;">
        ⚡ Powered by Streamlit
    </div>
""", unsafe_allow_html=True)
