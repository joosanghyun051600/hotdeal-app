import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# --- [1] 앱 기본 설정 ---
st.set_page_config(
    page_title="린치핀 핫딜 앱",
    page_icon="🔥",
    layout="wide"
)

# --- [2] 디자인 (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    /* 탭 글씨 크기 키우기 */
    button[data-baseweb="tab"] {
        font-size: 18px;
        font-weight: bold;
    }
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

# --- [3] 데이터 엔진 1: (진짜) Yes24 크롤러 ---
@st.cache_data(ttl=600)
def get_real_yes24_deals():
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
                
                results.append({"상품명": title, "가격": price + "원", "링크": link, "이미지": img_url})
                if len(results) >= 12: break # 12개만
            except: continue
        return results
    except: return []

# --- [3-2] 데이터 엔진 2: (가짜) 예시 데이터 생성기 ---
# 아직 크롤링 소스가 없는 탭을 보여주기 위한 가짜 데이터입니다.
def get_dummy_data(category):
    data = []
    if category == "음식점":
        names = ["백종원 파스타", "서울 초밥 맛집", "강남 스테이크", "홍대 떡볶이"]
        images = ["https://source.unsplash.com/400x300/?food,pasta", "https://source.unsplash.com/400x300/?sushi", "https://source.unsplash.com/400x300/?steak", "https://source.unsplash.com/400x300/?koreanfood"]
    elif category == "숙박":
        names = ["제주 오션뷰 호텔", "강릉 감성 펜션", "서울 5성급 호캉스", "부산 에어비앤비"]
        images = ["https://source.unsplash.com/400x300/?hotel", "https://source.unsplash.com/400x300/?house", "https://source.unsplash.com/400x300/?room", "https://source.unsplash.com/400x300/?travel"]
    else: # 건강/피트니스
        names = ["3개월 헬스 할인권", "요가/필라테스 1회권", "단백질 보충제 특가", "러닝화 한정판"]
        images = ["https://source.unsplash.com/400x300/?gym", "https://source.unsplash.com/400x300/?yoga", "https://source.unsplash.com/400x300/?protein", "https://source.unsplash.com/400x300/?shoes"]

    for i in range(4):
        data.append({
            "상품명": names[i],
            "가격": "99,000원 (예시)",
            "링크": "#",
            "이미지": f"https://via.placeholder.com/300?text={category}+Image" # 이미지 에러 방지용 기본 이미지
        })
    return data

# --- [4] 메인 화면 ---
def main():
    st.title("🔥 린치핀 핫딜 모음")
    
    # [핵심] 탭 메뉴 만들기
    tab1, tab2, tab3, tab4 = st.tabs(["🍽️ 음식점", "🏨 숙박", "💪 건강/피트니스", "📈 마케팅"])

    # --- 탭 1: 음식점 ---
    with tab1:
        st.caption("전국의 맛집 할인 정보를 모았습니다.")
        data = get_dummy_data("음식점")
        cols = st.columns(4)
        for i, item in enumerate(data):
            with cols[i]:
                with st.container():
                    st.image(item['이미지'], use_container_width=True)
                    st.markdown(f"**{item['상품명']}**")
                    st.markdown(f":red[**{item['가격']}**]")
                    st.button("쿠폰 받기", key=f"food_{i}")

    # --- 탭 2: 숙박 ---
    with tab2:
        st.caption("최저가 숙소 예약을 도와드립니다.")
        data = get_dummy_data("숙박")
        cols = st.columns(4)
        for i, item in enumerate(data):
            with cols[i]:
                with st.container():
                    st.image(item['이미지'], use_container_width=True)
                    st.markdown(f"**{item['상품명']}**")
                    st.markdown(f":blue[**{item['가격']}**]")
                    st.button("예약하기", key=f"stay_{i}")
    
    # --- 탭 3: 건강 ---
    with tab3:
        st.caption("건강한 삶을 위한 특가 상품입니다.")
        data = get_dummy_data("건강")
        cols = st.columns(4)
        for i, item in enumerate(data):
            with cols[i]:
                with st.container():
                    st.image(item['이미지'], use_container_width=True)
                    st.markdown(f"**{item['상품명']}**")
                    st.markdown(f":green[**{item['가격']}**]")
                    st.button("구매하기", key=f"health_{i}")

    # --- 탭 4: 마케팅 (진짜 데이터) ---
    with tab4:
        st.caption("마케팅/경제 베스트셀러 도서 정보를 실시간으로 가져옵니다.")
        if st.button("🔄 최신 정보 불러오기"):
            st.cache_data.clear()
            st.rerun()
            
        data = get_real_yes24_deals() # 여기만 진짜 크롤링 연결!
        
        if data:
            cols = st.columns(4)
            for i, item in enumerate(data):
                with cols[i % 4]:
                    with st.container():
                        st.image(item['이미지'], use_container_width=True)
                        st.markdown(f"**{item['상품명'][:16]}...**")
                        st.markdown(f":blue[**{item['가격']}**]")
                        st.link_button("구매하러 가기 👉", item['링크'], use_container_width=True)

if __name__ == "__main__":
    main()
