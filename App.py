from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

#sample data
todos = [
    {"id":1, "task":"Learn Flask", "completed":False},
    {"id":2, "task":"Buld REST API", "completed":False}
]

class TodoList(Resource):
    def get(self):
        return jsonify({"todos":todos})

    
    def post(self):
        data = request.get_json()
        new_todo = {
            "id": len(todos) + 1,
            "task": data.get("task"),
            "completed":False
        }
        todos.append(new_todo)
        print(todos)
        return new_todo
    

class Todo(Resource):
    def put(self, todo_id):
        todo = next((t for t in todos if t['id'] == todo_id), None)
        if todo is None:
            return {"Error":f"Todo with id {todo_id} not found"}, 404
        data = request.get_json()
        todo["task"] = data.get("task", todo['task'])
        todo['completed'] = data.get('completed', todo['completed'])
        return todo
    
    def delete(self, todo_id):
        global todos
        todos = [t for t in todos if t['id'] != todo_id]
        return "", 204

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, "/todos/<int:todo_id>")

if __name__ == "__main__":
    app.run(debug=True)