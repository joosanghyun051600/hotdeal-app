import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- [1] 앱 기본 설정 ---
st.set_page_config(
    page_title="린치핀 큐레이션",
    page_icon="💎",
    layout="wide"
)

# --- [2] 디자인 (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    /* 탭 디자인 */
    button[data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
    }
    div[data-testid="stContainer"] {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    div[data-testid="stContainer"]:hover {
        transform: translateY(-5px);
    }
    .stButton>button {
        width: 100%;
        background-color: #333333;
        color: white;
        border: none;
        border-radius: 8px;
        height: 40px;
    }
    .stButton>button:hover { background-color: #000000; color: white; }
    img { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- [3] 만능 데이터 엔진 (카테고리 번호만 넣으면 됨!) ---
@st.cache_data(ttl=600)
def get_yes24_data(category_num):
    # categoryNumber 뒤에 숫자를 바꿔끼울 수 있게 만들었습니다.
    url = f"https://www.yes24.com/Product/Category/BestSeller?categoryNumber={category_num}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select("#yesBestList li")
        
        results = []
        for item in items:
            try:
                # 1. 제목
                title = item.select_one(".gd_name").get_text(strip=True)
                # 2. 링크
                link = "https://www.yes24.com" + item.select_one(".gd_name")['href']
                # 3. 가격
                price = item.select_one(".yes_b").get_text(strip=True)
                # 4. 이미지
                img_tag = item.select_one("img")
                img_url = img_tag.get('data-original') or img_tag.get('src')
                
                results.append({
                    "상품명": title,
                    "가격": price + "원",
                    "링크": link,
                    "이미지": img_url
                })
                if len(results) >= 8: # 탭마다 8개씩만 보여주기
                    break
            except: continue
        return results
    except: return []

# --- [4] 화면 구성 ---
def main():
    st.title(" linchpin deal ")
    st.caption("당신의 성장을 위한 분야별 베스트 정보를 실시간으로 제공합니다.")

    # 탭 메뉴 정의
    tab1, tab2, tab3, tab4 = st.tabs(["🍳 맛집/요리", "✈️ 여행/숙박", "💪 건강/헬스", "📈 마케팅/트렌드"])

    # --- 탭 1: 맛집/요리 (카테고리 번호: 001001011) ---
    with tab1:
        st.info("🔥 요즘 뜨는 요리법과 맛집 가이드북을 모았습니다.")
        data = get_yes24_data("001001011") # 요리 카테고리 번호
        if data:
            cols = st.columns(4)
            for i, item in enumerate(data):
                with cols[i % 4]:
                    with st.container():
                        st.image(item['이미지'], use_container_width=True)
                        st.markdown(f"**{item['상품명'][:16]}...**")
                        st.caption(item['가격'])
                        st.link_button("보러가기", item['링크'], use_container_width=True)

    # --- 탭 2: 여행/숙박 (카테고리 번호: 001001009) ---
    with tab2:
        st.info("✈️ 떠나고 싶은 당신을 위한 추천 여행 가이드입니다.")
        data = get_yes24_data("001001009") # 여행 카테고리 번호
        if data:
            cols = st.columns(4)
            for i, item in enumerate(data):
                with cols[i % 4]:
                    with st.container():
                        st.image(item['이미지'], use_container_width=True)
                        st.markdown(f"**{item['상품명'][:16]}...**")
                        st.caption(item['가격'])
                        st.link_button("보러가기", item['링크'], use_container_width=True)

    # --- 탭 3: 건강/헬스 (카테고리 번호: 001001046) ---
    with tab3:
        st.info("💪 건강한 신체를 위한 필독서입니다.")
        data = get_yes24_data("001001046") # 건강 카테고리 번호
        if data:
            cols = st.columns(4)
            for i, item in enumerate(data):
                with cols[i % 4]:
                    with st.container():
                        st.image(item['이미지'], use_container_width=True)
                        st.markdown(f"**{item['상품명'][:16]}...**")
                        st.caption(item['가격'])
                        st.link_button("보러가기", item['링크'], use_container_width=True)
    
    # --- 탭 4: 마케팅 (카테고리 번호: 001) ---
    with tab4:
        st.info("📈 성공을 부르는 비즈니스 인사이트입니다.")
        data = get_yes24_data("001") # 종합 베스트셀러
        if data:
            cols = st.columns(4)
            for i, item in enumerate(data):
                with cols[i % 4]:
                    with st.container():
                        st.image(item['이미지'], use_container_width=True)
                        st.markdown(f"**{item['상품명'][:16]}...**")
                        st.caption(item['가격'])
                        st.link_button("보러가기", item['링크'], use_container_width=True)

if __name__ == "__main__":
    main()

