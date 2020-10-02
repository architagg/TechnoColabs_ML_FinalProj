import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

model = pickle.load(open('model.pkl', 'rb'))
model1 = pickle.load(open("model1.pkl", "rb"))

edu = {1: "Graduate school", 2: "University", 3: "High school", 4: "Others"}


def format_func(option):
    return edu[option]


import base64


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


set_png_as_page_bg('images/bg.png')

# page_bg_img = '''
# <style>
# body {
# background-image: url(./images/temp.jpeg);
#   background-color: #cccccc;
#   height: 500px;
#   background-position: center;
#   background-repeat: no-repeat;
#   background-size: cover;
# }
# </style>
# '''
#
# st.markdown(page_bg_img, unsafe_allow_html=True)


def Credit_Card_Default_Prediction(LIMIT_BAL, EDUCATION, AGE, PAY_1, BILL_AMT1, BILL_AMT2, BILL_AMT3,
                                   BILL_AMT4, BILL_AMT5, BILL_AMT6, PAY_AMT1, PAY_AMT2, PAY_AMT3, PAY_AMT4, PAY_AMT5,
                                   PAY_AMT6):
    try:
        input = np.array([[LIMIT_BAL, EDUCATION, AGE, PAY_1, BILL_AMT1, BILL_AMT2, BILL_AMT3, BILL_AMT4,
                           BILL_AMT5, BILL_AMT6, PAY_AMT1, PAY_AMT2, PAY_AMT3, PAY_AMT4, PAY_AMT5, PAY_AMT6]]).astype(
            np.float64)
        input = model1.transform(input)
        prediction = model.predict(input)
        return prediction[0]
    except ValueError:
        print("None")


def main():
    st.markdown("""

    <h1 style="color:black;text-align:left;">Technocolabs ML Final Project - Archit Aggarwal</h1>
    </div>
    """, unsafe_allow_html=True)
    html_temp = """

    <h1 style="color:black;text-align:left;">Credit Card Default Prediction App</h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    html_preform = """
    <h3 style="color:red;text-align:left;">Enter all values in NT Dollars </h3>
    <div style="margin-bottom:40px;">
    
    </div>
    """
    st.markdown(html_preform, unsafe_allow_html=True)
    LIMIT_BAL = st.text_input("Credit Provided (Individual and Supplementary)")
    EDUCATION = st.selectbox("Select Education Level", options=list(edu.keys()), format_func=format_func)
    AGE = st.slider("Select Age:", min_value=21, max_value=90)
    html_pay1 = """
     <h3 style="color:black;text-align:left;"><b>Repayment Status in September</b></h3>
     <p style="color:red;text-align:left;"><i>The measurement scale for the repayment status is as follows: -1 = pay duly,1 = payment delay for one month,2 = payment delay for two months, and so on up to 8 = payment delay for eight months, 9 = payment delay for nine months and above.</i></p>
     """
    st.markdown(html_pay1, unsafe_allow_html=True)
    PAY_1 = st.text_input("Enter Repayment status in September")
    html_gap1 = """
        <h3 style="color:black;text-align:left;"> Enter Bill Statement Amounts </h3>
        <div style="margin-bottom:40px;">
        </div>
        """
    st.markdown(html_gap1, unsafe_allow_html=True)
    BILL_AMT1 = st.text_input("Amount in September")
    BILL_AMT2 = st.text_input("Amount in August")
    BILL_AMT3 = st.text_input("Amount in July")
    BILL_AMT4 = st.text_input("Amount in June")
    BILL_AMT5 = st.text_input("Amount in May")
    BILL_AMT6 = st.text_input("Amount in April")
    html_gap2 = """
            <h3 style="color:black;text-align:left;"><b>Enter Paid Amounts </b></h3>
            <div style="margin-bottom:40px;">
            </div>
            """
    st.markdown(html_gap2, unsafe_allow_html=True)
    PAY_AMT1 = st.text_input("Paid Amount in September")
    PAY_AMT2 = st.text_input("Paid Amount in August")
    PAY_AMT3 = st.text_input("Paid Amount in July")
    PAY_AMT4 = st.text_input("Paid Amount in June")
    PAY_AMT5 = st.text_input("Paid Amount in May")
    PAY_AMT6 = st.text_input("Paid Amount in April")

    no_html = """  
      <div style="background-color:None;padding:10px >
       <h2 style="color:green;text-align:center;">The account owner did not fail to make the minimum payment.</h2>
       </div>
    """
    yes_html = """  
      <div style="background-color:None;padding:10px >
       <h2 style="color:red ;text-align:center;"> The account owner failed to make the minimum payment.</h2>
       </div>
    """
    none_html = """  
      <div style="background-color:None;padding:10px >
       <h2 style="color:black ;text-align:center;">Please enter all the values correctly !</h2>
       </div>
    """

    if st.button("Predict"):
        output = Credit_Card_Default_Prediction(LIMIT_BAL, EDUCATION,  AGE, PAY_1, BILL_AMT1, BILL_AMT2,
                                                BILL_AMT3, BILL_AMT4, BILL_AMT5, BILL_AMT6, PAY_AMT1, PAY_AMT2,
                                                PAY_AMT3, PAY_AMT4, PAY_AMT5, PAY_AMT6)
        st.markdown('The Predicted value is: {}'.format(output))

        if output == 1:
            st.markdown(yes_html, unsafe_allow_html=True)
        elif output == 0:
            st.markdown(no_html, unsafe_allow_html=True)
        else:
            st.markdown(none_html, unsafe_allow_html=True)


if __name__ == '__main__':
    main()