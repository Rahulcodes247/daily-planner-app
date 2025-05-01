import streamlit as st
from extra_streamlit_components import CookieManager
import httpx
from urllib.parse import urlencode
from services import add_user

# Initialize cookie manager
cookie_manager = CookieManager()

# Google OAuth config
# client_id = st.secrets["google"]["client_id"]
GOOGLE_CLIENT_ID = st.secrets["google"]["client_id"]
GOOGLE_CLIENT_SECRET = st.secrets["google"]["client_secret"]
REDIRECT_URI = "http://localhost:8501"  # Your Streamlit URL

def get_login_url():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

def get_token(code):
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    try:
        response = httpx.post("https://oauth2.googleapis.com/token", data=data)
        token_data = response.json()

        if 'error' in token_data:
            st.error(f"Token error: {token_data['error']}")
            return None

        if 'access_token' not in token_data:
            st.error("No access token in response")
            st.json(token_data)  # Show full response for debugging
            return None

        return token_data
    except Exception as e:
        st.error(f"Token request failed: {str(e)}")
        return None

def get_user_info(access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = httpx.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)
        return response.json()
    except Exception as e:
        st.error(f"User info request failed: {str(e)}")
        return None

# def main():
#     st.title("Google SSO with Streamlit")

#     query_params = st.query_params
#     if 'code' in query_params:
#         token = get_token(query_params['code'])
#         print(f"{token = }")
#         if token:
#             user_info = get_user_info(token['access_token'])
#             st.session_state.user = user_info
#             st.experimental_set_query_params()

#     if 'user' not in st.session_state:
#         st.markdown(f'<a href="{get_login_url()}">Login with Google</a>', unsafe_allow_html=True)
#     else:
#         st.write(f"Welcome {st.session_state.user['name']}!")
#         st.image(st.session_state.user['picture'])

#         if st.button("Logout"):
#             del st.session_state.user
# def main():
#     st.title("Google SSO with Streamlit")
#     print(f"{st.session_state = }")

#     # Initialize session state if not present
#     if 'auth_processed' not in st.session_state:
#         st.session_state.auth_processed = False

#     query_params = st.query_params

#     # Process auth code only if we haven't already
#     if 'code' in query_params and not st.session_state.auth_processed:
#         st.session_state.auth_processed = True  # Mark as processed

#         token = get_token(query_params['code'])

#         if token and 'access_token' in token:
#             user_info = get_user_info(token['access_token'])
#             print(f"{user_info = }")
#             if user_info:
#                 st.session_state.user = user_info
#                 print(f"{st.session_state = }")
#                 st.experimental_set_query_params()  # Clear the URL
#                 st.rerun()  # Trigger a controlled rerun
#             else:
#                 st.error("Failed to get user info")
#         else:
#             st.error("Authentication failed")

#     # Display appropriate UI based on auth state
#     if 'user' not in st.session_state:
#         print("with in if")
#         st.markdown(f'<a href="{get_login_url()}" target="_self">Login with Google</a>',
#                    unsafe_allow_html=True)
#     else:
#         print("with in else")
#         st.write(f"Welcome {st.session_state.user.get('name', 'User')}!")
#         if 'picture' in st.session_state.user:
#             st.image(st.session_state.user['picture'])
#         if st.button("Logout"):
#             del st.session_state.user
#             del st.session_state.auth_processed
#             st.rerun()

def main():
    print("main file execution")
    st.title("Google SSO with Streamlit")

    if st.button("Add User"):
        add_user()

    # Initialize critical session state variables
    if 'auth_in_progress' not in st.session_state:
        st.session_state.auth_in_progress = False
    if 'user' not in st.session_state:
        st.session_state.user = None

    query_params = st.query_params

    # Process auth code only if all conditions are met
    if ('code' in query_params and
        not st.session_state.auth_in_progress and
        st.session_state.user is None):

        st.session_state.auth_in_progress = True
        token = get_token(query_params['code'])

        if token and 'access_token' in token:
            user_info = get_user_info(token['access_token'])
            if user_info:
                st.session_state.user = user_info
                # Clear URL parameters without causing a rerun
                st.experimental_set_query_params()
                st.session_state.auth_in_progress = False
                st.rerun()  # Controlled refresh to update UI
            else:
                st.session_state.auth_in_progress = False
        else:
            st.session_state.auth_in_progress = False

    # Display appropriate UI
    if st.session_state.user:
        st.write(f"Welcome {st.session_state.user.get('name', 'User')}!")
        if 'picture' in st.session_state.user:
            st.image(st.session_state.user['picture'])
        if st.button("Logout"):
            st.session_state.clear()  # Clear all session state
            st.rerun()
    else:
        st.markdown(
            f'<a href="{get_login_url()}" target="_self">Login with Google</a>',
            unsafe_allow_html=True
        )
if __name__ == "__main__":
    main()