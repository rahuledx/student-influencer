import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_worksheet():
    # st.secrets["gsheets"] must contain the service account JSON fields
    # plus spreadsheet_url
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gsheets"], scope
    )
    client = gspread.authorize(creds)

    # spreadsheet_url stored in secrets
    sh = client.open_by_url(st.secrets["gsheets"]["spreadsheet_url"])
    # Use first sheet or change to .worksheet("Sheet1")
    worksheet = sh.sheet1
    return worksheet


def main():
    st.set_page_config(
        page_title="Student Influencer Survey",
        page_icon="🎯",
        layout="centered"
    )

    # Optional minimal CSS for center layout and hide helper text
    css = """
    <style>
    h1 {
      text-align: center;
    }
    section.main div.block-container {
      max-width: 700px;
    }
    .logo-container {
      text-align: center;
      margin-bottom: 20px;
    }
    .logo-container img {
      max-width: 350px;
      height: auto;
    }
    /* Hide the "press enter to submit" helper text */
    div.stTextInput p, div.stNumberInput p {
      display: none;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Add logo at the top
    logo_url = "https://admin.onlineamrita.com/sites/default/files/2025-04/Amrita%20Online%20Logo%20red%201.svg"
    st.markdown(f"""
    <div class="logo-container">
        <img src="{logo_url}" alt="Amrita Online Logo">
    </div>
    """, unsafe_allow_html=True)

    st.title("Student Influencer Survey")
    st.write(
        "We are identifying students with active social media presence to collaborate "
        "with us for influencer and campus ambassador opportunities."
    )

    with st.form("survey_form", clear_on_submit=True):
        # Basic info
        full_name = st.text_input("Full Name*", placeholder="Enter your full name")
        email = st.text_input("Email*", placeholder="Enter your email address")
        city = st.text_input("City*", placeholder="Enter your city")
        
        # Program dropdown
        program = st.selectbox(
            "Program*",
            options=[
                "Online MBA",
                "Online MCA",
                "Online MCom",
                "Online BCom",
                "Online BBA",
                "Online BCA"
            ]
        )
        
        # Semester dropdown - only till Semester 6
        semester = st.selectbox(
            "Semester*",
            options=[
                "Semester 1",
                "Semester 2",
                "Semester 3",
                "Semester 4",
                "Semester 5",
                "Semester 6"
            ]
        )
        
        phone = st.text_input("Phone number", placeholder="Enter your phone number")

        # Age - starts at 21
        age = st.number_input("Age*", min_value=21, max_value=80, step=1, value=21)

        # Language of content
        language = st.selectbox(
            "Primary language of your content*",
            options=[
                "English",
                "Hindi",
                "Malayalam",
                "Tamil",
                "Kannada",
                "Telugu",
                "Other"
            ]
        )

        # Type of content
        content_type = st.text_input(
            "Type of content you mainly create*",
            placeholder="e.g., exam prep, coding tutorials, campus vlogs"
        )

        st.markdown("### Social media platforms")

        st.write(
            "Select the platforms where you actively create content and enter "
            "your profile links."
        )

        col1, col2 = st.columns([1, 2])

        with col1:
            instagram_active = st.checkbox("Instagram")
            youtube_active = st.checkbox("YouTube")
            linkedin_active = st.checkbox("LinkedIn")
            twitter_active = st.checkbox("Twitter / X")
            facebook_active = st.checkbox("Facebook")

        with col2:
            instagram_handle = st.text_input(
                "Instagram profile link", key="insta_handle", placeholder="https://instagram.com/username"
            )
            youtube_handle = st.text_input(
                "YouTube profile link", key="yt_handle", placeholder="https://youtube.com/@channel"
            )
            linkedin_handle = st.text_input(
                "LinkedIn profile link", key="li_handle", placeholder="https://linkedin.com/in/username"
            )
            twitter_handle = st.text_input(
                "Twitter / X profile link", key="tw_handle", placeholder="https://twitter.com/username"
            )
            facebook_handle = st.text_input(
                "Facebook profile link", key="fb_handle", placeholder="https://facebook.com/username"
            )

        st.markdown("### Approximate follower count across all platforms*")

        follower_band = st.radio(
            "Select the range that best represents your total "
            "follower/subscriber count:",
            options=[
                "0-1000",
                "1,001–5,000",
                "5,001–20,000",
                "20,001–50,000",
                "50,000+"
            ]
        )

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Collect platforms list based on checkboxes
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

            # Simple validation
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
            if age is None:
                errors.append("Age is required.")
            if not language:
                errors.append("Language of content is required.")
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
                    platforms_str = ",".join(platforms)

                    # Row order must match your sheet header row
                    row = [
                        timestamp,
                        full_name,
                        email,
                        city,
                        program,
                        semester,
                        str(phone) if phone else "",
                        int(age),
                        language,
                        content_type,
                        platforms_str,
                        instagram_handle,
                        youtube_handle,
                        linkedin_handle,
                        twitter_handle,
                        facebook_handle,
                        follower_band
                    ]

                    worksheet.append_row(row)
                    st.success("Thank you for submitting the survey!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error saving response: {e}")


if __name__ == "__main__":
    main()
