from flask import jsonify, request, abort
from service import app
from service.models import Product
from service.common import status


######################################################################
# ROUTES
######################################################################

@app.route("/")
def index():
    """Index page"""
    return jsonify(name="Product REST API Service", version="1.0"), status.HTTP_200_OK


@app.route("/health")
def health():
    """Health check"""
    return jsonify(status="OK", message="OK"), status.HTTP_200_OK


######################################################################
# CREATE A PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_product():
    """
    Create a Product
    This endpoint will create a Product based on the posted data
    """
    if not request.is_json:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be application/json")

    data = request.get_json()
    if "name" not in data:
        abort(status.HTTP_400_BAD_REQUEST, "Missing required field: name")

    product = Product()
    product.deserialize(data)
    product.create()

    location_url = f"{request.base_url}/{product.id}"
    return jsonify(product.serialize()), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# READ A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a single Product
    """
    app.logger.info("Request to Retrieve a product with id [%s]", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update a Product
    """
    if not request.is_json:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be application/json")

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    data = request.get_json()
    product.deserialize(data)
    product.update()

    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a Product
    """
    product = Product.find(product_id)
    if product:
        product.delete()

    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIST ALL PRODUCTS WITH OPTIONAL FILTERING
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """
    List all Products with optional filters:
    - name
    - category
    - available
    """
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    products = Product.all()

    if name:
        products = [p for p in products if p.name == name]
    if category:
        products = [p for p in products if p.category.name == category]
    if available is not None:
        available_bool = available.lower() in ["true", "1", "yes"]
        products = [p for p in products if p.available == available_bool]

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK
