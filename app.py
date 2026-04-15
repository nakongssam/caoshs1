import streamlit as st
import hashlib
from datetime import datetime
from supabase import create_client, Client

# ─── 페이지 설정 ───
st.set_page_config(
    page_title="우리반 알림장",
    page_icon="📋",
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
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.main-title {
    font-size: 2rem;
    font-weight: 900;
    text-align: center;
    padding: 1rem 0 0.5rem;
    color: #1a1a2e;
}
.sub-title {
    text-align: center;
    color: #6c757d;
    font-size: 0.95rem;
    margin-bottom: 2rem;
}
.notice-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 0.8rem;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}
.notice-card h4 {
    margin: 0 0 0.3rem 0;
    font-weight: 700;
}
.notice-card p {
    margin: 0;
    font-size: 0.9rem;
    opacity: 0.9;
}
.notice-date {
    font-size: 0.75rem;
    opacity: 0.7;
    margin-top: 0.5rem;
}
.code-card {
    background: #f8f9fa;
    border-left: 4px solid #667eea;
    padding: 1rem 1.2rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 0.8rem;
}
.code-card h4 {
    margin: 0 0 0.3rem 0;
    font-weight: 600;
    color: #1a1a2e;
}
.code-block {
    background: #1a1a2e;
    color: #a5d6a7;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    margin-top: 0.5rem;
    word-break: break-all;
    white-space: pre-wrap;
}
.stat-box {
    background: #f0f2ff;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
}
.stat-box h2 {
    margin: 0;
    color: #667eea;
}
.stat-box p {
    margin: 0;
    font-size: 0.85rem;
    color: #6c757d;
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
#  회원가입
# ═══════════════════════════════════════
def page_register():
    st.markdown('<div class="main-title">📋 우리반 알림장</div>', unsafe_allow_html=True)
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

        # 학번 자동 생성 (예: 1학년 7반 1번 → 10701)
        user_id = f"{grade}{class_num:02d}{student_num:02d}"

        # 같은 학년/반/번호 중복 확인
        dup = (supabase.table("students")
               .select("id")
               .eq("grade", grade)
               .eq("class_num", class_num)
               .eq("student_num", student_num)
               .execute())
        if dup.data:
            st.error("이미 가입된 학번입니다. 로그인해주세요.")
            return

        # 가입
        supabase.table("students").insert({
            "user_id": user_id,
            "password_hash": hash_pw(password),
            "name": name,
            "grade": grade,
            "class_num": class_num,
            "student_num": student_num,
            "created_at": datetime.now().isoformat()
        }).execute()

        st.success(f"🎉 {name}님, 가입 완료! 학번 **{user_id}** 로 로그인하세요.")


# ═══════════════════════════════════════
#  로그인
# ═══════════════════════════════════════
def page_login():
    st.markdown('<div class="main-title">📋 우리반 알림장</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">로그인하여 공지와 개인 코드를 확인하세요</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        user_id = st.text_input("학번 (예: 10701 = 1학년7반1번)")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인", use_container_width=True)

    if submitted:
        if not user_id or not password:
            st.error("아이디와 비밀번호를 입력해주세요.")
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
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

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
        st.markdown(f'<div class="main-title">📋 우리반 알림장</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-title">{grade}학년 {class_num}반 {user["student_num"]}번 {user["name"]}</div>', unsafe_allow_html=True)
    with col2:
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()

    tab1, tab2 = st.tabs(["📢 전체 공지", "🔐 내 개인 코드"])

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

    # ── 공지 관리 ──
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
                col_a, col_b = st.columns([5, 1])
                with col_a:
                    date_str = n["created_at"][:10] if n.get("created_at") else ""
                    st.markdown(f"**{n['title']}** ({date_str})")
                    st.caption(n["content"][:100])
                with col_b:
                    if st.button("삭제", key=f"del_notice_{n['id']}"):
                        supabase.table("notices").delete().eq("id", n["id"]).execute()
                        st.rerun()

    # ── 개인 메시지 보내기 ──
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

        # CSV 양식 안내
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

    # ── 학생 관리 ──
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
                col_a, col_b, col_c = st.columns([5, 1, 1])
                with col_a:
                    st.text(f"{s['grade']}-{s['class_num']}반 {s['student_num']}번 {s['name']} (학번: {s['user_id']})")
                with col_b:
                    if st.button("🔑초기화", key=f"reset_pw_{s['id']}"):
                        # 비밀번호를 학번으로 초기화
                        supabase.table("students").update({
                            "password_hash": hash_pw(s["user_id"])
                        }).eq("id", s["id"]).execute()
                        st.success(f"{s['name']} 비밀번호 → 학번({s['user_id']})으로 초기화!")
                        st.rerun()
                with col_c:
                    if st.button("삭제", key=f"del_student_{s['id']}"):
                        (supabase.table("personal_messages")
                         .delete()
                         .eq("grade", s["grade"])
                         .eq("class_num", s["class_num"])
                         .eq("student_num", s["student_num"])
                         .execute())
                        supabase.table("students").delete().eq("id", s["id"]).execute()
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
