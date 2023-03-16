import os
import requests
import streamlit as st

BASE_URL = os.getenv("API_URL")

st.header("Admin Panel")

with open("styles/main.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


if st.session_state["DETAILS"] == None:
    st.warning("Make sure your logged in")
else:
    with st.spinner("Checking your access privileges and Loading content..."):
        logcheck = requests.get(
            f"{BASE_URL}/data/check/admin?username={st.session_state['DETAILS']['username']}&password={st.session_state['DETAILS']['password']}"
        )

        if logcheck.json()["admin"] == True:

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("# Manage Users")
                users = requests.get(f"{BASE_URL}/data/user")
                num = 1
                for user in users.json():
                    with st.container():
                        st.markdown(f"#### Username | {user['username'][0]}")
                        if user["admin"] == True:
                            p = st.button("Remove Admin", key=f"p{num}")
                            if p:
                                pu = requests.patch(
                                    f"{BASE_URL}/data/update/user?value=admin&state=False&id={user['id']}"
                                )
                                st.success("Admin demoted to user")
                        if user["admin"] == False:
                            m = st.button("Make Admin", key=f"m{num}")
                            if m:
                                pu = requests.patch(
                                    f"{BASE_URL}/data/update/user?value=admin&state=True&id={user['id']}"
                                )
                                st.success("User promoted to admin")
                        if user["banned"] == True:
                            u = st.button("Unban User", key=f"u{num}")
                            if u:
                                pu = requests.patch(
                                    f"{BASE_URL}/data/update/user?value=banned&state=False&id={user['id']}"
                                )
                                st.success("User unbanned")
                        if user["banned"] == False:
                            b = st.button("Ban User", key=f"b{num}")
                            if b:
                                pu = requests.patch(
                                    f"{BASE_URL}/data/update/user?value=banned&state=True&id={user['id']}"
                                )
                                st.success("User banned")
                    num += 1
            with c2:
                st.markdown("# Manage reports")
                reports = requests.get(f"{BASE_URL}/data/wall")
                num = 1
                for report in reports.json():
                    if report["reported"] == True:
                        with st.container():
                            st.markdown(f"#### Post | {report['title'][0]}")
                            st.markdown(f"###### User | {report['info']['user']}")
                            r = st.button("Delete post", key=f"r{num}")
                            if r:
                                pu = requests.delete(
                                    f"{BASE_URL}/data/delete/wall?id={report['key']}"
                                )
                                st.success("Post deleted")
                    num += 1

        else:
            st.error("You don't have admin privileges")
