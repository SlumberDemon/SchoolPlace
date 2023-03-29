import requests
import streamlit as st

st.session_state["LOGGEDIN"] = None
st.session_state["DETAILS"] = None

with open("styles/main.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.header(f"Welcome to SchoolPlace")
if st.session_state["LOGGEDIN"] == None:
    st.write("Login or Sign Up to get started!")
    (
        l1,
        l2,
    ) = st.columns(2)
    with l1:
        st.header("Login")
        USENAME = st.text_input("Username")
        pascode = st.text_input("Password")

        if pascode and USENAME:
            with st.spinner("Logging in..."):
                logcheck = requests.get(
                    f"https://school.deta.dev/data/check/user?username={USENAME}&password={pascode}"
                )
                st.session_state["LOGGEDIN"] = logcheck.json()["user"]
                st.session_state["DETAILS"] = {
                    "username": USENAME,
                    "password": pascode,
                    "banned": logcheck.json()["banned"],
                }
                if st.session_state["DETAILS"]["banned"] == False:
                    if st.session_state["LOGGEDIN"] == True:
                        st.success("Logged in!")
                    else:
                        st.error("Unable to login, make sure your details are correct!")
                elif st.session_state["DETAILS"]["banned"] == True:
                    st.session_state["LOGGEDIN"] = False
                    st.warning(
                        "Your account has been banned for violating School Place's rules"
                    )
        else:
            st.session_state["LOGGEDIN"] = None
    with l2:
        st.header("Create Account")
        pas = st.text_input("Password (Required)")
        em = st.text_input("Email (Optional)")
        if pas:
            if len(pas) >= 8:
                siup = st.button("Sign Up", key="signup")
                em = None if not em else em
                if siup:
                    with st.spinner("Creating account..."):
                        uname = requests.get("https://apis.kahoot.it")
                        usa = requests.post(
                            f"https://school.deta.dev/data/create/user?username={uname.json()['name']}&password={pas}&email={em}"
                        )
                        st.success("Acount created!")
                        with st.container():
                            st.write("__Your Login Details__")
                            st.write(f"`Username:` {usa.json()['username'][0]}")
                            if em != None:
                                st.write(f"`Email:` {usa.json()['email'][0]}")
                            st.write(f"`Password:` {usa.json()['password'][0]}")
            else:
                st.error("Password to short, please use at least 8 characters!")
