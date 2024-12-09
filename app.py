from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)

# GraphQL endpoint
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema, graphiql=True
    ),
)

if __name__ == "__main__":
    app.run(debug=True)
