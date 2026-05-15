import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data['student_id']


    res = supabase.table('subjects').select('subject_id, name').eq('subject_code', subject_code).execute()
    if not res.data:
        st.error('Subject Code not found!')
        if st.button('Close', key='auto_enroll_close_btn'):
            st.query_params.clear()
            st.rerun()
        return
    subject = res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
    if check.data:
        st.info('Youre already enrolled!')
        if st.button('Got it!', key='auto_enroll_got_it_btn'):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f"Would you like to enroll in **{subject['name']}**?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks', key='auto_enroll_no_btn'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button('Yes enroll now!', type='primary', width='stretch', key='auto_enroll_yes_btn'):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success('Joined succesfully!')
            st.query_params.clear()
            time.sleep(2)
            st.rerun()

