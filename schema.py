from graphene import ObjectType, String, Int, Float, List, Field, Schema, Mutation, ID
from graphene.types.scalars import Scalar
from graphql import GraphQLError

# Mock inventory
inventory = []

class ProductType(ObjectType):
    id = ID()
    name = String()
    price = Float()
    quantity = Int()
    category = String()

class Query(ObjectType):
    products = List(ProductType)

    def resolve_products(root, info):
        return inventory

class AddProduct(Mutation):
    class Arguments:
        name = String(required=True)
        price = Float(required=True)
        quantity = Int(required=True)
        category = String(required=True)

    product = Field(ProductType)

    def mutate(root, info, name, price, quantity, category):
        # Validation
        if price < 0 or quantity < 0:
            raise GraphQLError("Price and quantity must be non-negative.")

        product_id = len(inventory) + 1
        product = {"id": str(product_id), "name": name, "price": price, "quantity": quantity, "category": category}
        inventory.append(product)
        return AddProduct(product=product)

class UpdateProduct(Mutation):
    class Arguments:
        id = ID(required=True)
        name = String()
        price = Float()
        quantity = Int()
        category = String()

    product = Field(ProductType)

    def mutate(root, info, id, name=None, price=None, quantity=None, category=None):
        # Find the product
        product = next((item for item in inventory if item["id"] == id), None)
        if not product:
            raise GraphQLError(f"Product with ID {id} not found.")

        # Update fields
        if name:
            product["name"] = name
        if price is not None:
            if price < 0:
                raise GraphQLError("Price must be non-negative.")
            product["price"] = price
        if quantity is not None:
            if quantity < 0:
                raise GraphQLError("Quantity must be non-negative.")
            product["quantity"] = quantity
        if category:
            product["category"] = category

        return UpdateProduct(product=product)

class DeleteProduct(Mutation):
    class Arguments:
        id = ID(required=True)

    success = String()

    def mutate(root, info, id):
        global inventory
        # Find the product
        product = next((item for item in inventory if item["id"] == id), None)
        if not product:
            raise GraphQLError(f"Product with ID {id} not found.")

        # Delete the product
        inventory = [item for item in inventory if item["id"] != id]
        return DeleteProduct(success=f"Product with ID {id} deleted successfully.")

class Mutation(ObjectType):
    add_product = AddProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

schema = Schema(query=Query, mutation=Mutation)
