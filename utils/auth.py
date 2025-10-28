# FILE: utils/auth.py
from fastapi import Request, HTTPException, status
from utils.supabase import supabase  # Make sure this import matches your file


async def verify(request: Request):
    """
    Verify the requester is a valid student or teacher.
    Works by checking headers injected by the API Gateway (X-User-Id, X-User-Role).
    Falls back to cookies/headers for local development.
    """

    # 1. Check for Gateway-injected headers (production)
    user_id = request.headers.get("X-User-Id")
    role = request.headers.get("X-User-Role")

    # 2. Fallback for local testing (dev)
    if not user_id:
        user_id = request.cookies.get("user_id") or request.headers.get("user_id")
    if not role:
        role = request.cookies.get("role") or request.headers.get("role")

    # --- Validation ---
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing user_id (header or cookie)")

    if role not in ["student", "teacher"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid role: {role}")

    # Check if user exists in the correct table
    table = "students" if role == "student" else "teachers"

    # Use the supabase client imported from utils.supabase
    res = supabase.table(table).select("id").eq("id", user_id).execute()

    if not res.data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found in database")

    # Return both user_id and role
    return {"user_id": user_id, "role": role}
