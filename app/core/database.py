from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker


engine = create_async_engine(
    url=make_url(
        name_or_url=f"postgresql+asyncpg://root:textile9495@127.0.0.1:5432/smart-u"
    ),
    echo=False,
    future=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)


async_session = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
