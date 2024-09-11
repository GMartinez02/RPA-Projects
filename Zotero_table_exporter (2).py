#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[3]:


path = r"C:\Users\gmart\Desktop\Spring 2024\PONI\jallison.csv"
df = pd.read_csv(path, index_col="Key")

properties_measured = [
    "TEM",
    "Atom probe tomography",
    "Optical micrograph",
    "SEM",
    "Macro image",
    "EBSD",
    "XRD",
    "EDS",
    "NAMLT",
    "Tensile behavior",
    "Shear strength behavior",
    "3PB",
    "Electrical conductivity",
    "PDP (potentiodynamic polarization)",
    "EIS (electrochemical impedance spectroscopic)",
    "Computational thermodynamics",
    "Line-intercept method",
    "fatigue behavior",
    "fatigue model"
]

focus_of_investigation = [
    "heat treatment",
    "temperature behavior",
    "preheated substrate",
    "dissimilar joining",
    "simulation",
    "corrosion",
    "neutron imaging",
    "layer thickness",
    "overlap",
    "fatigue"
]


# In[4]:


df.dropna(subset=['Automatic Tags', 'Manual Tags'], inplace=True)


# In[17]:


df["properties_measured"] = ""
df["focus_of_investigation"] = ""


# In[18]:


df['article_id'] = df['Author'].str.split(';').str[0].str.strip()
df['article_id'] = df['article_id'] + df['Publication Year'].astype(str)


# In[19]:


df["Automatic Tags"] = df['Automatic Tags'].astype('string')
df["Manual Tags"] = df['Manual Tags'].astype('string')
df["Tags"] = df["Automatic Tags"] +';'+ df["Manual Tags"]


# In[20]:


temp_focus = []
temp_properties = []

def process_tags(tags):
    properties_found = []
    focus_found = []
    
    observation = tags.split(";")  
    
    for list_element in observation:
        if any(i in list_element for i in properties_measured):
            properties_found.append(list_element)
            
        if any(i in list_element for i in focus_of_investigation):
            focus_found.append(list_element)
    
    return ";".join(properties_found), ";".join(focus_found)

df[['Properties_Measured', 'Focus_of_Investigation']] = df['Tags'].apply(process_tags).apply(pd.Series)


# In[21]:


df.drop(df.columns.difference(['article_id', 'Title', 'Properties_Measured', 'Focus_of_Investigation']), 1, inplace=True)


# In[22]:


df.head()


# # Testing Pyzotero

# In[5]:


research_groups = {
    "Alabama": "ENTFKF9A",
    "BYU": "FHUA2AG6",
    "CSU": "J9P6QVL5",
    "Deakin": "FJDVBN8V",
    "ERDC": "A2IE9CCN",
    "JALLISON": "8R7A5FQF",
    "Jiangsu": "PIYWXUPX",
    "LSU": "BZPPUWWE",
    "Macao": "Q7J9TBZS",
    "Milano": "53EIUIDU",
    "Nanjing": "BXJRXGGL",
    "Northwester": "PZFMYYIG",
    "RIT": "IT7R9HI9",
    "Southwest": "8GR28UYH",
    "Tianjin": "YZFTU45C",
    "UNT": "K35CYECW",
    "UTK": "EKEA9F9A",
    "UTwente": "RIABIUZK",
    "UW Madison": "YWZYT6L9",
    "Yu Group": "A869GQQS"
}


# In[7]:


from pyzotero import zotero

library_id = 5025296
api_key = "98LqcOAUtBstPC5XJe4699fz"
library_type = 'group'

zot = zotero.Zotero(library_id, library_type, api_key)


# In[13]:


def extract_item_info(collection_id):
    items = zot.collection_items(collection_id)
    item_info = {}
    for item in items:
        item_id = item['key']
        authors = item['data'].get('creators', [])
        author_names = ', '.join([author['lastName'] for author in authors])
        year = item['data'].get('date', '')
        title = item['data'].get('title', '')
        tags = [tag['tag'] for tag in item['data'].get('tags', [])]
        item_info[item_id] = {
            'Author': author_names,
            'Year': year,
            'Title': title,
            'Tags': ', '.join(tags)
        }
    return item_info


# In[14]:


data = []

for group_name, group_id in research_groups.items():
    print("Research Group:", group_name)
    collection_info = extract_item_info(group_id)
    for item_id, info in collection_info.items():
        data.append({
            'Research Group': group_name,
            'Item ID': item_id,
            'Author': info['Author'],
            'Year': info['Year'],
            'Title': info['Title'],
            'Tags': info['Tags']
        })
        
df = pd.DataFrame(data)


# In[17]:


df.head(10)


# # Combining Pyzotero and Application

# In[ ]:




