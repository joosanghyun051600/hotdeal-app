import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- [1] 앱 기본 설정 ---
st.set_page_config(
    page_title="나만의 핫딜 앱",
    page_icon="🔥",
    layout="wide"
)

# --- [2] 디자인 꾸미기 ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    div[data-testid="stContainer"] {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%;
        background-color: #ff6b00;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #e65c00; color: white; }
    img { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- [3] 데이터 수집 엔진 ---
@st.cache_data(ttl=600)
def get_hot_deals():
    url = "https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select("#yesBestList li")
        
        results = []
        for item in items:
            try:
                title = item.select_one(".gd_name").get_text(strip=True)
                link = "https://www.yes24.com" + item.select_one(".gd_name")['href']
                price = item.select_one(".yes_b").get_text(strip=True)
                img_tag = item.select_one("img")
                img_url = img_tag.get('data-original') or img_tag.get('src')
                
                results.append({
                    "상품명": title,
                    "가격": price + "원",
                    "링크": link,
                    "이미지": img_url
                })
                if len(results) >= 40: break
            except: continue
        return results
    except: return []

# --- [4] 메인 화면 ---
def main():
    with st.sidebar:
        st.title("🔎 핫딜 검색")
        keyword = st.text_input("검색어 입력", placeholder="예: 트렌드, 돈")
        if st.button("🔄 새로고침"):
            st.cache_data.clear()
            st.rerun()

    st.title("🔥 실시간 베스트 핫딜")
    st.divider()

    data = get_hot_deals()
    if keyword:
        data = [item for item in data if keyword in item['상품명']]
    
    if data:
        cols = st.columns(4)
        for i, item in enumerate(data):
            with cols[i % 4]:
                with st.container():
                    st.image(item['이미지'], use_container_width=True)
                    st.markdown(f"**{item['상품명'][:18]}...**")
                    st.markdown(f":blue[**{item['가격']}**]")
                    st.link_button("구매하러 가기 👉", item['링크'], use_container_width=True)
    else:
        st.warning("검색 결과가 없습니다.")

if __name__ == "__main__":
    main()

