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

    # Optional minimal CSS for center layout
    css = """
    <style>
    h1 {
      text-align: center;
    }
    section.main div.block-container {
      max-width: 700px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    st.title("Student Influencer Survey")
    st.write(
        "We are identifying students with active social media presence to collaborate "
        "with us for influencer and campus ambassador opportunities."
    )

    with st.form("survey_form", clear_on_submit=True):
        # Basic info
        full_name = st.text_input("Full Name*")
        city = st.text_input("City*")
        program_year = st.text_input("Program and Year*")
        phone = st.text_input("Phone number")

        # Age
        age = st.number_input("Age*", min_value=13, max_value=80, step=1)

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
            "Type of content you mainly create* "
            "(e.g., exam prep, coding tutorials, campus vlogs)"
        )

        st.markdown("### Social media platforms")

        st.write(
            "Select the platforms where you actively create content and enter "
            "your handles/URLs."
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
                "Instagram handle / profile URL", key="insta_handle"
            )
            youtube_handle = st.text_input(
                "YouTube channel URL", key="yt_handle"
            )
            linkedin_handle = st.text_input(
                "LinkedIn profile URL", key="li_handle"
            )
            twitter_handle = st.text_input(
                "Twitter / X handle / URL", key="tw_handle"
            )
            facebook_handle = st.text_input(
                "Facebook profile/page URL", key="fb_handle"
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
            if not city:
                errors.append("City is required.")
            if not program_year:
                errors.append("Program and Year is required.")
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
                        city,
                        program_year,
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
