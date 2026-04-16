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

.stApp {
    background: #FAFAFA;
}

/* ─── 다크모드: 배경도 어둡게 ─── */
@media (prefers-color-scheme: dark) {
    .stApp { background: #1E1E1E !important; }
    .stForm { background: #2D2D2D !important; border-color: #444 !important; }
    .stExpander, [data-testid="stExpander"] { background: #2D2D2D !important; border-color: #444 !important; }
    .stTabs [data-baseweb="tab-panel"] { background: #2D2D2D !important; }
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] { background: #2D2D2D !important; border-color: #444 !important; }
    .stAlert { background: #2D2D2D !important; }
    .code-card-code { background: #2D2D2D !important; border-color: #444 !important; border-left-color: #4CAF50 !important; }
}

/* ─── 메인 타이틀 ─── */
.main-title {
    font-family: 'Gaegu', cursive;
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
    padding: 0.8rem 0 0.3rem;
    color: #333333;
}
.sub-title {
    text-align: center;
    color: #888888;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}

/* ─── 공지 카드 ─── */
.notice-card {
    background: #FFFFFF;
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 0.8rem;
    border: 1px solid #E8E8E8;
    border-left: 4px solid #FF9800;
}
.notice-card h4 {
    margin: 0 0 0.4rem 0;
    font-weight: 700;
    font-size: 1rem;
    color: #333333;
}
.notice-card p {
    margin: 0;
    font-size: 0.9rem;
    color: #555555;
    line-height: 1.6;
}
.notice-date {
    font-size: 0.75rem;
    color: #AAAAAA;
    margin-top: 0.5rem;
}

/* ─── 개인 코드 카드 ─── */
.code-card {
    background: #FFFFFF;
    border-left: 4px solid #4CAF50;
    padding: 1.1rem 1.3rem;
    border-radius: 0 10px 10px 0;
    margin-bottom: 0.8rem;
    border: 1px solid #E8E8E8;
    border-left: 4px solid #4CAF50;
}
.code-card h4 {
    margin: 0 0 0.4rem 0;
    font-weight: 600;
    color: #333333;
    font-size: 1rem;
}

/* ─── 코드 블록 ─── */
.code-block {
    background: #2D2D2D;
    color: #E0E0E0;
    padding: 0.9rem 1.1rem;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 0.88rem;
    margin-top: 0.5rem;
    word-break: break-all;
    white-space: pre-wrap;
}

/* ─── 통계 박스 ─── */
.stat-box {
    background: #FFFFFF;
    padding: 1.2rem;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #E8E8E8;
}
.stat-box h2 {
    margin: 0;
    color: #FF9800;
    font-size: 1.8rem;
    font-weight: 900;
}
.stat-box p {
    margin: 0.2rem 0 0;
    font-size: 0.85rem;
    color: #888888;
}

/* ─── 비밀번호 초기화 배너 ─── */
.reset-banner {
    background: #FFF8E1;
    border: 1px solid #FFE082;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
    color: #333333;
}

/* ─── 웰컴 배너 ─── */
.welcome-banner {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    text-align: center;
    margin-bottom: 1rem;
    border: 1px solid #E8E8E8;
}
.welcome-banner h3 {
    margin: 0;
    color: #333333;
    font-family: 'Gaegu', cursive;
    font-size: 1.15rem;
}
.welcome-banner p {
    margin: 0.1rem 0 0;
    color: #888888;
    font-size: 0.82rem;
}

/* ─── 버튼 ─── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* ─── 폼 ─── */
.stForm {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid #E8E8E8;
}

/* ─── Expander / 탭 패널 흰색 ─── */
.stExpander, [data-testid="stExpander"] {
    background: #FFFFFF !important;
    border-radius: 10px !important;
    border: 1px solid #E8E8E8 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #FFFFFF;
    border-radius: 0 0 10px 10px;
    padding: 1rem;
}
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border-radius: 10px;
    border: 1px solid #E8E8E8;
}
.stAlert {
    background: #FFFFFF !important;
    border-radius: 8px !important;
}

/* ─── 코드 카드 내 코드 영역 ─── */
.code-card-code {
    border-left: 4px solid #4CAF50;
    border-right: 1px solid #E8E8E8;
    background: #FFFFFF;
    padding: 0 1.3rem;
    margin-top: -1rem;
}

/* ─── 코드 복사 버튼 항상 표시 ─── */
[data-testid="stCode"] button,
[data-testid="stCodeBlock"] button,
.stCode button,
.stCodeBlock button,
pre + div button,
[class*="Code"] button {
    opacity: 1 !important;
    visibility: visible !important;
    display: flex !important;
}

/* ─── 반응형 ─── */
@media (max-width: 768px) {
    .main-title {
        font-size: 1.8rem;
    }
}

/* ─── 다크모드 대응 ─── */
@media (prefers-color-scheme: dark) {
    .main-title { color: #F0F0F0; }
    .sub-title { color: #AAAAAA; }
    .notice-card { background: #2D2D2D; border-color: #444; }
    .notice-card h4 { color: #F0F0F0; }
    .notice-card p { color: #CCCCCC; }
    .code-card { background: #2D2D2D; border-color: #444; }
    .code-card h4 { color: #F0F0F0; }
    .code-card p { color: #CCCCCC; }
    .stat-box { background: #2D2D2D; border-color: #444; }
    .stat-box p { color: #AAAAAA; }
    .welcome-banner { background: #2D2D2D; border-color: #444; }
    .welcome-banner h3 { color: #F0F0F0; }
    .welcome-banner p { color: #AAAAAA; }
    .reset-banner { background: #3D3520; border-color: #665520; color: #F0F0F0; }
    .notice-date { color: #999999; }
}

/* Streamlit 다크모드 테마 감지 */
[data-testid="stAppViewContainer"][data-theme="dark"] .main-title,
.stApp[data-theme="dark"] .main-title { color: #F0F0F0; }
[data-testid="stAppViewContainer"][data-theme="dark"] .sub-title,
.stApp[data-theme="dark"] .sub-title { color: #AAAAAA; }
[data-testid="stAppViewContainer"][data-theme="dark"] .notice-card,
.stApp[data-theme="dark"] .notice-card { background: #2D2D2D; border-color: #444; }
[data-testid="stAppViewContainer"][data-theme="dark"] .notice-card h4,
.stApp[data-theme="dark"] .notice-card h4 { color: #F0F0F0; }
[data-testid="stAppViewContainer"][data-theme="dark"] .notice-card p,
.stApp[data-theme="dark"] .notice-card p { color: #CCCCCC; }
[data-testid="stAppViewContainer"][data-theme="dark"] .code-card,
.stApp[data-theme="dark"] .code-card { background: #2D2D2D; border-color: #444; }
[data-testid="stAppViewContainer"][data-theme="dark"] .code-card h4,
.stApp[data-theme="dark"] .code-card h4 { color: #F0F0F0; }
[data-testid="stAppViewContainer"][data-theme="dark"] .code-card p,
.stApp[data-theme="dark"] .code-card p { color: #CCCCCC; }
[data-testid="stAppViewContainer"][data-theme="dark"] .stat-box,
.stApp[data-theme="dark"] .stat-box { background: #2D2D2D; border-color: #444; }
[data-testid="stAppViewContainer"][data-theme="dark"] .stat-box p,
.stApp[data-theme="dark"] .stat-box p { color: #AAAAAA; }
[data-testid="stAppViewContainer"][data-theme="dark"] .welcome-banner,
.stApp[data-theme="dark"] .welcome-banner { background: #2D2D2D; border-color: #444; }
[data-testid="stAppViewContainer"][data-theme="dark"] .welcome-banner h3,
.stApp[data-theme="dark"] .welcome-banner h3 { color: #F0F0F0; }
[data-testid="stAppViewContainer"][data-theme="dark"] .welcome-banner p,
.stApp[data-theme="dark"] .welcome-banner p { color: #AAAAAA; }
[data-testid="stAppViewContainer"][data-theme="dark"] .reset-banner,
.stApp[data-theme="dark"] .reset-banner { background: #3D3520; border-color: #665520; color: #F0F0F0; }
</style>
""", unsafe_allow_html=True)

# ─── 세션 토큰으로 로그인 유지 ───
import secrets as _secrets

def _generate_token():
    return _secrets.token_hex(16)

def _save_token(user_id, token):
    """Supabase에 토큰 저장"""
    # 기존 토큰 삭제 후 새로 저장
    supabase.table("sessions").upsert({
        "user_id": user_id,
        "token": token
    }, on_conflict="user_id").execute()

def _get_user_by_token(token):
    """토큰으로 유저 조회"""
    result = supabase.table("sessions").select("user_id").eq("token", token).execute()
    if not result.data:
        return None, None
    stored_user_id = result.data[0]["user_id"]
    
    # 관리자 체크
    if stored_user_id == "admin":
        return {"name": "관리자", "user_id": "admin"}, "admin"
    
    # 교사 조회
    teacher = supabase.table("teachers").select("*").eq("user_id", stored_user_id).execute()
    if teacher.data:
        return teacher.data[0], "teacher"
    
    # 학생 조회
    student = supabase.table("students").select("*").eq("user_id", stored_user_id).execute()
    if student.data:
        return student.data[0], "student"
    return None, None

def _delete_token(user_id):
    """로그아웃 시 토큰 삭제"""
    supabase.table("sessions").delete().eq("user_id", user_id).execute()

# ─── 세션 초기화 (토큰 기반 자동 로그인) ───
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

    # URL에 토큰이 있으면 자동 로그인 시도
    params = st.query_params
    token = params.get("token")
    if token:
        user, role = _get_user_by_token(token)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.session_state.role = role
            st.session_state.token = token

# ─── 관리자 비밀번호 (secrets에서 가져옴) ───
ADMIN_ID = "admin"

def get_admin_pw_hash():
    return hash_pw(st.secrets.get("ADMIN_PASSWORD", "teacher1234"))

def do_logout():
    """로그아웃 처리"""
    if st.session_state.user:
        _delete_token(st.session_state.user.get("user_id", ""))
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.token = None
    st.query_params.clear()
    st.rerun()


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
#  교사 가입
# ═══════════════════════════════════════
def page_teacher_register():
    st.markdown('<div class="main-title">🏫 천안오성고 1학년 알림장</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">선생님 가입</div>', unsafe_allow_html=True)

    with st.form("teacher_register_form"):
        invite_code = st.text_input("초대 코드")
        name = st.text_input("이름")
        user_id = st.text_input("아이디 (영문/숫자)")
        password = st.text_input("비밀번호", type="password")
        password_confirm = st.text_input("비밀번호 확인", type="password")
        submitted = st.form_submit_button("가입하기", use_container_width=True)

    if submitted:
        # 초대 코드 확인
        correct_code = st.secrets.get("TEACHER_INVITE_CODE", "osung2026")
        if invite_code != correct_code:
            st.error("초대 코드가 올바르지 않습니다.")
            return
        if not all([name, user_id, password, password_confirm]):
            st.error("모든 항목을 입력해주세요.")
            return
        if password != password_confirm:
            st.error("비밀번호가 일치하지 않습니다.")
            return
        if len(password) < 4:
            st.error("비밀번호는 4자 이상으로 설정해주세요.")
            return

        # 아이디 중복 확인 (교사 테이블)
        dup = supabase.table("teachers").select("id").eq("user_id", user_id).execute()
        if dup.data:
            st.error("이미 사용 중인 아이디입니다.")
            return

        # 학생 아이디와도 중복 확인
        dup2 = supabase.table("students").select("id").eq("user_id", user_id).execute()
        if dup2.data:
            st.error("이미 사용 중인 아이디입니다.")
            return

        supabase.table("teachers").insert({
            "user_id": user_id,
            "password_hash": hash_pw(password),
            "name": name,
            "created_at": datetime.now().isoformat()
        }).execute()

        st.success(f"🎉 {name} 선생님, 가입 완료! 아이디 **{user_id}** 로 로그인하세요.")


# ═══════════════════════════════════════
#  로그인
# ═══════════════════════════════════════
def page_login():
    st.markdown('<div class="main-title">🏫 천안오성고 1학년 알림장</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">로그인</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        user_id = st.text_input("학번(학생) 또는 아이디(교사)")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인", use_container_width=True)

    if submitted:
        if not user_id or not password:
            st.error("학번/아이디와 비밀번호를 입력해주세요.")
            return

        # 관리자 로그인
        if user_id == ADMIN_ID and hash_pw(password) == get_admin_pw_hash():
            token = _generate_token()
            _save_token("admin", token)
            st.session_state.logged_in = True
            st.session_state.user = {"name": "관리자", "user_id": "admin"}
            st.session_state.role = "admin"
            st.session_state.token = token
            st.query_params["token"] = token
            st.rerun()
            return

        # 교사 로그인
        teacher_result = (supabase.table("teachers")
                          .select("*")
                          .eq("user_id", user_id)
                          .eq("password_hash", hash_pw(password))
                          .execute())
        if teacher_result.data:
            token = _generate_token()
            _save_token(user_id, token)
            st.session_state.logged_in = True
            st.session_state.user = teacher_result.data[0]
            st.session_state.role = "teacher"
            st.session_state.token = token
            st.query_params["token"] = token
            st.rerun()
            return

        # 학생 로그인
        result = (supabase.table("students")
                  .select("*")
                  .eq("user_id", user_id)
                  .eq("password_hash", hash_pw(password))
                  .execute())
        if result.data:
            token = _generate_token()
            _save_token(user_id, token)
            st.session_state.logged_in = True
            st.session_state.user = result.data[0]
            st.session_state.role = "student"
            st.session_state.token = token
            st.query_params["token"] = token
            st.rerun()
        else:
            st.error("학번/아이디 또는 비밀번호가 올바르지 않습니다.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("처음이에요 (비밀번호 설정)", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
    with col2:
        if st.button("선생님 가입", use_container_width=True):
            st.session_state.page = "teacher_register"
            st.rerun()


# ═══════════════════════════════════════
#  학생 대시보드
# ═══════════════════════════════════════
def page_student_dashboard():
    user = st.session_state.user
    grade = user["grade"]
    class_num = user["class_num"]

    # 헤더
    st.markdown(f'<div class="main-title">🏫 천안오성고 1학년 알림장</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="welcome-banner">
        <p>{grade}학년 {class_num}반 {user["student_num"]}번</p>
        <h3>👋 {user["name"]}님, 반가워요!</h3>
    </div>
    """, unsafe_allow_html=True)

    col_tabs, col_logout = st.columns([5, 1])
    with col_logout:
        if st.button("로그아웃", use_container_width=True, key="logout_student"):
            do_logout()

    tab1, tab2, tab3 = st.tabs(["🔐 내 개인 코드", "📢 전체 공지", "⚙️ 내 정보"])

    # ── 개인 코드/메시지 ──
    with tab1:
        messages = (supabase.table("personal_messages")
                    .select("*")
                    .eq("grade", grade)
                    .eq("class_num", class_num)
                    .eq("student_num", user["student_num"])
                    .order("created_at", desc=True)
                    .limit(20)
                    .execute())
        if messages.data:
            for idx, m in enumerate(messages.data):
                date_str = m["created_at"][:10] if m.get("created_at") else ""
                content_html = f"""
                <div class="code-card" style="margin-bottom:0; border-radius:0 10px 0 0; border-bottom:none;">
                    <h4>💌 {m['title']}</h4>
                """
                if m.get("message"):
                    content_html += f"<p>{m['message']}</p>"
                content_html += "</div>"
                st.markdown(content_html, unsafe_allow_html=True)
                if m.get("code"):
                    st.markdown('<div class="code-card-code">', unsafe_allow_html=True)
                    st.code(m["code"], language=None)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="code-card" style="margin-top:0; border-radius:0 0 10px 0; border-top:none; padding-top:0;">
                    <div class="notice-date" style="color:#999;">{date_str}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("아직 받은 개인 코드/메시지가 없습니다.")

    # ── 전체 공지 ──
    with tab2:
        notices = (supabase.table("notices")
                   .select("*")
                   .order("created_at", desc=True)
                   .limit(20)
                   .execute())
        if notices.data:
            for n in notices.data:
                date_str = n["created_at"][:10] if n.get("created_at") else ""
                author = n.get("author", "")
                author_tag = f" | {author}" if author else ""
                st.markdown(f"""
                <div class="notice-card">
                    <h4>📌 {n['title']}</h4>
                    <p>{n['content']}</p>
                    <div class="notice-date">{date_str}{author_tag}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("아직 공지가 없습니다.")

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
    if st.session_state.role == "teacher":
        display_name = st.session_state.user.get("name", "선생님")
        st.markdown(f'<div class="main-title">😊 {display_name} 선생님</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-title">⚙️ 관리자 페이지</div>', unsafe_allow_html=True)

    # 탭 + 로그아웃을 같은 줄에
    col_tabs, col_logout = st.columns([5, 1])
    with col_logout:
        if st.button("로그아웃", use_container_width=True, key="logout_admin"):
            do_logout()

    # 세션 메시지 표시 제거 (탭 안에서 표시)

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
            author = st.session_state.user.get("name", "관리자")
            supabase.table("notices").insert({
                "title": title,
                "content": content,
                "author": author,
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
                author = n.get("author", "")
                author_tag = f" - {author}" if author else ""
                with st.expander(f"📌 {n['title']} ({date_str}{author_tag})"):
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

        # CSV/엑셀 일괄 전송 기능
        st.markdown("---")
        st.subheader("📦 파일로 일괄 전송")
        st.caption("CSV 또는 엑셀(xlsx) 파일을 업로드하면 학생별로 개인 코드를 자동 저장합니다.")

        with st.expander("📄 파일 양식 보기 / 양식 다운로드"):
            st.markdown("""
            파일에 아래 열을 포함해주세요:
            
            | 학년 | 반 | 번호 | 코드 |
            |------|-----|------|------|
            | 1 | 7 | 1 | ABC123 |
            | 1 | 7 | 2 | DEF456 |
            
            - **첫 줄은 헤더**: `학년,반,번호,코드`
            - **메시지 열 추가 가능**: `학년,반,번호,코드,메시지`
            """)
            # CSV 양식 다운로드
            import pandas as pd
            template_df = pd.DataFrame({
                "학년": [1, 1, 1],
                "반": [1, 1, 1],
                "번호": [1, 2, 3],
                "코드": ["코드입력", "코드입력", "코드입력"],
                "메시지": ["", "", ""]
            })
            csv_template = template_df.to_csv(index=False).encode("utf-8-sig")
            st.download_button("📥 CSV 양식 다운로드", csv_template, "코드전송_양식.csv", "text/csv", use_container_width=True)

        with st.form("csv_bulk_form"):
            csv_title = st.text_input("전송 제목", key="csv_title", placeholder="예: 개인 인증코드")
            csv_message = st.text_area("공통 메시지 (선택)", key="csv_msg", placeholder="예: 아래 코드를 사용하세요.")
            csv_file = st.file_uploader("파일 업로드", type=["csv", "xlsx", "xls"], key="csv_upload")
            csv_submit = st.form_submit_button("일괄 전송", use_container_width=True)

        if csv_submit and csv_title and csv_file:
            import pandas as pd
            import io
            try:
                file_name = csv_file.name.lower()
                if file_name.endswith((".xlsx", ".xls")):
                    df = pd.read_excel(csv_file)
                else:
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
        
        # 고유 제목 목록 가져오기
        all_titles_raw = (supabase.table("personal_messages")
                          .select("title")
                          .order("created_at", desc=True)
                          .execute())
        
        if all_titles_raw.data:
            # 중복 제거하면서 순서 유지
            seen = set()
            unique_titles = []
            for row in all_titles_raw.data:
                t = row["title"]
                if t not in seen:
                    seen.add(t)
                    unique_titles.append(t)

            for title_name in unique_titles:
                # 해당 제목의 메시지 전체 가져오기
                title_msgs = (supabase.table("personal_messages")
                              .select("*")
                              .eq("title", title_name)
                              .order("grade")
                              .order("class_num")
                              .order("student_num")
                              .execute())
                
                if not title_msgs.data:
                    continue
                
                msgs = title_msgs.data
                first_msg = msgs[0]
                date_display = first_msg["created_at"][:10] if first_msg.get("created_at") else ""
                label = f"📦 {title_name} ({date_display}) — {len(msgs)}명"
                
                with st.expander(label):
                    # 반별로 묶어서 보여주기
                    from itertools import groupby
                    sorted_msgs = sorted(msgs, key=lambda x: (x['grade'], x['class_num'], x['student_num']))
                    
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
                    group_id = first_msg['id'][:8]
                    with st.form(f"edit_group_{group_id}"):
                        edit_title = st.text_input("제목 (일괄 수정)", value=title_name, key=f"gt_{group_id}")
                        edit_message = st.text_area("공통 메시지 (일괄 수정)", value=first_msg.get("message", ""), key=f"gm_{group_id}")
                        col_save, col_del = st.columns(2)
                        with col_save:
                            save = st.form_submit_button("💾 전체 수정", use_container_width=True)
                        with col_del:
                            delete = st.form_submit_button("🗑️ 전체 삭제", use_container_width=True)

                    if save:
                        supabase.table("personal_messages").update({
                            "title": edit_title,
                            "message": edit_message
                        }).eq("title", title_name).execute()
                        st.success(f"✅ {len(msgs)}건 일괄 수정 완료!")
                        st.rerun()
                    if delete:
                        supabase.table("personal_messages").delete().eq("title", title_name).execute()
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
            # 세션 메시지 표시 (비번 초기화 등)
            if st.session_state.get("admin_msg"):
                st.success(st.session_state["admin_msg"])
                del st.session_state["admin_msg"]

            total = len(students.data)
            class_set = set((s['grade'], s['class_num']) for s in students.data)
            class_sorted = sorted(class_set, key=lambda x: (x[0], x[1]))

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="stat-box">
                    <h2>{total}</h2>
                    <p>전체 가입 학생 수</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="stat-box">
                    <h2>{len(class_sorted)}</h2>
                    <p>학급 수</p>
                </div>
                """, unsafe_allow_html=True)

            # 반별 가입 현황
            with st.expander("📊 반별 가입 현황"):
                for g, c in class_sorted:
                    class_students = [s for s in students.data if s['grade'] == g and s['class_num'] == c]
                    registered_nums = sorted([s['student_num'] for s in class_students])
                    st.markdown(f"**{g}-{c}반**: {len(class_students)}명 가입")
                    st.caption(f"  가입: {', '.join(str(n) + '번' for n in registered_nums)}")

            st.markdown("---")

            # 반 선택 필터 (숫자순 정렬)
            class_set = set((s['grade'], s['class_num']) for s in students.data)
            class_sorted = sorted(class_set, key=lambda x: (x[0], x[1]))
            class_list = ["전체"] + [f"{g}-{c}반" for g, c in class_sorted]
            selected_class = st.selectbox("학급 선택", class_list, key="class_filter")

            # 필터링
            if selected_class == "전체":
                filtered = students.data
            else:
                g = int(selected_class.split("-")[0])
                c = int(selected_class.split("-")[1].replace("반", ""))
                filtered = [s for s in students.data if s["grade"] == g and s["class_num"] == c]

            filtered = sorted(filtered, key=lambda x: (x['grade'], x['class_num'], x['student_num']))
            st.caption(f"📋 {len(filtered)}명")

            # 학생 목록 (플랫 리스트)
            for s in filtered:
                pw_status = " 🔴" if s.get("pw_reset") else ""
                col_info, col_manage = st.columns([7, 1])
                with col_info:
                    st.markdown(f"{s['grade']}-{s['class_num']}반 {s['student_num']}번 {s['name']}{pw_status}")
                with col_manage:
                    if st.button("관리", key=f"manage_{s['id']}", use_container_width=True):
                        st.session_state[f"show_edit_{s['id']}"] = not st.session_state.get(f"show_edit_{s['id']}", False)
                        st.rerun()

                # 관리 패널 (버튼 누르면 펼쳐짐)
                if st.session_state.get(f"show_edit_{s['id']}", False):
                    with st.container():
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
                            st.session_state["admin_msg"] = f"🔑 {s['name']} 비밀번호가 학번({s['user_id']})으로 초기화되었습니다. 학생에게 학번으로 로그인 후 비밀번호를 다시 설정하라고 안내해주세요."
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

                    st.markdown("---")
        else:
            st.info("아직 가입한 학생이 없습니다.")


# ═══════════════════════════════════════
#  메인 라우팅
# ═══════════════════════════════════════
def main():
    if st.session_state.logged_in:
        if st.session_state.role in ("admin", "teacher"):
            page_admin_dashboard()
        elif st.session_state.role == "student" and st.session_state.user.get("pw_reset"):
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
        elif page == "teacher_register":
            page_teacher_register()
            st.markdown("---")
            if st.button("← 로그인으로 돌아가기", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        else:
            page_login()

if __name__ == "__main__":
    main()
