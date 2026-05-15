from src.database.config import supabase
import bcrypt
from datetime import datetime, timedelta
import secrets


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def get_teacher_by_username_or_email(value):
    if not value:
        return None

    value = value.strip()

    try:
        response = (
            supabase.table("teachers")
            .select("*")
            .eq("username", value)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]
    except Exception as e:
        print("Teacher username lookup error:", e)

    try:
        response = (
            supabase.table("teachers")
            .select("*")
            .eq("email", value)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]
    except Exception as e:
        print("Teacher email lookup error:", e)

    return None


def create_teacher(username, password, name, email=None):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name,
        "email": email,
    }
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    teacher = get_teacher_by_username_or_email(username)
    if teacher and check_pass(password, teacher["password"]):
        return teacher
    return None


def update_teacher_password(teacher_id, new_password):
    data = {"password": hash_pass(new_password), "updated_at": datetime.now().isoformat()}
    response = supabase.table("teachers").update(data).eq("teacher_id", teacher_id).execute()
    return response.data


def create_teacher_otp(teacher_id, purpose="login"):
    otp = f"{secrets.randbelow(900000) + 100000}"
    expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    data = {
        "teacher_id": teacher_id,
        "otp_code": otp,
        "purpose": purpose,
        "expires_at": expires_at,
        "used": False,
    }
    supabase.table("teacher_otps").insert(data).execute()
    return otp


def verify_teacher_otp(teacher_id, otp_code, purpose="login"):
    if not teacher_id or not otp_code:
        return False

    response = (
        supabase.table("teacher_otps")
        .select("*")
        .eq("teacher_id", teacher_id)
        .eq("otp_code", str(otp_code).strip())
        .eq("purpose", purpose)
        .eq("used", False)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        return False

    row = response.data[0]

    try:
        expires_at = datetime.fromisoformat(str(row["expires_at"]).replace("Z", "+00:00"))
        if expires_at.tzinfo is not None:
            expires_at = expires_at.replace(tzinfo=None)
    except Exception:
        return False

    if datetime.utcnow() > expires_at:
        return False

    supabase.table("teacher_otps").update({"used": True}).eq("otp_id", row["otp_id"]).execute()
    return True


def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data


def create_student(new_name, student_roll_number=None, face_embedding=None, voice_embedding=None):
    data = {
        "name": new_name,
        "university_roll_number": student_roll_number,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding,
    }
    response = supabase.table("students").insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data


def get_teacher_subjects(teacher_id):
    response = (
        supabase.table("subjects")
        .select("*, subject_students(count), attendance_logs(timestamp)")
        .eq("teacher_id", teacher_id)
        .execute()
    )
    subjects = response.data
    for sub in subjects:
        sub["total_students"] = sub.get("subject_students", [{}])[0].get("count", 0) if sub.get("subject_students") else 0
        attendance = sub.get("attendance_logs", [])
        unique_sessions = len(set(log["timestamp"] for log in attendance))
        sub["total_classes"] = unique_sessions
        sub.pop("subject_student", None)
        sub.pop("attendance_logs", None)
    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {"student_id": student_id, "subject_id": subject_id}
    response = supabase.table("subject_students").insert(data).execute()
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response = supabase.table("subject_students").delete().eq("student_id", student_id).eq("subject_id", subject_id).execute()
    return response.data


def get_student_subjects(student_id):
    response = supabase.table("subject_students").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table("attendance_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table("attendance_logs").insert(logs).execute()
    return response.data


def get_attendance_for_teacher(teacher_id):
    response = (
        supabase.table("attendance_logs")
        .select("*, subjects!inner(*), students(*)")
        .eq("subjects.teacher_id", teacher_id)
        .execute()
    )
    return response.data
