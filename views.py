from main import *
import json
from flask import Flask, request

# вьюшка для получения всех пользователей
@app.route('/users')
def get_users():
	user_list = User.query.all()  # к классу User применяем атрибут для запроса, а далее метод для получения всех элементов
	users_result = []
	for user in user_list:
		users_result.append(user.user_dict())
	# возвращаем результат в виде json словаря, применяя метод для модели
	return jsonify(users_result)



# вьюшка для получения пользователя по id
@app.route("/users/<int:id>")
def get_user_by_id(id):
	user = User.query.get(id)  # к классу User применяем атрибут для запроса, а далее метод для получения элемента
	if user is None:
		return 'user not found'
	# возвращаем результат в виде json словаря, применяя метод для модели
	return jsonify(user.user_dict())

# вьюшка для получения всех заказов
@app.route('/orders')
def get_orders():
	order_list = Order.query.all()  # к классу Order применяем атрибут для запроса, а далее метод для получения всех элементов
	orders_result = []
	for order in order_list:
		orders_result.append(order.order_dict())
	# возвращаем результат в виде json словаря, применяя метод для модели
	return jsonify(orders_result)

# вьюшка для получения заказа по id
@app.route("/orders/<int:id>")
def get_order_by_id(id):
	order = Order.query.get(id)  # к классу Order применяем атрибут для запроса, а далее метод для получения элемента
	if order is None:
		return 'order not found'
	# возвращаем результат в виде json словаря, применяя метод для модели
	return jsonify(order.order_dict())

# вьюшка для получения всех предложений
@app.route('/offers')
def get_offers():
	offer_list = Offer.query.all()  # к классу Offer применяем атрибут для запроса, а далее метод для получения всех элементов
	offers_result = []
	for offer in offer_list:
		offers_result.append(offer.offer_dict())
	# возвращаем результат в виде json словаря, применяя метод для модели
	return jsonify(offers_result)

# вьюшка для получения предложения по id
@app.route("/offers/<int:id>")
def get_offer_by_id(id):
	offer = Offer.query.get(id)  # к классу Offer применяем атрибут для запроса, а далее метод для получения элемента
	if offer is None:
		return 'offer not found'
	# возвращаем результат в виде json словаря, применяя метод для модели
	return jsonify(offer.offer_dict())

# вьюшка для добавления пользователя
@app.route("/users", methods=["POST"])
def add_user():
	user_data = json.loads(request.data)  #  то что передается в запросе, формируется в json формате
	#  создаем экземпляр класса User на основе переданного запроса
	new_user = User(
		id = user_data["id"],
		first_name = user_data["first_name"],
		last_name = user_data["last_name"],
		age = user_data["age"],
		email = user_data["email"],
		role = user_data["role"],
		phone = user_data["phone"]
	)
	db.session.add(new_user)  # добавляем объект db в сессию через атрибут session, а к нему применяем метод для добавления пользователя
	db.session.commit()  # подтверждаем сессию
	return ""

# вьюшка для обновления или удаления пользователя по id
@app.route("/users/<int:id>", methods=["PUT", "DELETE"])
def change_or_delete_user(id):
	if request.method == "PUT":
		user_data = json.loads(request.data)  # то что передается в запросе, формируется в json формате
		new_user = User.query.get(id)  # к классу User применяем атрибут для запроса, а далее метод для получения элемента
		new_user.first_name = user_data["first_name"]
		new_user.last_name = user_data["last_name"]
		new_user.age = user_data["age"]
		new_user.email = user_data["email"]
		new_user.role = user_data["role"]
		new_user.phone = user_data["phone"]

		db.session.add(new_user)
		db.session.commit()
		return ""

	if request.method == "DELETE":
		new_user = User.query.get(id)
		db.session.delete(new_user)
		db.session.commit()
		return ""

# вьюшка для добавления заказа
@app.route("/orders", methods=["POST"])
def add_order():
	order_data = json.loads(request.data)  #  то что передается в запросе, формируется в json формате
	#  создаем экземпляр класса Order на основе переданного запроса
	new_order = Order(
		id=order_data["id"],
		name=order_data["name"],
		description=order_data["description"],
		start_date=order_data["start_date"],
		end_date=order_data["end_date"],
		address=order_data["address"],
		customer_id=order_data["customer_id"],
		executor_id=order_data["executor_id"]
	)
	db.session.add(new_order)  # добавляем объект db в сессию через атрибут session, а к нему применяем метод для добавления пользователя
	db.session.commit()  # подтверждаем сессию
	return ""

# вьюшка для обновления или удаления заказа по id
@app.route("/orders/<int:id>", methods=["PUT", "DELETE"])
def change_or_delete_order(id):
	if request.method == "PUT":
		order_data = json.loads(request.data)  # то что передается в запросе, формируется в json формате
		new_order = Order.query.get(id)  # к классу Order применяем атрибут для запроса, а далее метод для получения элемента
		new_order.id = order_data["id"]
		new_order.name = order_data["name"]
		new_order.description = order_data["description"]
		new_order.start_date = order_data["start_date"]
		new_order.end_date = order_data["end_date"]
		new_order.address = order_data["address"]
		new_order.customer_id = order_data["customer_id"]
		new_order.executor_id = order_data["executor_id"]

		db.session.add(new_order)
		db.session.commit()
		return ""

	if request.method == "DELETE":
		new_order = Order.query.get(id)
		db.session.delete(new_order)
		db.session.commit()
		return ""

# вьюшка для добавления предложения
@app.route("/offers", methods=["POST"])
def add_offer():
	offer_data =json.loads(request.data)  #  то что передается в запросе, формируется в json формате
	#  создаем экземпляр класса User на основе переданного запроса
	new_offer = Offer(
		id=offer_data["id"],
		order_id=offer_data["order_id"],
		executor_id=offer_data["executor_id"]
	)
	db.session.add(new_offer)  # добавляем объект db в сессию через атрибут session, а к нему применяем метод для добавления пользователя
	db.session.commit()  # подтверждаем сессию
	return ""

# вьюшка для обновления или удаления предложения по id
@app.route("/offers/<int:id>", methods=["PUT", "DELETE"])
def change_or_delete_offer(id):
	if request.method == "PUT":
		offer_data = json.loads(request.data)  # то что передается в запросе, формируется в json формате
		new_offer = Offer.query.get(id)  # к классу Order применяем атрибут для запроса, а далее метод для получения элемента
		new_offer.id = offer_data["id"]
		new_offer.order_id = offer_data["order_id"]
		new_offer.executor_id = offer_data["executor_id"]

		db.session.add(new_offer)
		db.session.commit()
		return ""

	if request.method == "DELETE":
		new_offer = Offer.query.get(id)
		db.session.delete(new_offer)
		db.session.commit()
		return ""


app.run()