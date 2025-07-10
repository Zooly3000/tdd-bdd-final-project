######################################################################
# Loading data into the service
######################################################################
from behave import given
import requests
from service.common.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED

@given('the following products')
def step_impl(context):
    """Delete all Products and load new ones"""
    # delete all products first
    rest_endpoint = f"{context.base_url}/products"
    response = requests.get(rest_endpoint)
    assert response.status_code == 200
    for product in response.json():
        response = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert response.status_code == HTTP_204_NO_CONTENT

    # load the database with new products
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'].lower() in ['true', '1'],
            "category": row['category']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTP_201_CREATED
