from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware)


class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str
    published: bool

posts: list[Post] = [
    Post(
        id=1,
        title="Getting Started with FastAPI",
        content="FastAPI is a modern, fast web framework for building APIs with Python 3.8+.",
        author="TechEnthusiast",
        published=True
    ),
    Post(
        id=2,
        title="Mastering Pydantic",
        content="Data validation and settings management using Python type hints.",
        author="Pythonista",
        published=True
    ),
    Post(
        id=3,
        title="TDD with Pytest",
        content="Learn how to write better code by writing tests first.",
        author="CodeQuality",
        published=False
    ),
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "posts": posts,
            "title": "Home"
        }
    )

@app.get("/posts/{post_id}", include_in_schema=False)
def post_detail(request: Request,post_id: int):
    for post in posts:
        if post.id == post_id:
            title = post.title[:50]
            return templates.TemplateResponse(
                "post.html",
                 {
                    "request": request,
                    "post": post,
                    "title": post.title[:50]
                }
    )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/api/posts")
def get_posts():
    return {"posts": posts}

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):

    # api error response
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    # web page error response
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": exc.status_code,
            "title": "Something went wrong",
            "message": exc.detail
        },
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    # API → JSON
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "detail": exc.errors(),
                "body": exc.body,
            },
        )

    # HTML → Template
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": 422,
            "title": "Invalid Request",
            "message": "Some fields contain invalid data. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
