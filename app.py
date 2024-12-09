import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re

# Set up page configuration
st.set_page_config(
    page_title="Phishing URL Detection",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Add custom CSS for 3D animations and styling
st.markdown(
    """
    <style>
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1658388012384-23bc0c66e3ac?q=80&w=2970&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            font-family: 'Arial', sans-serif;
        }

        .title {
            color: #A0E7E5;
            text-align: center;
            font-size: 4.5rem;
            font-weight: bold;
            margin-top: 30px;
            animation: glow 1.5s infinite alternate;
            letter-spacing: 3px;
        }

        .think-box {
            color: #FFAEBC;
            text-align: center;
            font-size: 2.8rem;  /* Increased size */
            font-weight: bold;
            margin: 40px auto;
            padding: 20px;
            max-width: 700px;
            background: rgba(17, 34, 64, 0.85);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            animation: move-left-right 4s infinite alternate ease-in-out;
        }

        @keyframes move-left-right {
            0% {
                transform: translateX(0);
            }
            50% {
                transform: translateX(20px);
            }
            100% {
                transform: translateX(0);
            }
        }

        .info {
            color: #FFAEBC;
            text-align: center;
            font-size: 1.8rem;
            margin-bottom: 40px;
        }

        .box {
            margin: 40px auto;
            padding: 40px;
            max-width: 700px;
            background: rgba(17, 34, 64, 0.85);
            border-radius: 15px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }

        input {
            width: 100%;
            padding: 20px;
            margin-bottom: 25px;
            border-radius: 8px;
            border: 2px solid #FFAEBC;
            font-size: 1.3rem;
            background: transparent;
            color: #FFFFFF;
            outline: none;
            transition: 0.3s ease;
        }

        input:hover {
            border-color: #B4F8C8;
        }

        .button {
            width: 100%;
            padding: 20px;
            border: none;
            border-radius: 8px;
            font-size: 1.5rem;
            cursor: pointer;
            background: linear-gradient(45deg, #FFAEBC, #A0E7E5);
            color: #0A192F;
            font-weight: bold;
            transition: 0.3s ease;
            box-shadow: 0 8px 15px rgba(255, 174, 188, 0.4);
        }

        .button:hover {
            background: linear-gradient(45deg, #A0E7E5, #FFAEBC);
            transform: scale(1.1);
            box-shadow: 0 10px 20px rgba(255, 174, 188, 0.6);
        }

        .result {
            margin-top: 25px;
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            color: #FFAEBC;
            animation: pop 0.8s ease-out;
        }

        @keyframes glow {
            0%, 100% {
                text-shadow: 0 0 25px #A0E7E5, 0 0 45px #A0E7E5;
            }
            50% {
                text-shadow: 0 0 35px #B4F8C8, 0 0 60px #B4F8C8;
            }
        }

        @keyframes pop {
            0% {
                transform: scale(0.9);
            }
            100% {
                transform: scale(1);
            }
        }

        select {
            width: 100%;
            padding: 20px;
            margin-bottom: 25px;
            border-radius: 8px;
            border: 2px solid #FFAEBC;
            font-size: 1.3rem;
            background: transparent;
            color: #FFFFFF;
            outline: none;
            transition: 0.3s ease;
        }

        select:hover {
            border-color: #B4F8C8;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header
st.markdown('<div class="title">PHISHING URL DETECTION</div>', unsafe_allow_html=True)

# Add "Think Before You Click" text in place of Box 2
st.markdown('<div class="think-box">Think Before You Click</div>', unsafe_allow_html=True)

# Input box and selection inside a styled box
url = st.text_input('Enter URL', placeholder="https://example.com", key="url_input")

# Dropdown for model selection
choice = st.selectbox(
    "Select Machine Learning Model",
    [
        'Random Forest', 'Support Vector Machine', 'Decision Tree',
        'AdaBoost', 'Neural Network', 'K-Neighbors', 'Gaussian Naive Bayes'
    ],
    key="model_choice",
)

# The rest of your backend code remains unchanged...

# Select the model based on user choice
model = ml.nb_model
if choice == 'Random Forest':
    model = ml.rf_model
elif choice == 'Support Vector Machine':
    model = ml.svm_model
elif choice == 'Decision Tree':
    model = ml.dt_model
elif choice == 'Random Forest':
    model = ml.rf_model
elif choice == 'Gaussian Naive Bayes':
    model = ml.nb_model
elif choice == 'AdaBoost':
    model = ml.ab_model
elif choice == 'Neural Network':
    model = ml.nn_model
elif choice == 'K-Neighbors':
    model = ml.kn_model

# Button to check the URL
if st.button('Check URL', key="check_button"):
    if url:
        try:
            response = re.get(url, verify=False, timeout=4)
            if response.status_code != 200:
                st.warning("HTTP connection was not successful for the URL, If possible try to avoid using it")
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                vector = [fe.create_vector(soup)]  # Ensure 2D array format
                result = model.predict(vector)

                if result[0] == 0:
                    st.markdown('<div class="result" style="color: #64FFDA;">✅ This website is legitimate!</div>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown('<div class="result" style="color: #FF6B6B;">🚨 Warning! This website is a potential phishing site!</div>', unsafe_allow_html=True)

        except re.exceptions.RequestException as e:
            # Instead of error, generate features based on a predefined phishing HTML structure for testing
            st.warning("Seems like the website isn't actively running. So, generating the predefined phishing features for analysis.")

            # Create a simple predefined phishing HTML to use as soup
            phishing_html = """
            <html>
                <head><title>PayPal Update</title></head>
                <body>
                    <form action="/login" method="post">
                        <input type="text" name="username" />
                        <input type="password" name="password" />
                        <input type="submit" value="Login" />
                    </form>
                </body>
            </html>
            """
            soup = BeautifulSoup(phishing_html, "html.parser")
            vector = [fe.create_vector(soup)]  # Ensure 2D array format
            result = model.predict(vector)

            if result[0] == 0:
                st.markdown('<div class="result" style="color: #64FFDA;">✅ This website is legitimate!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result" style="color: #FF6B6B;">🚨 Warning! This website is a potential phishing site!</div>', unsafe_allow_html=True)
                
    else:
        st.warning("Please enter a valid URL!")

# Footer
st.markdown(
    """
    <div style="text-align: center; color: #CCD6F6; margin-top: 30px;">
        <p>© Susan & Bimal</p>
    </div>
    """,
    unsafe_allow_html=True,
)
