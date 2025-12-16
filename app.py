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
    
    /* 사이드바 전체 배경 흰색 고정 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }

    /* 사이드바 글씨: 검은색 (#000000) */
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] .stText, 
    [data-testid="stSidebar"] h1 {
        color: #000000 !important;
    }
    
    /* 사이드바 안의 링크/버튼 글씨: 흰색 (#ffffff) */
    [data-testid="stSidebar"] a {
         color: #ffffff !important;
         text-decoration: none; /* 밑줄 제거 */
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
    
    /* 일반 버튼 스타일 */
    .stButton>button {
        width: 100%;
        background-color: #333333;
        border: none;
        border-radius: 8px;
        height: 40px;
        font-weight: bold;
        color: white !important;
    }
    .stButton>button:hover {
        background-color: #000000;
    }

    /* [NEW] 링크 버튼(전화, 카톡) 스타일 강제 적용 */
    a[data-testid="stLinkButton"] {
        display: inline-block;
        width: 100%;
        background-color: #333333;
        color: #ffffff !important;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px; /* 버튼 사이 간격 */
    }
    a[data-testid="stLinkButton"]:hover {
        background-color: #000000;
    }
    
    img { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- [3] 데이터 엔진 ---
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
                results.append({"상품명": title, "가격": price + "원", "링크": link, "이미지": img_url})
                if len(results) >= 8: break
            except: continue
        return results
    except: return []

# --- [4] 메인 화면 ---
def main():
    # ---------------------------------------------------------
    # [사이드바]
    # ---------------------------------------------------------
    with st.sidebar:
        st.title("🏢 린치핀 마케팅")
        st.markdown("---") 
        
        st.info("비즈니스 성장을 돕는\n최적의 솔루션을 제공합니다.")
        
        st.caption("📞 Contact")
        
        # 1. 텍스트로 보여주기
        st.text("010-5802-6463") 
        st.text("csp051600@naver.com") 
        
        st.markdown("---") 
        
        # [NEW] 전화 걸기 버튼 (tel: 기능 사용)
        # 본인 전화번호로 수정하세요 (하이픈 - 없이 숫자만)
        phone_number = "01058026463" 
        st.link_button(
            "📞 전화 상담 바로 연결", 
            f"tel:{phone_number}", 
            use_container_width=True
        )

        # 2. 카카오톡 오픈채팅 버튼
        kakao_url = "https://open.kakao.com/o/sXxxxxx" 
        st.link_button(
            "💬 1:1 오픈채팅 문의하기", 
            kakao_url, 
            use_container_width=True
        )
        
        st.markdown("---")
        st.caption("ⓒ 2025 Linchpin Marketing")
    # ---------------------------------------------------------

    # 메인 컨텐츠
    st.title("💎 린치핀 라이프스타일 큐레이션")
    st.caption("당신의 성장을 위한 분야별 베스트 정보를 실시간으로 제공합니다.")

    tab1, tab2, tab3, tab4 = st.tabs(["🍳 맛집/요리", "✈️ 여행/숙박", "💪 건강/헬스", "📈 마케팅/트렌드"])

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
