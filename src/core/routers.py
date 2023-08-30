from company.router import CompanyRouter
from cv.router import CVRouter
from main import app

routers = [
    CVRouter,
    CompanyRouter,
]

for router in routers:
    new_router = router(app)
    new_router.configure_routes()
