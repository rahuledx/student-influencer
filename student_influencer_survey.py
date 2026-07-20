import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_worksheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gsheets"], scope
    )
    client = gspread.authorize(creds)
    sh = client.open_by_url(st.secrets["gsheets"]["spreadsheet_url"])
    return sh.sheet1


def main():
    st.set_page_config(
        page_title="Student Influencer Survey",
        page_icon="🎯",
        layout="centered"
    )

    st.markdown(
        """
        <style>
        h1 {
            text-align: center;
            margin-top: 0.2rem;
        }
        section.main div.block-container {
            max-width: 760px;
            padding-top: 0.8rem;
        }
        .logo-container {
            text-align: center;
            margin-bottom: 2px;
        }
        .logo-container img {
            width: 100%;
            max-width: 1000px;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    logo_url = "https://admin.onlineamrita.com/sites/default/files/2025-04/Amrita%20Online%20Logo%20red%201.svg"
    st.markdown(
        f"""
        <div class="logo-container">
            <img src="{logo_url}" alt="Amrita Online Logo">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("Student Influencer Survey")
    st.write(
        "We are identifying students with active social media presence at Amrita Online "
        "to collaborate with us for influencer collaboration opportunities."
    )

    full_name = st.text_input("Full Name*", placeholder="Enter your full name")
    email = st.text_input("Email*", placeholder="Enter your email address")
    city = st.text_input("City*", placeholder="Enter your city")

    program = st.selectbox(
        "Program*",
        ["", "Online MBA", "Online MCA", "Online MCom", "Online BCom", "Online BBA", "Online BCA"]
    )

    semester = st.selectbox(
        "Semester*",
        ["", "Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5", "Semester 6"]
    )

    phone = st.text_input("Phone number", placeholder="Enter your phone number")
    age = st.number_input("Age*", min_value=21, max_value=80, step=1, value=21)

    language = st.selectbox(
        "Primary language of your content*",
        ["", "English", "Hindi", "Malayalam", "Tamil", "Kannada", "Telugu", "Other"]
    )

    content_type = st.text_input(
        "Type of content you mainly create*",
        placeholder="e.g., exam prep, coding tutorials, campus vlogs"
    )

    st.markdown("### Social media platforms")
    st.write(
        "Select the platforms where you actively create content and enter your profile links."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        instagram_active = st.checkbox("Instagram")
        youtube_active = st.checkbox("YouTube")
        linkedin_active = st.checkbox("LinkedIn")
        twitter_active = st.checkbox("Twitter / X")
        facebook_active = st.checkbox("Facebook")

    with col2:
        instagram_link = st.text_input(
            "Instagram profile link",
            placeholder="https://instagram.com/username"
        )
        youtube_link = st.text_input(
            "YouTube profile link",
            placeholder="https://youtube.com/@channel"
        )
        linkedin_link = st.text_input(
            "LinkedIn profile link",
            placeholder="https://linkedin.com/in/username"
        )
        twitter_link = st.text_input(
            "Twitter / X profile link",
            placeholder="https://twitter.com/username"
        )
        facebook_link = st.text_input(
            "Facebook profile link",
            placeholder="https://facebook.com/username"
        )

    st.markdown("### Approximate follower count across all platforms*")
    follower_band = st.radio(
        "Select the range that best represents your total follower/subscriber count:",
        ["0-1000", "1,001–5,000", "5,001–20,000", "20,001–50,000", "50,000+"]
    )

    submit = st.button("Submit")

    if submit:
        platforms = []
        if instagram_active:
            platforms.append("Instagram")
        if youtube_active:
            platforms.append("YouTube")
        if linkedin_active:
            platforms.append("LinkedIn")
        if twitter_active:
            platforms.append("Twitter / X")
        if facebook_active:
            platforms.append("Facebook")

        errors = []
        if not full_name:
            errors.append("Full Name is required.")
        if not email:
            errors.append("Email is required.")
        if not city:
            errors.append("City is required.")
        if not program:
            errors.append("Program is required.")
        if not semester:
            errors.append("Semester is required.")
        if not language:
            errors.append("Language is required.")
        if not content_type:
            errors.append("Type of content is required.")
        if not platforms:
            errors.append("At least one social media platform must be selected.")
        if not follower_band:
            errors.append("Follower count range is required.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            try:
                worksheet = get_worksheet()
                timestamp = datetime.utcnow().isoformat()

                row = [
                    timestamp,
                    full_name,
                    email,
                    city,
                    program,
                    semester,
                    phone if phone else "",
                    int(age),
                    language,
                    content_type,
                    ", ".join(platforms),
                    instagram_link,
                    youtube_link,
                    linkedin_link,
                    twitter_link,
                    facebook_link,
                    follower_band
                ]

                worksheet.append_row(row)
                st.success("Thank you for submitting the survey!")
                st.balloons()
            except Exception as e:
                st.error(f"Error saving response: {e}")


if __name__ == "__main__":
    main()
