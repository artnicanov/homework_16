import main

# вьюшка для получения всех пользователей
@main.app.route('/users')
def get_users():
	user_list = main.User.query.all()  # к классу User применяем атрибут для запроса, а далее метод для получения всех элементов
	users_result = []
	for user in user_list:
		users_result.append(user.user_dict())
	# возвращаем результат в виде json словаря, применяя метод для модели
	return main.jsonify(users_result)

# вьюшка для получения пользователя по id
@main.app.route("/users/<int:id>")
def get_user_by_id(id):
	user = main.User.query.get(id)  # к классу User применяем атрибут для запроса, а далее метод для получения элемента
	if user is None:
		return 'user not found'
	# возвращаем результат в виде json словаря, применяя метод для модели
	return main.jsonify(user.user_dict())

# вьюшка для получения всех заказов
@main.app.route('/orders')
def get_orders():
	order_list = main.Order.query.all()  # к классу Order применяем атрибут для запроса, а далее метод для получения всех элементов
	orders_result = []
	for order in order_list:
		orders_result.append(order.order_dict())
	# возвращаем результат в виде json словаря, применяя метод для модели
	return main.jsonify(orders_result)

# вьюшка для получения заказа по id
@main.app.route("/orders/<int:id>")
def get_order_by_id(id):
	order = main.Order.query.get(id)  # к классу Order применяем атрибут для запроса, а далее метод для получения элемента
	if order is None:
		return 'order not found'
	# возвращаем результат в виде json словаря, применяя метод для модели
	return main.jsonify(order.order_dict())

# вьюшка для получения всех предложений
@main.app.route('/offers')
def get_offers():
	offer_list = main.Offer.query.all()  # к классу Offer применяем атрибут для запроса, а далее метод для получения всех элементов
	offers_result = []
	for offer in offer_list:
		offers_result.append(offer.offer_dict())
	# возвращаем результат в виде json словаря, применяя метод для модели
	return main.jsonify(offers_result)

# вьюшка для получения предложения по id
@main.app.route("/offers/<int:id>")
def get_offer_by_id(id):
	offer = main.Offer.query.get(id)  # к классу Offer применяем атрибут для запроса, а далее метод для получения элемента
	if offer is None:
		return 'offer not found'
	# возвращаем результат в виде json словаря, применяя метод для модели
	return main.jsonify(offer.offer_dict())

# вьюшка для добавления пользователя
@main.app.route("/users", methods=["POST"])
def add_user():
	user_data = main.json.loads(main.request.data)  #  то что передается в запросе, формируется в json формате
	#  создаем экземпляр класса User на основе переданного запроса
	new_user = main.User(
		id = user_data["id"],
		first_name = user_data["first_name"],
		last_name = user_data["last_name"],
		age = user_data["age"],
		email = user_data["email"],
		role = user_data["role"],
		phone = user_data["phone"]
	)
	main.db.session.add(new_user)  # добавляем объект db в сессию через атрибут session, а к нему применяем метод для добавления пользователя
	main.db.session.commit()  # подтверждаем сессию
	return ""

# вьюшка для обновления или удаления пользователя по id
@main.app.route("/users/<int:id>", methods=["PUT", "DELETE"])
def change_or_delete_user(id):
	if main.request.method == "PUT":
		user_data = main.json.loads(main.request.data)  # то что передается в запросе, формируется в json формате
		new_user = main.User.query.get(id)  # к классу User применяем атрибут для запроса, а далее метод для получения элемента
		new_user.first_name = user_data["first_name"],
		new_user.last_name = user_data["last_name"],
		new_user.age = user_data["age"],
		new_user.email = user_data["email"],
		new_user.role = user_data["role"],
		new_user.phone = user_data["phone"]

		main.db.session.add(new_user)
		main.db.session.commit()
		return ""

	if main.request.method == "DELETE":
		new_user = main.User.query.get(id)
		main.db.session.delete(new_user)
		main.db.session.commit()
		return ""

# вьюшка для добавления заказа
@main.app.route("/orders", methods=["POST"])
def add_order():
	order_data = main.json.loads(main.request.data)  #  то что передается в запросе, формируется в json формате
	#  создаем экземпляр класса Order на основе переданного запроса
	new_order = main.Order(
		id=order_data["id"],
		name=order_data["name"],
		description=order_data["description"],
		start_date=order_data["start_date"],
		end_date=order_data["end_date"],
		address=order_data["address"],
		customer_id=order_data["customer_id"],
		executor_id=order_data["executor_id"]
	)
	main.db.session.add(new_order)  # добавляем объект db в сессию через атрибут session, а к нему применяем метод для добавления пользователя
	main.db.session.commit()  # подтверждаем сессию
	return ""

# вьюшка для обновления или удаления заказа по id
@main.app.route("/orders/<int:id>", methods=["PUT", "DELETE"])
def change_or_delete_order(id):
	# подготовить для PUT

	if main.request.method == "DELETE":
		new_order = main.Order.query.get(id)
		main.db.session.delete(new_order)
		main.db.session.commit()
		return ""

# вьюшка для добавления предложения
@main.app.route("/offers", methods=["POST"])
def add_offer():
	offer_data = main.json.loads(main.request.data)  #  то что передается в запросе, формируется в json формате
	#  создаем экземпляр класса User на основе переданного запроса
	new_offer = main.Offer(
		id=offer_data["id"],
		order_id=offer_data["order_id"],
		executor_id=offer_data["executor_id"]
	)
	main.db.session.add(new_offer)  # добавляем объект db в сессию через атрибут session, а к нему применяем метод для добавления пользователя
	main.db.session.commit()  # подтверждаем сессию
	return ""

# вьюшка для обновления или удаления предложения по id
@main.app.route("/offers/<int:id>", methods=["PUT", "DELETE"])
def change_or_delete_offer(id):
	# подготовить для PUT

	if main.request.method == "DELETE":
		new_offer = main.Offer.query.get(id)
		main.db.session.delete(new_offer)
		main.db.session.commit()
		return ""



main.app.run()