import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="📚 Book Borrow Dashboard", layout="centered")

DATA_FILE = "borrow_data.csv"

# 🔁 Load saved data
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=["Borrow Date", "Return Date"])
        return df.to_dict(orient="records")
    return []

# 💾 Save data to CSV
def save_data():
    df = pd.DataFrame(st.session_state.students)
    df.to_csv(DATA_FILE, index=False)

# ➕ Add new student
def add_student(name, roll, dept, book, days):
    borrow_date = datetime.now()
    return_date = borrow_date + timedelta(days=days)
    st.session_state.students.append({
        "Name": name,
        "Roll No": roll,
        "Department": dept,
        "Book": book,
        "Borrow Date": borrow_date,
        "Return Date": return_date
    })

# 🔄 Initialize session state
if "students" not in st.session_state:
    st.session_state.students = load_data()

# 📋 Sidebar - Add new entry
with st.sidebar:
    st.header("📌 Add New Borrow Entry")
    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")
    dept = st.text_input("Department")
    book = st.text_input("Issued Book")
    days = st.number_input("Borrow Days", min_value=1, max_value=30, value=7)

    if st.button("Add Student"):
        if name and roll and dept and book:
            add_student(name, roll, dept, book, days)
            save_data()
            st.success(f"{name} added successfully!")
        else:
            st.warning("Please fill all fields.")

# 🏠 Main - Student List
st.title("📚 Book Borrow Dashboard")
df = pd.DataFrame(st.session_state.students)

if not df.empty:
    df["Days Left"] = df["Return Date"].apply(lambda d: (d - datetime.now()).days)
    df = df.sort_values("Days Left")

    selected = st.selectbox("📌 Select Student", df["Name"])
    student = next((s for s in st.session_state.students if s["Name"] == selected), None)

    if student:
        st.subheader(f"📖 Details for {student['Name']}")
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

        extend = st.number_input("Extend Borrow Days", min_value=1, max_value=30, value=3)
        if st.button("Extend"):
            student["Return Date"] += timedelta(days=extend)
            save_data()
            st.success("Return date extended!")

else:
    st.info("No students added yet. Use the sidebar to start.")


