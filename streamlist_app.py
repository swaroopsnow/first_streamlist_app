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
   
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

# New section to display fruityvice api response

streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?)
   if not fruit_choice:
      streamlit.write('The user entered ', fruit_choice)
   else:
      #import requests
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # streamlit.text(fruityvice_response.json()) -- commented it for now.

      # Take the json version of the response and normalize it 
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

      except URLError as e:
      streamlit.error()
      
# output it on to the screen as a table format
streamlit.dataframe(fruityvice_normalized)

# don't run anything past here while we troubleshoot
streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Allow the end-user to add a fruit to the list (i.e., programatically add a second text entry box)

fruit_to_add = streamlit.text_input('What fruit would you like add?','Jackfruit')
streamlit.write('Thanks for adding ', fruit_to_add)

# This will not work correctly but just go with it for now
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")

