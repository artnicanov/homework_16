import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import data

app = Flask(__name__)  # переменная app - это экземпляр класса Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # устанавливаем конфигурацию для подключения к БД

db = SQLAlchemy(app)  # создаем экземпляр SQLAlchemy, в который передается наше приложение, а в нем уже есть настройка соединения с базой

class User(db.Model):
	"""
	создаем модель пользователя - класс User, который наследуется от базовой модели db.Model,
	в ней есть необходимый функционал для связи с таблицей
	"""
	__tablename__ = "user"  # так будет называться таблица

	# создаем колонки
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	age = db.Column(db.Integer)
	email = db.Column(db.String)
	role = db.Column(db.String)
	phone = db.Column(db.String)

	def user_dict(self):
		""" метод для созданной модели пользователя, который преобразует все поля в словарь """
		return {
			"id": self.id,
			"first_name": self.first_name,
			"last_name": self.last_name,
			"age": self.age,
			"email": self.email,
			"role": self.role,
			"phone": self.phone
		}

class Order(db.Model):
	""" модель заказа """
	__tablename__ = "order"  # так будет называться таблица

	# создаем колонки
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	start_date = db.Column(db.String)
	end_date = db.Column(db.String)
	address = db.Column(db.String)
	customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # связь с пользователем через внешний ключ из таблицы user
	executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # связь с пользователем через внешний ключ из таблицы user

	def order_dict(self):
		""" метод для созданной модели заказа, который преобразует все поля в словарь """
		return {
			"id": self.id,
			"name": self.name,
			"description": self.description,
			"start_date": self.start_date,
			"end_date": self.end_date,
			"address": self.address,
			"customer_id": self.customer_id,
			"executor_id": self.executor_id
		}

class Offer(db.Model):
	""" модель выполнения заказа """
	__tablename__ = "offer"  # так будет называться таблица

	# создаем колонки
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey("order.id"))  # связь с пользователем через внешний ключ из таблицы order
	executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # связь с пользователем через внешний ключ из таблицы user

	def offer_dict(self):
		""" метод для созданной модели выполнения заказа, который преобразует все поля в словарь """
		return {
			"id": self.id,
			"order_id": self.order_id,
			"executor_id": self.executor_id
		}

def create_db():
	"""  функция создает БД """
	app.app_context().push()
	with app.app_context():
		db.drop_all()
		db.create_all()
	for user_data in data.users:
		#  создаем объект класса User
		new_user = User(
			id=user_data["id"],
			first_name = user_data["first_name"],
			last_name = user_data["last_name"],
			age = user_data["age"],
			email = user_data["email"],
			role = user_data["role"],
			phone = user_data["phone"]
		)
		db.session.add(new_user)  # добавляем объект db в сессию через атрибут session, а к нему применяем метод для добавления пользователя
		db.session.commit()  # подтверждаем сессию

		for order_data in data.orders:
			#  создаем объект класса Order
			new_order = Order(
				id=order_data["id"],
				name=order_data["name"],
				description=order_data["description"],
				start_date=order_data["start_date"],
				end_date=order_data["end_date"],
				address=order_data["address"],
				customer_id=order_data["customer_id"],
				executor_id = order_data["executor_id"]
			)
			db.session.add(new_order)  # добавляем объект db в сессию через атрибут session, а к нему применяем метод для добавления заказа
			db.session.commit()  # подтверждаем сессию

			for offer_data in data.offers:
				#  создаем объект класса Offer
				new_offer = Offer(
					id=offer_data["id"],
					order_id=offer_data["order_id"],
					executor_id=offer_data["executor_id"]
				)
				db.session.add(new_offer)  # добавляем объект db в сессию через атрибут session, а к нему применяем метод для добавления исполнения заказа
				db.session.commit()  # подтверждаем сессию

@app.route('/users')
def get_users():
	user_list = User.query.all()  # к классу User применяем атрибут для запроса, а далее метод для получения всех элементов
	users_result = []
	for user in user_list:
		users_result.append(user.user_dict())
	# возвращаем результат в виде json словаря
	return json.dumps(users_result)

create_db()

app.run()