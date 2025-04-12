import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize session state for storing student data
if "students" not in st.session_state:
    st.session_state.students = []

# Helper to add a student
def add_student(name, roll, dept, book, borrow_days):
    borrow_date = datetime.now()
    return_date = borrow_date + timedelta(days=borrow_days)
    st.session_state.students.append({
        "Name": name,
        "Roll No": roll,
        "Department": dept,
        "Book": book,
        "Borrow Date": borrow_date,
        "Return Date": return_date
    })

# Sidebar - Add student
st.sidebar.header("📚 Add Borrower")
with st.sidebar.form("add_student_form"):
    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")
    dept = st.text_input("Department")
    book = st.text_input("Issued Book Name")
    days = st.number_input("Borrow Days", min_value=1, max_value=60, value=7)
    submitted = st.form_submit_button("Add")
    if submitted and all([name, roll, dept, book]):
        add_student(name, roll, dept, book, days)
        st.success(f"{name} added successfully!")

# Home - Student List
st.title("📘 Book Stall Borrow Dashboard")
st.write("Click on a student to view or manage details:")

# Convert session data to DataFrame
df = pd.DataFrame(st.session_state.students)

# Add a column to calculate days left
if not df.empty:
    df["Days Left"] = df["Return Date"].apply(lambda d: (d - datetime.now()).days)
    df = df.sort_values("Days Left")  # Sort by return deadline

    # Select student from sorted list
    selected = st.selectbox("Select Student", df["Name"])
    student = next((s for s in st.session_state.students if s["Name"] == selected), None)

    if student:
        st.subheader(f"Details for {student['Name']}")
        st.write(f"**Roll No:** {student['Roll No']}")
        st.write(f"**Department:** {student['Department']}")
        st.write(f"**Issued Book:** {student['Book']}")
        st.write(f"**Borrow Date:** {student['Borrow Date'].strftime('%Y-%m-%d')}")
        st.write(f"**Return Date:** {student['Return Date'].strftime('%Y-%m-%d')}")

        remaining = (student["Return Date"] - datetime.now()).days
        if remaining < 0:
            st.error("⏰ Return date passed!")
        else:
            st.info(f"📅 Days left: {remaining} day(s)")

        # Extend date option
        extend = st.number_input("Extend Borrow Days", min_value=1, max_value=30, value=3)
        if st.button("Extend"):
            student["Return Date"] += timedelta(days=extend)
            st.success("Return date extended!")
else:
    st.info("No students added yet.")

