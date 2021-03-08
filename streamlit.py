import streamlit as st

# Text/Title

st.title("Streamlit Tutorials")

# Header/Subheader

st.header("This is a header")
st.subheader("This is a subheader")

# Text
st.text("Hello Streamlit")

# Markdown
st.markdown("### This is a Markdown")

# Error/Colorful Text

st.success("Successful!")

st.info("Information")

st.warning("This is a warning")

st.error("This is an error!!")

st.exception("NameError('name three not defined')")

# Get Help Info about Python
st.help(range)

# Writing Text (Super Function)

st.write("Text with write")

# Images

from PIL import Image

img = Image.open("abstract.jpg")

st.image(img,width=300,caption='Simple Abstract')

# Widget
# Checkbox

if st.checkbox("Show/Hide"):
    st.text("Showing or Hiding")
    
# Radio 
status = st.radio("What is the status?", ("Active","Inactive"))

if status == 'Active':
    st.success("You are Active!")
else:
    st.warning('Inactive')
    
# Select Box
occupation = st.selectbox('Your occupation', 
                          ['Programmer', 
                           'Data Scientist'])

st.write("You selected this option " + occupation)

# Multiselect

location = st.multiselect('Where do you work?', 
                          ['Swiss', 'Japan'])

# slider

age = st.slider("What is your level",1,5)

# Buttons

st.button("Simple Button")

if st.button('About'):
    st.text('streamlit is very cool!')
    
# Text_Input

firstname = st.text_input('Enter Your First Name')

if st.button('submit'):
    result = firstname.title()
    st.success(result)
    
# Text_Area


msg = st.text_area('Enter Your First Name')

if st.button('submit!'):
    result = msg.title()
    st.success(result)
    
# Date Input

import datetime
today = st.date_input("Today is ", datetime.datetime.now())

# Time

the_time = st.time_input("The time is", datetime.time())


# Displaying JSON

st.text("Display JSON")
st.json({'name': 'Jessie', 'gender': 'male'})



# Display Raw Code

# 1
st.text('Display Raw Code')

st.code('import numpy as np\n'
        'import datetime as dt')
st.code('import pandas as pd')

# 2

with st.echo():
    # This will also show as a comment    
    import pandas as pd
    df = pd.DataFrame()


# Progress Bar

import time

my_bar = st.progress(0)
for p in range(10):
    my_bar.progress(p+1)



# Spinner

with st.spinner('Loading...'):
    time.sleep(5)
    
st.success("Finished")


# Ballons

st.balloons()


# SIDEBARS

st.sidebar.header("About")

st.sidebar.text("This is Streamlit Tutorial")





# Functions
@st.cache
def run_function():
    
    return range(100)


st.write(run_function())




# Plot

st.pyplot()


# DataFrame
st.dataframe(df)
# Tables
st.table(df)

































































































