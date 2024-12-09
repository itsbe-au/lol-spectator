import datetime
import streamlit as st
import requests

def get_newsfeed():
    response = requests.get("https://spec.com.au/wp-json/wp/v2/article?per_page=100")
    return response.json()

st.title("LOL Spectator")

st.write("Soooo, it turns out the Hamilton Spectator's API is just... wide open.")

st.write('---')

newsfeed = get_newsfeed()

# Get query params for article ID
params = st.query_params.get_all(key="article")
article_id = params[0] if params else None

if article_id:
    # Show single article
    article = next((a for a in newsfeed if str(a['id']) == article_id), None)
    if article:
        st.write(f"### {article['title']['rendered']}")
        st.write(datetime.datetime.strptime(article['date'], '%Y-%m-%dT%H:%M:%S').strftime('%b %d, %Y'))
        st.write(article['content']['rendered'], unsafe_allow_html=True)
        if st.button("Back to Articles"):
            st.query_params.clear()
            st.rerun()
else:
    # Show article cards
    for article in newsfeed:
        with st.container():
            st.write(f"### {article['title']['rendered']}")
            st.write(datetime.datetime.strptime(article['date'], '%Y-%m-%dT%H:%M:%S').strftime('%b %d, %Y'))
            if st.button("Read More", key=article['id']):
                st.query_params["article"] = article['id']
                st.rerun()
            st.divider()
