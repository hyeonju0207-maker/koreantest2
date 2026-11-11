import streamlit as st
import re

st.set_page_config(
    page_title="원미동 사람들 - 서술형 자동 채점 시스템",
    page_icon="📝",
    layout="wide"
)

st.title("📝 《원미동 사람들 - 일용할 양식》 서술형 자동 채점 시스템")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["✍️ 학생 답안 입력 및 채점", "📊 채점 기준표 안내", "⚙️ 채점 로직 세부 규칙"])

with tab2:
    st.subheader("📌 문항별 채점 기준표")
    st.markdown("""
    ### [문항 1] 이웃 간 갈등의 표면적 원인과 근본적 원인 (총 7점)
    - **표면적 원인 (4점, 각 2점)**:
      1. 경호네 슈퍼와 형제슈퍼(임금님 슈퍼) 간의 과도한 가격 파괴 및 경품 경쟁
      2. 새로 문을 연 싱싱청과물이 기존 슈퍼들의 영역(과물/야채 등)을 침범하여 발생한 갈등
    - **근본적 원인 (3점)**:
      - 소도시 변두리의 각박한 경제적 현실 속에서 생존하기 위해 이웃 간의 정을 잃고 이기적·속물적으로 변해가는 서민들의 삶과 구조적 현실

    ### [문항 2] 소설 제목 '일용할 양식'의 반어적 의미와 주제 (총 5점)
    - **제목의 의미 및 반어성 (3점)**:
      - 최소한의 생계를 뜻하는 성경 구절에서 유래했으나, 소설 속에서는 이웃을 짓밟고서라도 이익을 챙겨야 하는 이기적인 소시민의 모습을 반어적으로 상징함
    - **주제 의식 및 서민의 삶 (2점)**:
      - 각박한 생존 경쟁 속에서 최소한의 양심과 인간성을 상실해 가는 변두리 서민들의 애환을 드러냄
    """)

with tab3:
    st.subheader("💡 세부 채점 유의 사항 (반영된 감점/합격 로직)")
    st.markdown("""
    1. **의미 기반 인정**: 용어가 정확하지 않더라도 조건에서 허용한 핵심 의미가 담겨 있으면 정답 인정.
    2. **선택적 특성 반영**: 특정 대상/가게를 선택해 설명할 경우 해당 가게나 상황의 독자적 특성이 드러나야 함.
    3. **오개념 방지 규칙**: 한 개념이나 사건의 특성을 다른 사건/가게의 설명에 혼용·오적용 시 해당 항목 0점 처리.
    4. **결론 방향성 명확화**: 문제에서 요구하는 최종 결론(이기심, 생존 경쟁, 반어적 비판 등)이 문장에 명확히 드러나야 통과.
    """)

# 채점 로직 함수
def grade_item_1(ans_surf1, ans_surf2, ans_root):
    score_surf1 = 0
    score_surf2 = 0
    score_root = 0
    feedback = []

    # 1-1. 표면적 원인 1: 슈퍼 간 할인/경품 경쟁
    kw_super = ["경호", "형제", "임금님", "슈퍼", "가게"]
    kw_comp = ["가격", "할인", "싸게", "경품", "덤", "제살", "깎기", "세일", "출혈"]
    
    has_super = any(k in ans_surf1 for k in kw_super)
    has_comp = any(k in ans_surf1 for k in kw_surf1)
    
    if has_comp:
        if "싱싱" in ans_surf1 and not has_super:
            feedback.append("❌ [표면 원인 1] 싱싱청과물은 영역 침범이 원인입니다. 슈퍼 간 가격 경쟁 특성과 혼동되어 0점 처리되었습니다.")
        else:
            score_surf1 = 2
            feedback.append("✅ [표면 원인 1] 슈퍼 간 과도한 가격/경품 경쟁 원인을 올바르게 기술했습니다. (2점)")
    else:
        feedback.append("⚠️ [표면 원인 1] 슈퍼 간의 가격 깎기나 경품 경쟁에 대한 핵심 설명이 부족합니다. (0점)")

    # 1-2. 표면적 원인 2: 싱싱청과물의 진입 및 영역 침범
    kw_sing = ["싱싱", "청과", "새로", "신규", "야채", "과일"]
    kw_encroach = ["침범", "영역", "들어옴", "차림", "시작", "중복", "위협", "업종"]
    
    has_sing = any(k in ans_surf2 for k in kw_sing)
    has_enc = any(k in ans_surf2 for k in kw_encroach)
    
    if has_sing or has_enc:
        score_surf2 = 2
        feedback.append("✅ [표면 원인 2] 싱싱청과물의 진입 및 영역 침범 원인을 올바르게 기술했습니다. (2점)")
    else:
        feedback.append("⚠️ [표면 원인 2] 새로 생긴 싱싱청과물의 영역 침범 관련 내용이 누락되었습니다. (0점)")

    # 1-3. 근본적 원인: 각박한 현실, 생존 경쟁, 이기심
    kw_root_cause = ["생존", "먹고살", "경쟁", "각박", "현실", "변두리", "가난", "빈곤"]
    kw_root_result = ["이기", "속물", "정", "양심", "인간성", "돈", "이익"]
    
    has_cause = any(k in ans_root for k in kw_root_cause)
    has_result = any(k in ans_root for k in kw_root_result)
    
    # 한 문장 조건 체크
    is_single_sentence = len([s for s in re.split(r'[.!?]+', ans_root.strip()) if s]) <= 1
    
    if has_cause and has_result:
        if is_single_sentence:
            score_root = 3
            feedback.append("✅ [근본 원인] 각박한 현실과 소시민적 이기심을 한 문장으로 명확히 서술했습니다. (3점)")
        else:
            score_root = 2
            feedback.append("⚠️ [근본 원인] 내용은 적절하나 '한 문장으로 서술' 조건을 준수하지 않아 감점되었습니다. (2점)")
    elif has_result or has_cause:
        score_root = 1
        feedback.append("⚠️ [근본 원인] 현실적 여건 또는 이기심/속물성 중 일부만 표현되어 결론이 다소 불분명합니다. (1점)")
    else:
        feedback.append("❌ [근본 원인] 각박한 생존 환경이나 이기심에 대한 근본 원인 서술이 부족합니다. (0점)")

    return score_surf1 + score_surf2 + score_root, feedback


def grade_item_2(ans_title, ans_theme):
    score_title = 0
    score_theme = 0
    feedback = []

    # 2-1. 제목의 반어성 및 유래
    kw_origin = ["성경", "기도", "최소