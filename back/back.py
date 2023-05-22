
import json
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libary.sqlite3'
app.config['SECRET_KEY'] = "random string"
CORS(app)

db = SQLAlchemy(app)



#Books model

class Books(db.Model):
    id = db.Column('ID',db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year_published = db.Column(db.String(100))
    type = db.Column(db.String(100))

    def __init__(self, name, author, year_published, type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.type = type

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'year_published': self.year_published,
            'type': self.type
        }


#Function to display books
@app.route('/show-books')
def showBooks():
    books_list = [book.to_dict() for book in Books.query.all()]
    json_data = json.dumps(books_list)
    return json_data
#End function



#Function to add book to books
@app.route('/add-book', methods=['POST'])
def add_book():
    data = request.get_json()
    # print(data)
    name = data['name']
    author = data['author']
    year_published = data['year_published']
    type = data['type']

    new_book = Books(name, author, year_published, type)
    db.session.add(new_book)
    db.session.commit()
    return "A new record was created."
#End of function


#Delete book function
@app.route('/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book=Books.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return 'delete'
#End of function
#END OF BOOKS MODEL!!!!!


#Customers model
class Customers(db.Model):
    id = db.Column('ID',db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    age = db.Column(db.String(100))


    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'age': self.age,
        }


#Show customers function
@app.route('/show-customers')
def show_customers():
    customers_list = [customer.to_dict() for customer in Customers.query.all()]
    json_data = json.dumps(customers_list)
    return json_data
#End function


#Add customer function
@app.route('/add-customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    # print(data)
    name = data['name']
    city = data['city']
    age = data['age']


    new_customer = Customers(name, city, age)
    db.session.add(new_customer)
    db.session.commit()
    return "A new record was created."
#End of function

#Delete book function
@app.route('/deleteCustomer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer=Customers.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return 'delete'
#End of function

#Loans model

class Loans(db.Model):
    id = db.Column('ID',db.Integer, primary_key = True)
    custid = db.Column(db.String(100))
    bookid = db.Column(db.String(100))
    loandate = db.Column(db.String(100))
    returndate = db.Column(db.String(100))


    def __init__(self, custid, bookid, loandate,returndate):
        self.custid = custid
        self.bookid = bookid
        self.loandate = loandate
        self.returndate = returndate



    def to_dict(self):
        return {
            'id': self.id,
            'custid': self.custid,
            'bookid': self.bookid,
            'loandate': self.loandate,
            'returndate': self.returndate
        }


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)