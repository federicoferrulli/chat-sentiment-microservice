
routes: list[dict] = [
    {
        "prefix": "/api", 
        "from": "health.HealthRoute",
        "import": "router"
    },
    {
        "prefix": "/api", 
        "from": "messages.MessageRoute",
        "import": "router"
    },
]
