from flask import Flask, jsonify, request



app = Flask(__name__)

# Przykładowa baza danych (w pamięci)
users = [
    {"id": 1, "name": "Jan Kowalski", "email": "jan@kowalski.pl"},
    {"id": 2, "name": "Anna Nowak", "email": "anna@nowak.pl"}
]

# GET /users - Zwraca listę użytkowników
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET /users/{id} - Zwraca szczegóły użytkownika na podstawie jego identyfikatora
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# POST /users - Tworzy nowego użytkownika
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(key in data for key in ("name", "email")):
        return jsonify({"error": "Invalid data"}), 400

    new_id = max(user["id"] for user in users) + 1 if users else 1
    new_user = {"id": new_id, "name": data["name"], "email": data["email"]}
    users.append(new_user)
    return jsonify(new_user), 201

# PUT /users/{id} - Aktualizuje dane użytkownika
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data or not any(key in data for key in ("name", "email")):
        return jsonify({"error": "Invalid data"}), 400

    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.update({key: data[key] for key in data if key in user})
    return jsonify(user), 200

# DELETE /users/{id} - Usuwa użytkownika na podstawie jego identyfikatora
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
