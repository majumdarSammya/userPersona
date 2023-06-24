import openai
import pandas as pd
import streamlit as st
from streamlit_chat import message
import random

# PATH = "persona.csv"
openai.api_key = "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"

personaList = []


# def getPersona(PATH):
#     personaData = pd.read_csv(PATH, sep=";", encoding='cp1252')
#     personaData.index = [x for x in range(1, len(personaData.values)+1)]

#     return personaData.iloc[random.randint(0, len(personaData.index)), :].to_json()


@st.cache_data
def generate_response(system_prompt, user_prompt):
    st.session_state['messages'] = [
        {"role": "system", "content": system_prompt}
    ]
    response = openai.ChatCompletion.create(
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ],
        model="gpt-3.5-turbo",
        max_tokens=2048,
        temperature=0.3,
    )
    reply = response.choices[0].message.content
    st.session_state['messages'].append(
        {"role": "assistant", "content": response})
    return response['choices'][0]['message']['content'].strip()


def home():
    PATH = "persona.csv"

    def getPersona(PATH, idx):
        personaData = pd.read_csv(PATH, sep=";", encoding='cp1252')
        personaData.index = [x for x in range(1, len(personaData.values)+1)]

        return personaData.iloc[idx, :].to_json()

    init_persona = getPersona(PATH, 2)

    st.title("User Persona Chat Assistant")
    st.markdown("This is the User Persona Chat Assistant. It is capable of conversations with an user as users of sky products with vastly different buying habits and needs.")
    st.markdown("This application leverages openAI GPT-3.5-Turbo model.")
    system_prompt = """

    You are a customer who uses a lot of sky media company products. You have to do the following:
    - Learn what you can from the web on sky and their product offerings.
    - Understand the customer you will impersonate. This will be provided to you at the end of this prompt.
    - Format your answer in the following way: 
            - persona you got as an input  
            - Respond as if you are the person whose persona you got at the end of this sentence.

"""
    clear_button = st.button("Refresh", key="clear")
    if clear_button:
        system_prompt = """

                            You are a customer who uses a lot of sky media company products. You have to do the following:
                            - Learn what you can from the web on sky and their product offerings.
                            - Understand the customer from the information provided at the end of this prompt.
                            - Format your answer in the following way: 
                                    - persona you got as an input  
                                    - Respond from the customer's perspective

                        """

        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['messages'] = [
            {"role": "system", "content": system_prompt+init_persona}
        ]

    text_container = st.container()
    response_container = st.container()

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "system", "content": system_prompt}
        ]

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    with text_container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You:", key='input', height=100)
            submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_response(system_prompt+init_persona, user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i],
                        is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))


def main():
    home()


if __name__ == "__main__":
    main()
