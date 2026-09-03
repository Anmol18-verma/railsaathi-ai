import streamlit as st

st.set_page_config(
    page_title="RailSaathi AI",
    page_icon="🚆",
    layout="centered"
)

st.title("RailSaathi AI")
st.subheader("Personal Railway Travel Intelligence Assistant")

st.write(
    "Get quick answers about RAC, waiting lists, railway classes, "
    "PNR concepts, cancellation, luggage and passenger safety."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask RailSaathi AI...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    if "rac" in prompt.lower():
        answer = "RAC (Reservation Against Cancellation) allows a passenger to travel with a confirmed seat initially, while a berth may be allotted later if one becomes available."
    elif "waiting" in prompt.lower() or "wl" in prompt.lower():
        answer = "A waiting-list ticket means a confirmed berth or seat has not yet been allotted. Its status may change before the journey."
    elif "3a" in prompt.lower() or "third ac" in prompt.lower():
        answer = "3A (Third AC) is an air-conditioned railway class with sleeping berths arranged in tiers. It is commonly used for overnight and long-distance journeys."
    elif "luggage" in prompt.lower():
        answer = "Passengers should follow the applicable railway luggage rules and keep their belongings secure during the journey."
    elif "pnr" in prompt.lower():
        answer = "PNR stands for Passenger Name Record. It is a reference number associated with a railway reservation and its booking details."
    elif "safety" in prompt.lower():
        answer = "Keep your belongings secure, follow railway safety instructions, and use official railway services for emergency or live journey information."
    else:
        answer = "RailSaathi AI can help with RAC, waiting lists, train classes, PNR concepts, cancellation, luggage and passenger safety. For live railway information, please use official Indian Railways services."

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
