from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
async def register():
    return "Register"


@auth_router.post("/login")
async def login():
    return "Login"


@auth_router.post("/logout")
async def logout():
    return "Logout"
