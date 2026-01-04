CANONICAL_MAP = {
    "react": ["react", "react.js", "reactjs", "react js"],
    "node": ["node", "node.js", "nodejs", "node js", "express", "express.js"],
    "postgresql": ["postgres", "postgresql", "psql", "sql database", "relational database", "sqlalchemy"],
    "javascript": ["javascript", "js", "ecmascript"],
    "python": ["python", "py", "python3"],
    "ci/cd": ["ci/cd", "cicd", "ci cd", "ci-cd", "pipelines", "github actions", "automation"],
    "docker": ["docker", "dockerized", "containerization", "containers"],
    "fastapi": ["fastapi", "fast-api", "fast api"]
}

CONCEPT_CANONICAL_MAP = {
    "rest": [
        "rest", "rest api", "restful api", "restful apis", "restful services",
        "api development", "backend apis", "endpoint optimization"
    ],
    "jwt": [
        "jwt", "jwt-based", "json web tokens", "token-based", 
        "token refresh logic", "session management"
    ],
    "authentication": [
        "authentication", "authorization", "auth", "auth systems",
        "authentication mechanism", "secure authentication flows",
        "access control", "user roles", "permissions", "rate limiting"
    ],
    "async": [
        "async", "asyncio", "async i/o", "asynchronous programming",
        "concurrency", "non-blocking", "latency improvement", "throughput"
    ],
    "llm": [
        "llm", "large language models", "llm integrations", "ai-powered",
        "rag", "retrieval augmented generation", "langchain", "langgraph",
        "embeddings", "vector stores", "chatbot", "ai pipelines"
    ],
    "database_design": [
        "database schema", "schema design", "database architecture",
        "normalized database", "query optimization", "query profiling",
        "data pipelines", "indexing"
    ],
    "backend_performance": [
        "caching", "caching strategies", "performance optimization",
        "latency", "profiling", "scalable backend"
    ]
}


VARIANT_TO_CANONICAL = {
    variant: canonical
    for canonical, variants in CANONICAL_MAP.items()
    for variant in variants
}

VARIANT_TO_CONCEPT_CANONICAL = {
    variant: canonical
    for canonical, variants in CONCEPT_CANONICAL_MAP.items()
    for variant in variants
}
