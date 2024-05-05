import sqlite3
import streamlit as st
import time
import pandas as pd
conn = sqlite3.connect('data.db')
cursor = conn.cursor()



def read_movies():
    cursor.execute("""
            SELECT *
            FROM Questions
            WHERE isSelected = 0
            ORDER BY ID ASC
            LIMIT 1
            """ )
    return cursor.fetchone()

with st.sidebar:
    st.header("Navigation Menu")
    menu_selection = st.radio("Select a page:", ("Home", "Knowledge Base"))


if menu_selection == "Knowledge Base":
    # Create a form
    st.title("Add Data to Knowledge Base")
    with st.form(key="my_form"):
        # Text inputs with labels
        Question = st.text_input(label="Question:")
        Answer = st.text_input(label="Answer:")
        Right = st.text_input(label="Right Answer:")
        Conclusion = st.text_input(label="Conclusion:")

        # Submit button
        submitted = st.form_submit_button(label="Submit")

    # Process form submission
    if submitted:
        st.write("**Submitted values:**")
        Questions = [
            (Question,Answer,Right,Conclusion,0),
        ]
        cursor.executemany("""INSERT INTO Questions (Question,Answers,RightAnswers,Conclusion,isSelected) 
                           VALUES  (?, ?, ?, ?, ?)""", Questions)

        conn.commit()
    cursor.execute("SELECT * FROM Questions")

    # Fetch all rows and column names
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # Create a pandas DataFrame
    df = pd.DataFrame(data, columns=columns)
    df

if menu_selection == "Home":

    st.title("pharmaceutical inventory management consultant")
    st.subheader("type 'reset' to relode")
    messages = st.container(height=500)
    data = read_movies()

    if 'my_list' not in st.session_state:
        st.session_state['my_list'] = []
    for item in st.session_state['my_list']:
        messages.chat_message("assistant").write(f"Echo: {item}")
    if data:

        messages.chat_message("assistant").write(f"Echo: {str(data[1])}  {str(data[2])}")

    else :
        Conclusion = cursor.execute("SELECT * FROM AnswersX").fetchall()
        if Conclusion:
            
            messages.chat_message("assistant").write(f"Echo: Conclusion :")
            for items in Conclusion:
                messages.chat_message("assistant").write(f"Echo: {items[0]}.")
        else:
            messages.chat_message("assistant").write(f"Echo: can not get answer or tell you advise.")


    user_input = st.text_input("Say something")
    submit_button = st.button("Submit")

    if submit_button :  # Button clicked
        if  user_input in "reset":
            cursor.execute("""
                UPDATE Questions
                SET isSelected = 0
            
                """)
            cursor.execute("DELETE FROM AnswersX")
            # Commit the changes to the database
            conn.commit()
            st.session_state.clear()
            progress_bar = st.progress(0)
            for i in range(50):
                progress_bar.progress(i)
                time.sleep(0.01) 
            st.experimental_rerun()
        elif user_input not in str(data[2]):
            
            messages.chat_message("assistant").write(f"Sorry, that's not quite right. Try again. The answer should be related to: {str(data[1])}")

        else:
            messages.chat_message("user").write(user_input)
            st.session_state['my_list'].append(f"{str(data[1])} -> {user_input}")
            # Get further user input after answering correctly

            cursor.execute("""
                UPDATE Questions
                SET isSelected = 1
                WHERE ID = ?
                """, (data[0],))

            # Commit the changes to the database
            conn.commit()

            if user_input in data[3] :
                sql = "INSERT INTO AnswersX (Answers) VALUES (?)"
                cursor.execute(sql, (data[4],))
                conn.commit()

            next_prompt = st.text("Inference")
            progress_bar = st.progress(0)
            for i in range(50):
                progress_bar.progress(i)
                time.sleep(0.01) 
            st.experimental_rerun()
        