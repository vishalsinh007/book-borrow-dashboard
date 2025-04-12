import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# File to store data
DATA_FILE = "student_data.csv"

# Load existing data or initialize
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Roll No", "Department", "Book Name", "Issue Date", "Return Date"])

# Save data to CSV
def save_data():
    df = pd.DataFrame(st.session_state.students)
    df.to_csv(DATA_FILE, index=False)

# Initialize student list
if "students" not in st.session_state:
    st.session_state.students = load_data().to_dict("records")

# Title
st.title("📚 Book Borrow Dashboard")

# Form to add student
with st.form("student_form"):
    st.subheader("Add Student")
    name = st.text_input("Name")
    roll = st.text_input("Roll No")
    dept = st.text_input("Department")
    book = st.text_input("Book Name")
    days = st.number_input("No. of Days to Borrow", min_value=1, max_value=30, value=7)
    submitted = st.form_submit_button("Add Student")

    if submitted:
        issue_date = datetime.now().date()
        return_date = issue_date + timedelta(days=int(days))
        st.session_state.students.append({
            "Name": name,
            "Roll No": roll,
            "Department": dept,
            "Book Name": book,
            "Issue Date": issue_date,
            "Return Date": return_date
        })
        save_data()
        st.success(f"{name} added successfully!")

# Show student list sorted by remaining days
st.subheader("📋 Borrowed Students")
today = datetime.now().date()
sorted_students = sorted(st.session_state.students, key=lambda x: (datetime.strptime(str(x["Return Date"]), "%Y-%m-%d").date() - today).days)

for student in sorted_students:
    with st.expander(f"{student['Name']} ({student['Roll No']})"):
        st.write(f"📘 **Book Name**: {student['Book Name']}")
        st.write(f"🏫 **Department**: {student['Department']}")
        st.write(f"📅 **Issue Date**: {student['Issue Date']}")
        st.write(f"📆 **Return Date**: {student['Return Date']}")

        # Calculate days left
        return_date = datetime.strptime(str(student["Return Date"]), "%Y-%m-%d").date()
        days_left = (return_date - today).days
        if days_left >= 0:
            st.info(f"⏳ **Days Left**: {days_left} days")
        else:
            st.error(f"⚠️ Overdue by {-days_left} days")

        # Extend + Remove in same row
        extend = st.number_input("Extend Borrow Days", min_value=1, max_value=30, value=3, key=f"extend_{student['Roll No']}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Extend", key=f"extend_btn_{student['Roll No']}"):
                student["Return Date"] = (datetime.strptime(str(student["Return Date"]), "%Y-%m-%d") + timedelta(days=int(extend))).date()
                save_data()
                st.success("Return date extended!")
                st.rerun()


        with col2:
            if st.button("❌ Remove Student", key=f"remove_btn_{student['Roll No']}"):
                st.session_state.students = [s for s in st.session_state.students if not (s["Name"] == student["Name"] and s["Roll No"] == student["Roll No"])]
                save_data()
                st.success(f"{student['Name']} removed successfully!")
                st.rerun()

