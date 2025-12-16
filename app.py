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
    
    /* 사이드바 디자인 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* 탭 버튼 디자인 */
    button[data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
    }
    
    /* 카드 박스 디자인 */
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
    
    /* 버튼 공통 디자인 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 40px;
        font-weight: bold;
    }
    img { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- [3] 만능 데이터 엔진 ---
@st.cache_data(ttl=600)
def get_yes24_data(category_num):
    url = f"https://www.yes24.com/Product/Category/BestSeller?categoryNumber={category_num}"
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
                if len(results) >= 8: 
                    break
            except: continue
        return results
    except: return []

# --- [4] 메인 화면 ---
def main():
    # ---------------------------------------------------------
    # [NEW] 사이드바: 명함 및 연락처 기능 추가
    # ---------------------------------------------------------
    with st.sidebar:
        st.title("🏢 린치핀 마케팅")
        st.markdown("---") # 구분선
        
        # 소개글
        st.info("비즈니스 성장을 돕는\n최적의 솔루션을 제공합니다.")
        
        # 연락처 정보
        st.caption("📞 Contact")
        st.text("010-5802-6463") # 본인 번호로 수정 가능
        st.text("csp051600@naver.com") # 이메일 수정 가능
        
        st.markdown("---") # 구분선
        
        # [핵심] 카카오톡 오픈채팅 버튼
        # 아래 주소를 본인의 오픈채팅방 주소로 바꿔주세요!
        kakao_url = "https://pf.kakao.com/_UMxbzn" 
        
        st.link_button(
            "💬 1:1 채팅 문의하기", 
            kakao_url, 
            use_container_width=True,
            help="클릭하면 카카오톡으로 연결됩니다."
        )
        
        st.markdown("---")
        st.caption("ⓒ 2025 Linchpin Marketing")
    # ---------------------------------------------------------

    # 메인 컨텐츠
    st.title("💎 린치핀 good deal ")
    st.caption("당신의 성장을 위한 분야별 베스트 정보를 실시간으로 제공합니다.")

    tab1, tab2, tab3, tab4 = st.tabs(["🍳 맛집/요리", "✈️ 여행/숙박", "💪 건강/헬스", "📈 마케팅/트렌드"])

    # 탭 1: 맛집 (요리)
    with tab1:
        st.success("🔥 요즘 뜨는 요리법과 맛집 가이드북을 모았습니다.")
        data = get_yes24_data("001001011") 
        if data:
            cols = st.columns(4)
            for i, item in enumerate(data):
                with cols[i % 4]:
                    with st.container():
                        st.image(item['이미지'], use_container_width=True)
                        st.markdown(f"**{item['상품명'][:16]}...**")
                        st.caption(item['가격'])
                        st.link_button("보러가기", item['링크'], use_container_width=True)

    # 탭 2: 여행
    with tab2:
        st.info("✈️ 떠나고 싶은 당신을 위한 추천 여행 가이드입니다.")
        data = get_yes24_data("001001009") 
        if data:
            cols = st.columns(4)
            for i, item in enumerate(data):
                with cols[i % 4]:
                    with st.container():
                        st.image(item['이미지'], use_container_width=True)
                        st.markdown(f"**{item['상품명'][:16]}...**")
                        st.caption(item['가격'])
                        st.link_button("보러가기", item['링크'], use_container_width=True)

    # 탭 3: 건강
    with tab3:
        st.warning("💪 건강한 신체를 위한 필독서입니다.")
        data = get_yes24_data("001001046") 
        if data:
            cols = st.columns(4)
            for i, item in enumerate(data):
                with cols[i % 4]:
                    with st.container():
                        st.image(item['이미지'], use_container_width=True)
                        st.markdown(f"**{item['상품명'][:16]}...**")
                        st.caption(item['가격'])
                        st.link_button("보러가기", item['링크'], use_container_width=True)
    
    # 탭 4: 마케팅
    with tab4:
        st.error("📈 성공을 부르는 비즈니스 인사이트입니다.")
        data = get_yes24_data("001") 
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

