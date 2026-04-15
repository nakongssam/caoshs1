import streamlit as st
import hashlib
from datetime import datetime
from supabase import create_client, Client

# ─── 페이지 설정 ───
st.set_page_config(
    page_title="천안오성고 1학년 알림장",
    page_icon="🏫",
    layout="centered"
)

# ─── Supabase 연결 ───
@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()

# ─── 비밀번호 해싱 ───
def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ─── 스타일 ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Gaegu:wght@400;700&display=swap');

/* ─── 전역 스타일 ─── */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* Streamlit 기본 배경 커스텀 */
.stApp {
    background: linear-gradient(180deg, #FFF9F0 0%, #FFF0E6 50%, #FFE8D6 100%);
}

/* ─── 메인 타이틀 ─── */
.main-title {
    font-family: 'Gaegu', cursive;
    font-size: 2.4rem;
    font-weight: 700;
    text-align: center;
    padding: 0.8rem 0 0.3rem;
    color: #5D4037;
    letter-spacing: -0.5px;
}
.sub-title {
    text-align: center;
    color: #8D6E63;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    font-weight: 400;
}

/* ─── 공지 카드 ─── */
.notice-card {
    background: linear-gradient(135deg, #FF9A76 0%, #FFBA92 100%);
    color: white;
    padding: 1.2rem 1.5rem;
    border-radius: 16px;
    margin-bottom: 0.8rem;
    box-shadow: 0 4px 12px rgba(255, 154, 118, 0.25);
    border: 2px solid rgba(255,255,255,0.3);
    transition: transform 0.2s ease;
}
.notice-card:hover {
    transform: translateY(-2px);
}
.notice-card h4 {
    margin: 0 0 0.4rem 0;
    font-weight: 700;
    font-size: 1.05rem;
}
.notice-card p {
    margin: 0;
    font-size: 0.9rem;
    opacity: 0.95;
    line-height: 1.6;
}
.notice-date {
    font-size: 0.75rem;
    opacity: 0.7;
    margin-top: 0.5rem;
}

/* ─── 개인 코드 카드 ─── */
.code-card {
    background: #FFFFFF;
    border-left: 5px solid #FFB74D;
    padding: 1.1rem 1.3rem;
    border-radius: 0 14px 14px 0;
    margin-bottom: 0.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: transform 0.2s ease;
}
.code-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.code-card h4 {
    margin: 0 0 0.4rem 0;
    font-weight: 600;
    color: #5D4037;
    font-size: 1rem;
}

/* ─── 코드 블록 ─── */
.code-block {
    background: linear-gradient(135deg, #5D4037 0%, #4E342E 100%);
    color: #FFE0B2;
    padding: 0.9rem 1.1rem;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    font-size: 0.88rem;
    margin-top: 0.5rem;
    word-break: break-all;
    white-space: pre-wrap;
    border: 1px solid rgba(255,224,178,0.2);
}

/* ─── 통계 박스 ─── */
.stat-box {
    background: #FFFFFF;
    padding: 1.2rem;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border: 2px solid #FFE0B2;
}
.stat-box h2 {
    margin: 0;
    color: #FF8A65;
    font-size: 1.8rem;
    font-weight: 900;
}
.stat-box p {
    margin: 0.2rem 0 0;
    font-size: 0.85rem;
    color: #8D6E63;
}

/* ─── 비밀번호 초기화 배너 ─── */
.reset-banner {
    background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
    border: 2px solid #FFB74D;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
    color: #5D4037;
}

/* ─── 웰컴 배너 ─── */
.welcome-banner {
    background: linear-gradient(135deg, #FFE0B2 0%, #FFCC80 100%);
    border-radius: 12px;
    padding: 0.7rem 1rem;
    text-align: center;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.5);
}
.welcome-banner h3 {
    margin: 0;
    color: #5D4037;
    font-family: 'Gaegu', cursive;
    font-size: 1.15rem;
}
.welcome-banner p {
    margin: 0.1rem 0 0;
    color: #6D4C41;
    font-size: 0.82rem;
}

/* ─── Streamlit 버튼 커스텀 ─── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* ─── Streamlit 폼 커스텀 ─── */
.stForm {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 1px solid #FFE0B2;
}

/* ─── 탭 커스텀 ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    font-weight: 600;
    font-size: 0.9rem;
}

/* ─── Expander 커스텀 ─── */
.streamlit-expanderHeader {
    font-weight: 600;
    font-size: 0.95rem;
    border-radius: 10px;
}

/* ─── 반응형 (모바일) ─── */
@media (max-width: 768px) {
    .main-title {
        font-size: 1.8rem;
    }
    .notice-card {
        padding: 1rem 1.2rem;
    }
    .code-card {
        padding: 0.9rem 1rem;
    }
    .stat-box h2 {
        font-size: 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ─── 세션 초기화 ───
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# ─── 관리자 비밀번호 (secrets에서 가져옴) ───
ADMIN_ID = "admin"

def get_admin_pw_hash():
    return hash_pw(st.secrets.get("ADMIN_PASSWORD", "teacher1234"))


# ═══════════════════════════════════════
#  회원가입 (비밀번호 설정)
# ═══════════════════════════════════════
def page_register():
    st.markdown('<div class="main-title">🏫 천안오성고 1학년 알림장</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">비밀번호 설정</div>', unsafe_allow_html=True)

    with st.form("register_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            grade = st.number_input("학년", min_value=1, max_value=3, value=1, step=1)
        with col2:
            class_num = st.number_input("반", min_value=1, max_value=20, value=1, step=1)
        with col3:
            student_num = st.number_input("번호", min_value=1, max_value=50, value=1, step=1)
        name = st.text_input("이름")
        password = st.text_input("비밀번호 설정", type="password")
        password_confirm = st.text_input("비밀번호 확인", type="password")
        submitted = st.form_submit_button("가입하기", use_container_width=True)

    if submitted:
        if not all([name, password, password_confirm]):
            st.error("모든 항목을 입력해주세요.")
            return
        if password != password_confirm:
            st.error("비밀번호가 일치하지 않습니다.")
            return
        if len(password) < 4:
            st.error("비밀번호는 4자 이상으로 설정해주세요.")
            return

        user_id = f"{grade}{class_num:02d}{student_num:02d}"

        dup = (supabase.table("students")
               .select("id")
               .eq("grade", grade)
               .eq("class_num", class_num)
               .eq("student_num", student_num)
               .execute())
        if dup.data:
            st.error("이미 가입된 학번입니다. 로그인해주세요.")
            return

        supabase.table("students").insert({
            "user_id": user_id,
            "password_hash": hash_pw(password),
            "name": name,
            "grade": grade,
            "class_num": class_num,
            "student_num": student_num,
            "pw_reset": False,
            "created_at": datetime.now().isoformat()
        }).execute()

        st.success(f"🎉 {name}님, 가입 완료! 학번 **{user_id}** 로 로그인하세요.")


# ═══════════════════════════════════════
#  비밀번호 재설정 페이지 (초기화 후 학생이 새 비번 설정)
# ═══════════════════════════════════════
def page_reset_password():
    user = st.session_state.user
    st.markdown('<div class="main-title">🏫 천안오성고 1학년 알림장</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="reset-banner">
        ⚠️ <strong>비밀번호가 초기화되었습니다.</strong><br>
        새 비밀번호를 설정해주세요.
    </div>
    """, unsafe_allow_html=True)

    with st.form("reset_pw_form"):
        new_pw = st.text_input("새 비밀번호", type="password")
        new_pw_confirm = st.text_input("새 비밀번호 확인", type="password")
        submitted = st.form_submit_button("비밀번호 변경", use_container_width=True)

    if submitted:
        if not new_pw or not new_pw_confirm:
            st.error("비밀번호를 입력해주세요.")
            return
        if new_pw != new_pw_confirm:
            st.error("비밀번호가 일치하지 않습니다.")
            return
        if len(new_pw) < 4:
            st.error("비밀번호는 4자 이상으로 설정해주세요.")
            return

        supabase.table("students").update({
            "password_hash": hash_pw(new_pw),
            "pw_reset": False
        }).eq("id", user["id"]).execute()

        # 세션 업데이트
        st.session_state.user["pw_reset"] = False
        st.success("✅ 비밀번호가 변경되었습니다!")
        st.rerun()


# ═══════════════════════════════════════
#  로그인
# ═══════════════════════════════════════
def page_login():
    st.markdown('<div class="main-title">🏫 천안오성고 1학년 알림장</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">학번과 비밀번호를 입력해주세요</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        user_id = st.text_input("학번 (예: 10101 = 1학년1반1번)")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인", use_container_width=True)

    if submitted:
        if not user_id or not password:
            st.error("학번과 비밀번호를 입력해주세요.")
            return

        # 관리자 로그인
        if user_id == ADMIN_ID and hash_pw(password) == get_admin_pw_hash():
            st.session_state.logged_in = True
            st.session_state.user = {"name": "선생님", "user_id": "admin"}
            st.session_state.role = "admin"
            st.rerun()
            return

        # 학생 로그인
        result = (supabase.table("students")
                  .select("*")
                  .eq("user_id", user_id)
                  .eq("password_hash", hash_pw(password))
                  .execute())
        if result.data:
            st.session_state.logged_in = True
            st.session_state.user = result.data[0]
            st.session_state.role = "student"
            st.rerun()
        else:
            st.error("학번 또는 비밀번호가 올바르지 않습니다.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("처음이에요 (비밀번호 설정)", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
    with col2:
        if st.button("🔑 관리자 로그인", use_container_width=True):
            st.info("위 로그인 폼에서 관리자 아이디/비밀번호를 입력하세요.")


# ═══════════════════════════════════════
#  학생 대시보드
# ═══════════════════════════════════════
def page_student_dashboard():
    user = st.session_state.user
    grade = user["grade"]
    class_num = user["class_num"]

    # 헤더
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="main-title">🏫 천안오성고 1학년 알림장</div>', unsafe_allow_html=True)
    with col2:
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()

    st.markdown(f"""
    <div class="welcome-banner">
        <h3>👋 {user["name"]}님, 반가워요!</h3>
        <p>{grade}학년 {class_num}반 {user["student_num"]}번</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📢 전체 공지", "🔐 내 개인 코드", "⚙️ 내 정보"])

    # ── 전체 공지 ──
    with tab1:
        notices = (supabase.table("notices")
                   .select("*")
                   .order("created_at", desc=True)
                   .limit(20)
                   .execute())
        if notices.data:
            for n in notices.data:
                date_str = n["created_at"][:10] if n.get("created_at") else ""
                st.markdown(f"""
                <div class="notice-card">
                    <h4>📌 {n['title']}</h4>
                    <p>{n['content']}</p>
                    <div class="notice-date">{date_str}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("아직 공지가 없습니다.")

    # ── 개인 코드/메시지 ──
    with tab2:
        messages = (supabase.table("personal_messages")
                    .select("*")
                    .eq("grade", grade)
                    .eq("class_num", class_num)
                    .eq("student_num", user["student_num"])
                    .order("created_at", desc=True)
                    .limit(20)
                    .execute())
        if messages.data:
            for m in messages.data:
                date_str = m["created_at"][:10] if m.get("created_at") else ""
                content_html = f"""
                <div class="code-card">
                    <h4>💌 {m['title']}</h4>
                """
                if m.get("message"):
                    content_html += f"<p>{m['message']}</p>"
                if m.get("code"):
                    content_html += f'<div class="code-block">{m["code"]}</div>'
                content_html += f'<div class="notice-date" style="color:#999; margin-top:0.5rem;">{date_str}</div></div>'
                st.markdown(content_html, unsafe_allow_html=True)
        else:
            st.info("아직 받은 개인 코드/메시지가 없습니다.")

    # ── 내 정보 수정 (4번 기능) ──
    with tab3:
        st.subheader("내 정보 수정")
        with st.form("edit_my_info"):
            new_name = st.text_input("이름", value=user["name"])
            st.caption(f"학번: {user['user_id']} (변경 불가)")
            submitted = st.form_submit_button("정보 수정", use_container_width=True)

        if submitted:
            if not new_name:
                st.error("이름을 입력해주세요.")
            else:
                supabase.table("students").update({
                    "name": new_name
                }).eq("id", user["id"]).execute()
                st.session_state.user["name"] = new_name
                st.success("✅ 정보가 수정되었습니다!")
                st.rerun()

        st.markdown("---")
        st.subheader("비밀번호 변경")
        with st.form("change_pw_form"):
            current_pw = st.text_input("현재 비밀번호", type="password")
            new_pw = st.text_input("새 비밀번호", type="password")
            new_pw_confirm = st.text_input("새 비밀번호 확인", type="password")
            pw_submitted = st.form_submit_button("비밀번호 변경", use_container_width=True)

        if pw_submitted:
            if not all([current_pw, new_pw, new_pw_confirm]):
                st.error("모든 항목을 입력해주세요.")
            elif hash_pw(current_pw) != user["password_hash"]:
                st.error("현재 비밀번호가 올바르지 않습니다.")
            elif new_pw != new_pw_confirm:
                st.error("새 비밀번호가 일치하지 않습니다.")
            elif len(new_pw) < 4:
                st.error("비밀번호는 4자 이상으로 설정해주세요.")
            else:
                supabase.table("students").update({
                    "password_hash": hash_pw(new_pw)
                }).eq("id", user["id"]).execute()
                st.session_state.user["password_hash"] = hash_pw(new_pw)
                st.success("✅ 비밀번호가 변경되었습니다!")


# ═══════════════════════════════════════
#  관리자 대시보드
# ═══════════════════════════════════════
def page_admin_dashboard():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="main-title">⚙️ 관리자 페이지</div>', unsafe_allow_html=True)
    with col2:
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["📢 공지 관리", "💌 개인 메시지", "👥 학생 관리"])

    # ══════════════════════════
    # ── 공지 관리 (수정 가능) ──
    # ══════════════════════════
    with tab1:
        st.subheader("새 공지 작성")
        with st.form("notice_form"):
            title = st.text_input("공지 제목")
            content = st.text_area("공지 내용")
            submitted = st.form_submit_button("공지 등록", use_container_width=True)
        if submitted and title:
            supabase.table("notices").insert({
                "title": title,
                "content": content,
                "created_at": datetime.now().isoformat()
            }).execute()
            st.success("공지가 등록되었습니다!")
            st.rerun()

        st.markdown("---")
        st.subheader("등록된 공지")
        notices = (supabase.table("notices")
                   .select("*")
                   .order("created_at", desc=True)
                   .limit(30)
                   .execute())
        if notices.data:
            for n in notices.data:
                date_str = n["created_at"][:10] if n.get("created_at") else ""
                with st.expander(f"📌 {n['title']} ({date_str})"):
                    with st.form(f"edit_notice_{n['id']}"):
                        edit_title = st.text_input("제목", value=n["title"], key=f"nt_{n['id']}")
                        edit_content = st.text_area("내용", value=n.get("content", ""), key=f"nc_{n['id']}")
                        col_save, col_del = st.columns(2)
                        with col_save:
                            save = st.form_submit_button("💾 수정 저장", use_container_width=True)
                        with col_del:
                            delete = st.form_submit_button("🗑️ 삭제", use_container_width=True)
                    if save:
                        supabase.table("notices").update({
                            "title": edit_title,
                            "content": edit_content
                        }).eq("id", n["id"]).execute()
                        st.success("수정 완료!")
                        st.rerun()
                    if delete:
                        supabase.table("notices").delete().eq("id", n["id"]).execute()
                        st.rerun()

    # ══════════════════════════════════
    # ── 개인 메시지 보내기 (수정 가능) ──
    # ══════════════════════════════════
    with tab2:
        st.subheader("개인 코드/메시지 전송")
        st.caption("학생이 아직 가입하지 않아도 코드를 미리 등록할 수 있습니다.")

        with st.form("personal_msg_form"):
            col_g, col_c, col_n = st.columns(3)
            with col_g:
                msg_grade = st.number_input("학년", min_value=1, max_value=3, value=1, step=1, key="msg_grade")
            with col_c:
                msg_class = st.number_input("반", min_value=1, max_value=20, value=1, step=1, key="msg_class")
            with col_n:
                msg_num = st.number_input("번호", min_value=1, max_value=50, value=1, step=1, key="msg_num")
            msg_title = st.text_input("제목")
            message = st.text_area("메시지 (선택)")
            code = st.text_area("코드/링크 (선택)")
            submitted = st.form_submit_button("전송", use_container_width=True)

        if submitted and msg_title:
            supabase.table("personal_messages").insert({
                "grade": msg_grade,
                "class_num": msg_class,
                "student_num": msg_num,
                "title": msg_title,
                "message": message,
                "code": code,
                "created_at": datetime.now().isoformat()
            }).execute()
            st.success(f"✅ {msg_grade}-{msg_class}반 {msg_num}번에게 전송 완료!")

        # CSV 일괄 전송 기능
        st.markdown("---")
        st.subheader("📦 CSV로 일괄 전송")
        st.caption("CSV 파일을 업로드하면 학생별로 개인 코드를 자동 저장합니다. 학생 가입 전에도 가능!")

        with st.expander("📄 CSV 파일 양식 보기"):
            st.markdown("""
            CSV 파일에 아래 열을 포함해주세요:
            
            | 학년 | 반 | 번호 | 코드 |
            |------|-----|------|------|
            | 1 | 7 | 1 | ABC123 |
            | 1 | 7 | 2 | DEF456 |
            
            - **첫 줄은 헤더**: `학년,반,번호,코드` (또는 영어: `grade,class,number,code`)
            - **메시지 열 추가 가능**: `학년,반,번호,코드,메시지`
            """)

        with st.form("csv_bulk_form"):
            csv_title = st.text_input("전송 제목", key="csv_title", placeholder="예: 4월 개인 인증코드")
            csv_message = st.text_area("공통 메시지 (선택)", key="csv_msg", placeholder="예: 아래 코드를 사용하세요.")
            csv_file = st.file_uploader("CSV 파일 업로드", type=["csv"], key="csv_upload")
            csv_submit = st.form_submit_button("CSV로 일괄 전송", use_container_width=True)

        if csv_submit and csv_title and csv_file:
            import pandas as pd
            import io
            try:
                raw = csv_file.read()
                for enc in ["utf-8-sig", "utf-8", "euc-kr", "cp949"]:
                    try:
                        text = raw.decode(enc)
                        break
                    except (UnicodeDecodeError, LookupError):
                        continue
                else:
                    text = raw.decode("utf-8", errors="replace")
                df = pd.read_csv(io.StringIO(text))
                col_map = {
                    "학년": "grade", "반": "class", "번호": "number", "코드": "code", "메시지": "message",
                    "class_num": "class", "student_num": "number",
                }
                df.columns = [col_map.get(c.strip(), c.strip().lower()) for c in df.columns]

                required = ["grade", "class", "number", "code"]
                missing = [c for c in required if c not in df.columns]
                if missing:
                    st.error(f"CSV에 필수 열이 없습니다: {missing}")
                else:
                    rows_to_insert = []
                    for _, row in df.iterrows():
                        msg_val = str(row.get("message", "")) if "message" in df.columns else ""
                        rows_to_insert.append({
                            "grade": int(row["grade"]),
                            "class_num": int(row["class"]),
                            "student_num": int(row["number"]),
                            "title": csv_title,
                            "message": csv_message + ("\n" + msg_val if msg_val else ""),
                            "code": str(row["code"]),
                            "created_at": datetime.now().isoformat()
                        })

                    if rows_to_insert:
                        supabase.table("personal_messages").insert(rows_to_insert).execute()
                        st.success(f"✅ {len(rows_to_insert)}명에게 전송 완료!")

            except Exception as e:
                st.error(f"CSV 처리 중 오류: {e}")

        # 보낸 메시지 목록 (그룹별 관리)
        st.markdown("---")
        st.subheader("📋 보낸 메시지 관리")
        all_msgs = (supabase.table("personal_messages")
                    .select("*")
                    .order("created_at", desc=True)
                    .limit(500)
                    .execute())
        if all_msgs.data:
            # 같은 제목 + 같은 시간(분 단위)으로 그룹핑
            from collections import OrderedDict
            groups = OrderedDict()
            for m in all_msgs.data:
                # 분 단위까지 잘라서 같은 시점에 보낸 것끼리 묶기
                time_key = m["created_at"][:16] if m.get("created_at") else ""
                group_key = f"{m['title']}||{time_key}"
                if group_key not in groups:
                    groups[group_key] = []
                groups[group_key].append(m)

            for group_key, msgs in groups.items():
                title_part, time_part = group_key.split("||")
                date_display = time_part[:10] if time_part else ""
                label = f"📦 {title_part} ({date_display}) — {len(msgs)}명"
                with st.expander(label):
                    # 대상 목록을 반별로 정리
                    sorted_msgs = sorted(msgs, key=lambda x: (x['grade'], x['class_num'], x['student_num']))
                    
                    # 반별로 묶어서 보여주기
                    from itertools import groupby
                    st.markdown("**📌 대상:**")
                    for cls_key, cls_msgs in groupby(sorted_msgs, key=lambda x: f"{x['grade']}-{x['class_num']}반"):
                        cls_list = list(cls_msgs)
                        nums = ", ".join(str(m['student_num']) + "번" for m in cls_list)
                        st.caption(f"  {cls_key}: {nums}")

                    # 개별 코드 미리보기
                    with st.expander("👀 개인별 코드 확인", expanded=False):
                        for m in sorted_msgs:
                            code_preview = m.get('code', '-') or '-'
                            st.text(f"{m['grade']}-{m['class_num']}반 {m['student_num']}번: {code_preview}")

                    # 일괄 수정 폼
                    first_msg = msgs[0]
                    group_id = first_msg['id'][:8]
                    with st.form(f"edit_group_{group_id}"):
                        edit_title = st.text_input("제목 (일괄 수정)", value=title_part, key=f"gt_{group_id}")
                        edit_message = st.text_area("공통 메시지 (일괄 수정)", value=first_msg.get("message", ""), key=f"gm_{group_id}")
                        col_save, col_del = st.columns(2)
                        with col_save:
                            save = st.form_submit_button("💾 전체 수정", use_container_width=True)
                        with col_del:
                            delete = st.form_submit_button("🗑️ 전체 삭제", use_container_width=True)

                    if save:
                        for m in msgs:
                            supabase.table("personal_messages").update({
                                "title": edit_title,
                                "message": edit_message
                            }).eq("id", m["id"]).execute()
                        st.success(f"✅ {len(msgs)}건 일괄 수정 완료!")
                        st.rerun()
                    if delete:
                        for m in msgs:
                            supabase.table("personal_messages").delete().eq("id", m["id"]).execute()
                        st.success(f"🗑️ {len(msgs)}건 일괄 삭제 완료!")
                        st.rerun()

    # ══════════════════════════════════════
    # ── 학생 관리 (비번 초기화 + 정보 수정) ──
    # ══════════════════════════════════════
    with tab3:
        students = (supabase.table("students")
                    .select("*")
                    .order("grade")
                    .order("class_num")
                    .order("student_num")
                    .execute())

        # 통계
        if students.data:
            total = len(students.data)
            classes = set(f"{s['grade']}-{s['class_num']}" for s in students.data)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="stat-box">
                    <h2>{total}</h2>
                    <p>전체 학생 수</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="stat-box">
                    <h2>{len(classes)}</h2>
                    <p>학급 수</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # 학생 목록
            for s in students.data:
                pw_status = " 🔴초기화됨" if s.get("pw_reset") else ""
                label = f"{s['grade']}-{s['class_num']}반 {s['student_num']}번 {s['name']} (학번: {s['user_id']}){pw_status}"
                with st.expander(label):
                    # 정보 수정 폼
                    with st.form(f"edit_student_{s['id']}"):
                        edit_name = st.text_input("이름", value=s["name"], key=f"sn_{s['id']}")
                        col_g, col_c, col_n = st.columns(3)
                        with col_g:
                            edit_grade = st.number_input("학년", min_value=1, max_value=3, value=s["grade"], key=f"sg_{s['id']}")
                        with col_c:
                            edit_class = st.number_input("반", min_value=1, max_value=20, value=s["class_num"], key=f"sc_{s['id']}")
                        with col_n:
                            edit_num = st.number_input("번호", min_value=1, max_value=50, value=s["student_num"], key=f"snum_{s['id']}")

                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            save_info = st.form_submit_button("💾 정보 수정", use_container_width=True)
                        with col_b:
                            reset_pw = st.form_submit_button("🔑 비번 초기화", use_container_width=True)
                        with col_c:
                            delete_student = st.form_submit_button("🗑️ 삭제", use_container_width=True)

                    if save_info:
                        new_user_id = f"{edit_grade}{edit_class:02d}{edit_num:02d}"
                        supabase.table("students").update({
                            "name": edit_name,
                            "grade": edit_grade,
                            "class_num": edit_class,
                            "student_num": edit_num,
                            "user_id": new_user_id
                        }).eq("id", s["id"]).execute()
                        st.success(f"✅ {edit_name} 정보 수정 완료! (새 학번: {new_user_id})")
                        st.rerun()

                    if reset_pw:
                        supabase.table("students").update({
                            "password_hash": hash_pw(s["user_id"]),
                            "pw_reset": True
                        }).eq("id", s["id"]).execute()
                        st.success(f"🔑 {s['name']} 비밀번호가 학번({s['user_id']})으로 초기화되었습니다! 학생이 로그인하면 새 비밀번호를 설정하게 됩니다.")
                        st.rerun()

                    if delete_student:
                        (supabase.table("personal_messages")
                         .delete()
                         .eq("grade", s["grade"])
                         .eq("class_num", s["class_num"])
                         .eq("student_num", s["student_num"])
                         .execute())
                        supabase.table("students").delete().eq("id", s["id"]).execute()
                        st.success(f"🗑️ {s['name']} 삭제 완료")
                        st.rerun()
        else:
            st.info("아직 가입한 학생이 없습니다.")


# ═══════════════════════════════════════
#  메인 라우팅
# ═══════════════════════════════════════
def main():
    if st.session_state.logged_in:
        if st.session_state.role == "admin":
            page_admin_dashboard()
        elif st.session_state.role == "student" and st.session_state.user.get("pw_reset"):
            # 비밀번호 초기화 상태면 재설정 페이지로
            page_reset_password()
        else:
            page_student_dashboard()
    else:
        page = st.session_state.get("page", "login")
        if page == "register":
            page_register()
            st.markdown("---")
            if st.button("← 로그인으로 돌아가기", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        else:
            page_login()

if __name__ == "__main__":
    main()
