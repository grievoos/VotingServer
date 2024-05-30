from flask import Flask
from flask_restful import Api, Resource, reqparse
import sqlite3


server_app = Flask(__name__)
server_api = Api(server_app)
server_db_route = sqlite3.connect("voting.sqlite3", check_same_thread=False)


class Vote(Resource):
    def get(self):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("SELECT * FROM vote")
            get_vote_data = cursor.fetchall()
            vote_data = []
            for i in get_vote_data:
                vote_data.append({"id": i[0], "title": i[1], "start_date": i[2], "finish_date": i[3], "status": i[4]})
            return {"Response": vote_data}

    def post(self):
        with server_db_route:
            cursor = server_db_route.cursor()
            parser = reqparse.RequestParser()
            parser.add_argument("title", type=str, location="form")
            parser.add_argument("start_date", type=str, location="form")
            parser.add_argument("finish_date", type=str, location="form")
            parser.add_argument("status", type=str, location="form")
            cursor.execute("INSERT INTO vote (title, start_date, finish_date, status) VALUES (?, ?, ?, ?)",
                           (parser.parse_args()["title"], parser.parse_args()["start_date"],
                            parser.parse_args()["finish_date"], parser.parse_args()["status"],))
            server_db_route.commit()


class FindVoteDataById(Resource):
    def get(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("SELECT * FROM vote WHERE id = ?", (id,))
            get_vote_data = cursor.fetchall()
            return {"id": get_vote_data[0][0], "title": get_vote_data[0][1], "start_date": get_vote_data[0][2],
                    "finish_date": get_vote_data[0][3], "status": get_vote_data[0][4]}

    def put(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            parser = reqparse.RequestParser()
            parser.add_argument("title", type=str, location="form")
            parser.add_argument("start_date", type=str, location="form")
            parser.add_argument("finish_date", type=str, location="form")
            parser.add_argument("status", type=str, location="form")
            cursor.execute("UPDATE vote SET title = ?, start_date = ?, finish_date = ?, status = ? WHERE id = ?",
                           (parser.parse_args()["title"], parser.parse_args()["start_date"],
                            parser.parse_args()["finish_date"], parser.parse_args()["status"], id,))
            server_db_route.commit()

    def delete(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("DELETE FROM vote WHERE id = ?",
                           (id,))
            server_db_route.commit()


server_api.add_resource(Vote, "/Vote")
server_api.add_resource(FindVoteDataById, "/Vote/<int:id>")


class Users(Resource):
    def get(self):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("SELECT * FROM users")
            get_users_data = cursor.fetchall()
            users_data = []
            for i in get_users_data:
                users_data.append({"id": i[0], "first_name": i[1], "last_name": i[2], "email": i[3], "phone": i[4],
                                   "status": i[5]})
            return {"Response": users_data}

    def post(self):
        with server_db_route:
            cursor = server_db_route.cursor()
            parser = reqparse.RequestParser()
            parser.add_argument("first_name", type=str, location="form")
            parser.add_argument("last_name", type=str, location="form")
            parser.add_argument("email", type=str, location="form")
            parser.add_argument("phone", type=str, location="form")
            parser.add_argument("status", type=str, location="form")
            cursor.execute("INSERT INTO users (first_name, last_name, email, phone, status) VALUES (?, ?, ?, ?, ?)",
                           (parser.parse_args()["first_name"], parser.parse_args()["last_name"],
                            parser.parse_args()["email"], parser.parse_args()["phone"], parser.parse_args()["status"],))
            server_db_route.commit()


class FindUsersDataById(Resource):
    def get(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
            user_data = cursor.fetchall()
            return {"id": user_data[0][0], "first_name": user_data[0][1], "last_name": user_data[0][2],
                    "email": user_data[0][3], "phone": user_data[0][4], "status": user_data[0][5]}

    def put(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            parser = reqparse.RequestParser()
            parser.add_argument("first_name", type=str, location="form")
            parser.add_argument("last_name", type=str, location="form")
            parser.add_argument("email", type=str, location="form")
            parser.add_argument("phone", type=str, location="form")
            parser.add_argument("status", type=str, location="form")
            cursor.execute("UPDATE users SET first_name = ?, last_name = ?, email = ?, phone = ?, status = ?  WHERE id = ?",
                           (parser.parse_args()["first_name"], parser.parse_args()["last_name"],
                            parser.parse_args()["email"], parser.parse_args()["phone"],
                            parser.parse_args()["status"], id, ))
            server_db_route.commit()

    def delete(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (id, ))
            server_db_route.commit()


server_api.add_resource(Users, "/Users")
server_api.add_resource(FindUsersDataById, "/Users/<int:id>")


class Question(Resource):
    def get(self):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("SELECT question.id, question.vote_id, question.content, question.vote_date, vote.title FROM question, vote WHERE question.vote_id = vote.id")
            get_question_data = cursor.fetchall()
            question_data = []
            for i in get_question_data:
                question_data.append({"id": i[0], "vote_id": i[1], "content": i[2], "vote_date": i[3], "title": i[4]})
            return {"Response": question_data}

    def post(self):
        with server_db_route:
            cursor = server_db_route.cursor()
            parser = reqparse.RequestParser()
            parser.add_argument("vote_id", type=int, location="form")
            parser.add_argument("content", type=str, location="form")
            parser.add_argument("vote_date", type=str, location="form")
            cursor.execute("INSERT INTO question (vote_id, content, vote_date) VALUES (?, ?, ?)",
                           (parser.parse_args()["vote_id"], parser.parse_args()["content"],
                            parser.parse_args()["vote_date"], ))
            server_db_route.commit()


class FindQuestionDataById(Resource):
    def get(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("SELECT question.id, question.vote_id, question.content, question.vote_date, vote.title FROM question, vote WHERE question.vote_id = vote.id AND question.id = ?",
                           (id, ))
            question_data = cursor.fetchall()
            return {"id": question_data[0][0], "vote_id": question_data[0][1], "content": question_data[0][2],
                    "vote_date": question_data[0][3], "title": question_data[0][4]}

    def put(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            parser = reqparse.RequestParser()
            parser.add_argument("vote_id", type=int, location="form")
            parser.add_argument("content", type=str, location="form")
            parser.add_argument("vote_date", type=str, location="form")
            cursor.execute("UPDATE question SET vote_id = ?, content = ?, vote_date = ? WHERE id = ?",
                           (parser.parse_args()["vote_id"], parser.parse_args()["content"],
                 parser.parse_args()["vote_date"], id, ))
            server_db_route.commit()

    def delete(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("DELETE FROM question WHERE id = ?", (id, ))
            server_db_route.commit()


server_api.add_resource(Question, "/Question")
server_api.add_resource(FindQuestionDataById, "/Question/<int:id>")


class Choice(Resource):
    def get(self):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("SELECT choice.id, choice.question_id, choice.user_id, choice.user_choice, question.content, users.first_name || ' ' || users.last_name as fullname FROM choice, question, users WHERE choice.question_id = question.id AND choice.user_id = users.id")
            get_choice_data = cursor.fetchall()
            vote_data = []
            for i in get_choice_data:
                vote_data.append({"id": i[0], "question_id": i[1], "user_id": i[2], "user_choice": i[3],
                                  "content": i[4], "fullname": i[5]})
        return {"Response": vote_data}

    def post(self):
        with server_db_route:
            cursor = server_db_route.cursor()
            parser = reqparse.RequestParser()
            parser.add_argument("question_id", type=int, location="form")
            parser.add_argument("user_id", type=int, location="form")
            parser.add_argument("user_choice", type=str, location="form")
            cursor.execute("INSERT INTO choice (question_id, user_id, user_choice) VALUES (?, ?, ?)",
                           (parser.parse_args()["question_id"], parser.parse_args()["user_id"],
                            parser.parse_args()["user_choice"], ))
            server_db_route.commit()


class FindChoiceById(Resource):
    def get(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("SELECT choice.id, choice.question_id, choice.user_id, choice.user_choice, question.content, users.first_name || ' ' || users.last_name as fullname FROM choice, question, users WHERE choice.question_id = question.id AND choice.user_id = users.id AND choice.id = ?",
                           (id, ))
            vote_data = cursor.fetchall()
            return {"id": vote_data[0][0], "question_id": vote_data[0][1], "user_id": vote_data[0][2],
                    "user_choice": vote_data[0][3], "content": vote_data[0][4], "fullname": vote_data[0][5]}

    def put(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            parser = reqparse.RequestParser()
            parser.add_argument("question_id", type=int, location="form")
            parser.add_argument("user_id", type=int, location="form")
            parser.add_argument("user_choice", type=str, location="form")
            cursor.execute("UPDATE choice SET question_id = ?, user_id = ?, user_choice = ? WHERE id = ?",
                           (parser.parse_args()["question_id"], parser.parse_args()["user_id"],
                            parser.parse_args()["user_choice"], id, ))
            server_db_route.commit()

    def delete(self, id):
        with server_db_route:
            cursor = server_db_route.cursor()
            cursor.execute("DELETE FROM choice WHERE id = ?", (id, ))
            server_db_route.commit()


server_api.add_resource(Choice, "/Choice")
server_api.add_resource(FindChoiceById, "/Choice/<int:id>")


server_api.init_app(server_app)
server_app.run(debug=True, host="192.168.3.60")
