import streamlit as st
st.set_page_config(page_title = "Text input Demo", page_icon="🐶")

st.markdown("""
<style>
.stApp{
background-color : #87CEEB;
}
</style>
""", unsafe_allow_html=True)
st.title("Text input Demo")
name = st.text_input("Enter your name:",placeholder="Type your name here...")
st.write(f"Hello, {name}!")
secret = st.text_input("Enter your password",placeholder="Type your password here...",type="password")
st.write(f"Your password has {len(secret)} characters.")
comments = st.text_area("Any additional comments?",placeholder="Type your comments here...", height = 150)
st.write(f"Your written {len(comments)} characters.")
if st.button("Submit"):
    st.write("You clicked on Submit!")
show_message = st.checkbox("Do you want an extra message?")
if show_message:
    st.write("This is an extra message. Have a good day!.")