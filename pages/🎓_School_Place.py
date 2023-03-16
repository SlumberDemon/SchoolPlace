import os
import random
import textwrap
import requests
import datetime
import streamlit as st
from urllib.request import urlopen
from PIL import Image, ImageDraw, ImageFont
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

BASE_URL = "https://school.deta.dev/"


st.set_page_config(page_title="SchoolPlace", page_icon=f"{BASE_URL}/cdn/hat.ico")

with open("styles/main.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

with st.sidebar:
    navbar = option_menu(
        menu_title=None,
        options=["Home", "Wall", "Posts", "Create Post"],
        icons=["house", "list", "list-task", "pencil"],
    )


class smol_font:
    title = ImageFont.truetype("extras/font.otf", 36)
    user = ImageFont.truetype("extras/font.otf", 25)
    time = ImageFont.truetype("extras/font.otf", 15)


class big_font:
    title = ImageFont.truetype("extras/font.otf", 45)
    user = ImageFont.truetype("extras/font.otf", 40)
    tags = ImageFont.truetype("extras/font.otf", 20)
    time = ImageFont.truetype("extras/font.otf", 25)
    content = ImageFont.truetype("extras/font.otf", 35)


if st.session_state["LOGGEDIN"] == True:
    if navbar == "Home":
        st.header(f"Welcome {st.session_state['DETAILS']['username']}")
        with st.spinner(
            "Please wait! SchoolPlace is Loading an animal image and facts..."
        ):
            try:
                animals = [
                    "Panda",
                    "Dog",
                    "Cat",
                    "Fox",
                    "Red_Panda",
                    "Koala",
                    "Birb",
                    "Raccoon",
                    "Kangaroo",
                    "Pikachu",
                ]
                adata = requests.get(
                    f"https://some-random-api.ml/animal/{random.choice(animals)}"
                )
                ajson = adata.json()
                image = Image.open(urlopen(ajson["image"]))
                st.image(image, caption=f"Did you know: {ajson['fact']}")
            except:
                img = Image.open(urlopen("https://httpcats.com/404.jpg"))
                st.image(img)

    elif navbar == "Wall":
        st.header("Welcome to Wall")
        st.write("Receive help or help others")
        st.write("ㅤㅤㅤ\nㅤㅤㅤ")
        with st.spinner("Loading..."):
            by = requests.get(f"{BASE_URL}/data/wall")
            data = by.json()
            count = 1
            img = 1
            for i in data:
                with st.container():
                    im = Image.open(urlopen(f"{BASE_URL}/cdn/wall_smol.png"))
                    d = ImageDraw.Draw(im)
                    d.text((20, 20), f"{i['title'][0]}", "black", smol_font.title)
                    d.text((20, 65), f"{i['info']['user']}", "grey", smol_font.user)
                    d.text((20, 95), f"{i['tags'][0]}", "grey", big_font.tags)
                    d.text((20, 150), f"{i['info']['time']}", "grey", smol_font.time)
                    st.image(im)
                    i1, i2 = st.columns(2)
                    with i1:
                        wall = st.button(
                            "ㅤㅤㅤㅤㅤㅤㅤㅤView Wall Postㅤㅤㅤㅤㅤㅤㅤㅤ", key=f"img{img}"
                        )
                    if wall:
                        with st.container():
                            im = Image.open(urlopen(f"{BASE_URL}/cdn/wall_big.png"))
                            d = ImageDraw.Draw(im)
                            d.text(
                                (20, 30), f"{i['title'][0]}", "black", big_font.title
                            )
                            d.text(
                                (20, 80), f"{i['info']['user']}", "grey", big_font.user
                            )
                            d.text(
                                (20, 135),
                                textwrap.fill(f"{i['content'][0]}", width=40),
                                "black",
                                big_font.content,
                            )
                            d.text(
                                (20, 800),
                                f"{i['info']['time']}",
                                "grey",
                                big_font.time,
                            )
                            st.image(im)
                            with st.spinner("Loading comments..."):
                                HtmlFile = open("html/wall.html", "r", encoding="utf-8")
                                source_code = HtmlFile.read()
                                components.html(source_code, height=600)
                            close = st.button("ㅤㅤㅤㅤㅤㅤCloseㅤㅤㅤㅤㅤㅤ", key="close")
                    with i2:
                        report = st.button("Report Wall Post", key=f"report{img}")
                        if report:
                            try:
                                ro = requests.patch(
                                    f"{BASE_URL}/data/update/wall?value=reported&state=True&id={i['key']}"
                                )
                                ro.close()
                                st.success("Reported")
                            except:
                                st.error("Unable to report wall post")
                img += 1
                if count == 3:
                    count = 0
                else:
                    count += 1
            by.close()

    elif navbar == "Posts":
        st.header("Welcome to Posts")
        with st.spinner("Loading..."):
            HtmlFile = open("html/posts.html", "r", encoding="utf-8")
            source_code = HtmlFile.read()
            components.html(source_code, height=800)

    elif navbar == "Create Post":
        st.header("Create Wall Post")
        title = st.text_input(
            "Subject",
            max_chars=20,
        )
        tags = st.multiselect(
            "Topic Tags",
            ["#Homework", "#Revision", "#Study", "#Help", "#Other"],
        )
        content = st.text_area("Description", max_chars=850, height=250)
        submit = st.button("Submit", key="submit")
        if submit:
            date = datetime.datetime.utcnow()
            try:
                ti = date.strftime("%x | %X")
                ta = ", ".join(str(x).replace("#", "") for x in tags)
                r = requests.post(
                    f"{BASE_URL}/data/create/wall?title={title}&content={content}&user={st.session_state['DETAILS']['username']}&time={ti}&tags={ta}"
                )
                st.success(f"Posted!")
            except:
                st.warning("Unable to Post")
elif st.session_state["LOGGEDIN"] == False:
    st.error("Incorrect Login! Please try again!")
elif st.session_state["LOGGEDIN"] == None:
    st.warning("To Access this page you need to login!")


# Welcome to School Place! Make sure to use common sense! We hope you enjoy your stay!
