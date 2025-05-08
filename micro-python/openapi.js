{
    "openapi": "3.1.0",
    "info": {
      "title": "1R-Micro API",
      "version": "1.0.0",
      "description": "OpenAPI 3.1 schema for the 1R-Micro v1 API."
    },
    "paths": {
      "/v1/objects": {
        "get": {
          "summary": "List all objects",
          "responses": {
            "200": {
              "description": "Array of JSON-LD objects"
            }
          }
        },
        "post": {
          "summary": "Create a new object",
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "object"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": "Object created"
            }
          }
        }
      },
      "/v1/objects/{object_id}": {
        "get": {
          "summary": "Get object by ID",
          "parameters": [
            {
              "name": "object_id",
              "in": "path",
              "required": true,
              "schema": { "type": "string" }
            }
          ],
          "responses": {
            "200": { "description": "Object found" },
            "404": { "description": "Not found" }
          }
        },
        "put": {
          "summary": "Replace full object",
          "parameters": [
            {
              "name": "object_id",
              "in": "path",
              "required": true,
              "schema": { "type": "string" }
            }
          ],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "object"
                }
              }
            }
          },
          "responses": {
            "200": { "description": "Object replaced" }
          }
        },
        "patch": {
          "summary": "Update object partially",
          "parameters": [
            {
              "name": "object_id",
              "in": "path",
              "required": true,
              "schema": { "type": "string" }
            }
          ],
          "requestBody": {
            "required": true,
            "content": {
              "application/merge-patch+json": {
                "schema": {
                  "type": "object"
                }
              }
            }
          },
          "responses": {
            "200": { "description": "Object updated" }
          }
        },
        "delete": {
          "summary": "Delete object",
          "parameters": [
            {
              "name": "object_id",
              "in": "path",
              "required": true,
              "schema": { "type": "string" }
            }
          ],
          "responses": {
            "200": { "description": "Object deleted" },
            "404": { "description": "Not found" }
          }
        }
      },
      "/v1/objects/{object_id}/render": {
        "get": {
          "summary": "Render object in human-readable format",
          "parameters": [
            {
              "name": "object_id",
              "in": "path",
              "required": true,
              "schema": { "type": "string" }
            },
            {
              "name": "format",
              "in": "query",
              "schema": { "type": "string", "enum": ["html", "md", "ascii"] }
            }
          ],
          "responses": {
            "200": { "description": "Rendered string" },
            "404": { "description": "Object not found" }
          }
        }
      },
      "/v1/subscriptions": {
        "post": {
          "summary": "Create a subscription",
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "object"
                }
              }
            }
          },
          "responses": {
            "201": { "description": "Subscription created" }
          }
        },
        "get": {
          "summary": "List all subscriptions",
          "responses": {
            "200": { "description": "Array of subscriptions" }
          }
        }
      },
      "/v1/subscriptions/{sub_id}": {
        "delete": {
          "summary": "Delete a subscription",
          "parameters": [
            {
              "name": "sub_id",
              "in": "path",
              "required": true,
              "schema": { "type": "string" }
            }
          ],
          "responses": {
            "200": { "description": "Subscription deleted" },
            "404": { "description": "Not found" },
            "403": { "description": "Forbidden" }
          }
        }
      },
      "/v1/events": {
        "post": {
          "summary": "Post a domain event",
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "object"
                }
              }
            }
          },
          "responses": {
            "201": { "description": "Event created" }
          }
        }
      },
      "/v1/whoami": {
        "get": {
          "summary": "Return the caller's entity context",
          "responses": {
            "200": { "description": "Entity info" },
            "401": { "description": "Unauthorized" }
          }
        }
      }
    }
  }
  