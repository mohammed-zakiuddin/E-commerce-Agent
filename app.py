import streamlit as st
from duckduckgo_search import DDGS
import pandas as pd
import re

st.set_page_config(page_title="ShopSmart AI", page_icon="🛒", layout="wide")

st.title("🛒 ShopSmart AI - E-commerce Agent")
st.write("Finds, compares & recommends the best buy instantly!")

# Smarter English check (allow ₹, $, numbers, %, etc.)
def is_mostly_english(text):
    if not text:
        return False
    english_chars = re.findall(r"[A-Za-z\s]", text)
    return len(english_chars) / len(text) > 0.6   # 60% English threshold

query = st.text_input("Enter the product you want to search:")

if query:
    st.subheader(f"🔎 Searching for: {query}")
    
    products = []
    with DDGS() as ddgs:
        search_query = query + " buy online price English"
        for r in ddgs.text(
            search_query,
            region="us-en",   # try "in-en" if you want India English results
            safesearch="Moderate",
            max_results=10
        ):
            title = r.get("title", "")
            desc = r.get("body", "")
            link = r.get("href", "")

            if is_mostly_english(title) or is_mostly_english(desc):
                products.append({"Product": title, "Description": desc, "Link": link})
    
    if products:
        st.subheader("📊 Product Comparison Table")
        df = pd.DataFrame(products)
        st.dataframe(df, use_container_width=True)

        # Best pick = first result
        best_product = products[0]
        st.success(f"✅ Best Buy Suggestion: {best_product['Product']}")
        st.markdown(f"[Check it out here]({best_product['Link']})")
    else:
        st.error("No English product results found. Try a different keyword.")
