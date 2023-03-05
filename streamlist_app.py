import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu \n')
streamlit.text('🥣Omega-3 & Blueberry oatmeal \n')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie \n')
streamlit.text('🐔Hard boiled free range eggs')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
   
#import pandas # commented this after all the import statements are organized at the beggining 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

#create the repeatable code lock (called a function)
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
   
# New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.write("Please select a fruit to get information.")
   else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)  # output it on to the screen as a table format

except URLError as e:
   streamlit.error()

streamlit.header("View our fruit list - Add yur favorites!")
#snowfalke-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
         return my_cur.fetchall()
      
# Add a button to load the fruit
if streamlit.button('Get fruit List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)

# don't run anything past here while we troubleshoot
# streamlit.stop()

# Allow the end-user to add a fruit to the list (i.e., programatically add a second text entry box)
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
         return "Thanks for adding " + new_fruit 
      
fruit_to_add = streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add a fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(fruit_to_add)
   my_cnx.close()
   streamlit.text(back_from_function)


