from fastapi import APIRouter

from follow.routes import follows
from password_service.routes import password
from posts.comments.routes import comment
from posts.posts.routes import post
# from posts.likes.routes import like
from search.routes import search
from users.auth.routes import auth
from users.profile.routes import user

router = APIRouter()

router.include_router(auth)
router.include_router(user)
router.include_router(post)
router.include_router(password)
router.include_router(comment)
# router.include_router(like)
router.include_router(search)
router.include_router(follows)
