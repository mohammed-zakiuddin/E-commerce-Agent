import streamlit as st
from duckduckgo_search import DDGS
import pandas as pd
import re

st.set_page_config(page_title="ShopSmart AI", page_icon="🛒", layout="wide")

st.title("🛒 ShopSmart AI - E-commerce Agent")
st.write("Finds, compares & recommends the best buy instantly!")

# Smarter English check
def is_mostly_english(text):
    if not text:
        return False
    english_chars = re.findall(r"[A-Za-z\s]", text)
    return len(english_chars) / len(text) > 0.6

# Extract price from text (₹, $, numbers)
def extract_price(text):
    if not text:
        return float('inf')
    prices = re.findall(r"[\$₹]?\s?[\d,]+(?:\.\d+)?", text)
    price_nums = []
    for p in prices:
        p_clean = p.replace("₹", "").replace("$", "").replace(",", "").strip()
        try:
            price_nums.append(float(p_clean))
        except:
            continue
    return min(price_nums) if price_nums else float('inf')

query = st.text_input("Enter the product you want to search:")

if query:
    st.subheader(f"🔎 Searching for: {query}")
    
    products = []
    with DDGS() as ddgs:
        search_query = query + " buy online price English"
        for r in ddgs.text(
            search_query,
            region="us-en",
            safesearch="Moderate",
            max_results=10
        ):
            title = r.get("title", "")
            desc = r.get("body", "")
            link = r.get("href", "")
            
            if is_mostly_english(title) or is_mostly_english(desc):
                price = extract_price(title + " " + desc)
                products.append({"Product": title, "Description": desc, "Link": link, "Price": price})
    
    if products:
        # Sort by price
        df = pd.DataFrame(products).sort_values(by="Price")

        st.subheader("📊 Product Comparison Table")
        
        # Make clickable links
        df['Link'] = df['Link'].apply(lambda x: f"[Visit]({x})")
        st.dataframe(df[["Product", "Description", "Link", "Price"]], use_container_width=True)

        # Best Buy = lowest price
        best_product = df.iloc[0]
        st.success(f"✅ Best Buy Suggestion: {best_product['Product']} at {best_product['Price']}")
        st.markdown(f"[Check it out here]({products[0]['Link']})", unsafe_allow_html=True)
        
    else:
        st.error("No English product results found. Try a different keyword.")
