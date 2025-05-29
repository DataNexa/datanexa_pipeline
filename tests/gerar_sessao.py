from dags.services.API.APIDatanexa import APIDatanexa


api = APIDatanexa()

response = api.get("auth/healthcheck")

print(response.body(), response.code(), response.message())

print(api.getSession())
