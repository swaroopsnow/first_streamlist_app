import streamlit

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu \n')
streamlit.text('🥣Omega-3 & Blueberry oatmeal \n')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie \n')
streamlit.text('🐔Hard boiled free range eggs')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
   
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
