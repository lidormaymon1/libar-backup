import json, requests, random, datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import String, or_, func, Integer




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libary.sqlite3'
app.config['SECRET_KEY'] = "random string"
CORS(app)

db = SQLAlchemy(app)


# Books model

class Books(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique = True)
    author = db.Column(db.String(100))
    date_published = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    type = db.Column(db.Integer)
    loans = db.relationship('Loans', backref='book')


    def __init__(self, name, author, date_published, type, quantity):
        self.name = name
        self.author = author
        self.date_published = date_published
        self.type = type
        self.quantity = quantity

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'date_published': self.date_published,
            'quantity': self.quantity,
            'type': self.type
        }
    


# Function to fetch bookS data from open libary API and add it to the database,
# we only call this function once to fill the database with an actual data.
#sources:
#   Open Libary:https://openlibrary.org/subjects/python.json
#               https://openlibrary.org/subjects/cooking.json
#               https://openlibrary.org/subjects/humor.json
#               https://openlibrary.org/subjects/kids_books.json
#               https://openlibrary.org/subjects/exercise.json

def fetch_and_add_books():
    url = 'https://openlibrary.org/subjects/exercise.json'  
    response = requests.get(url)
    data = response.json()

    for work in data.get('works', []):
        book_data = work.get('title', '')
        author_data = work.get('authors', [])
        published_data = work.get('first_publish_year', '')

        if isinstance(book_data, dict):
            book_name = book_data.get('title', '')
        else:
            book_name = book_data

        # Check if a book with the same name already exists
        existing_book = Books.query.filter_by(name=book_name).first()
        if existing_book:
            continue  # Ignore the book if it already exists in the database

        # Extract the book name, author, and date published from the data
        authors = [author.get('name', '') for author in author_data]
        if isinstance(published_data, int):
            year_published = ''
            date_published = datetime.datetime(published_data, 1, 1).strftime('%d/%m/%Y')
        else:
            year_published = ''
            date_published = ''

        book_type = random.randint(1, 3)
        book_quantity = random.randint(1, 15)
        new_book = Books(book_name, ', '.join(authors), date_published, book_type, book_quantity)
        db.session.add(new_book)

    db.session.commit()


#End of functiong fetching books
# Function to display books
@app.route('/show-books')
def showBooks():
    books_list = [book.to_dict() for book in Books.query.all()]
    json_data = json.dumps(books_list)
    return json_data
# End showing books function


#Function to search in books
@app.route('/search-books')
def searchBooks():
    search_term = request.args.get('search', '').lower()
    books_list = [book.to_dict() for book in Books.query.filter(
        or_(
            func.lower(Books.name).like(f'%{search_term}%'),
            func.lower(Books.author).like(f'%{search_term}%'),
        )
    )]
    json_data = json.dumps(books_list)
    return json_data
#End of function


#Function of counting how many books
def countBooks():
    books_list = [book.to_dict() for book in Books.query.all()]
    for book_count in len(books_list):
        book_count += 1
    print(book_count)
#End of count books function

# Function to add book to books
@app.route('/add-book', methods=['POST'])
def add_book():
    data = request.get_json()
    # print(data)
    name = data['name']
    author = data['author']
    date_published = data['date_published']
    type = data['type']
    quantity = data['quantity']

    new_book = Books(name, author, date_published, type, quantity)
    db.session.add(new_book)
    db.session.commit()
    return "A new record was created."
# End of function

#Function of updating book
@app.route('/books-update/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = Books.query.get(id)

    if book:
        book.name = data.get('name', book.name)
        book.author = data.get('author', book.author)
        book.date_published = data.get('date_published', book.date_published)
        book.quantity = data.get('quantity', book.quantity)
        book.type = data.get('type', book.type)

        db.session.commit()
        return 'sucess'
#End function update book


# Delete book function
@app.route('/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Books.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return 'delete'


# End of function
# END OF BOOKS MODEL!!!!!


# Customers model
class Customers(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    age = db.Column(db.String(100))
    loans = db.relationship('Loans', backref='customer')

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


# Show customers function
@app.route('/show-customers')
def show_customers():
    customers_list = [customer.to_dict() for customer in Customers.query.all()]
    json_data = json.dumps(customers_list)
    return json_data
# End function

#Function to search in customers
@app.route('/search-customers')
def searchCustomer():
    search_term = request.args.get('search', '').lower()
    customers_list = [customer.to_dict() for customer in Customers.query.filter(
        or_(
        func.lower(Customers.name).like(f'%{search_term}%')
        )
    )]
    json_Data = json.dumps(customers_list)
    return json_Data
#End of function searching customers

#Function of updating customer
@app.route('/customers-update/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = Customers.query.get(id)

    if customer:
        customer.name = data.get('name', customer.name)
        customer.city = data.get('city', customer.city)
        customer.age = data.get('age', customer.age)

        db.session.commit()
        return 'sucess'
#End function update customer


# Add customer function
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


# End of function

# Delete book function
@app.route('/deleteCustomer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customers.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return 'delete'


# End of function
#END OF CUSTOMERS MODEL!!!

##############
# Loans model#
###############
class Loans(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    custid = db.Column(db.Integer, db.ForeignKey('customers.ID'))
    bookid = db.Column(db.Integer, db.ForeignKey('books.ID'))
    loandate = db.Column(db.String(100))
    returndate = db.Column(db.String(100))

    def __init__(self, custid, bookid, loandate, returndate):
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

#Showing loans function
@app.route('/show-loans')
def showLoans():
    loans_list = [loan.to_dict() for loan in Loans.query.all()]
    json_data = json.dumps(loans_list)
    return json_data
#end of showing loans function

#Search loan function
@app.route('/search-loan')
def searchLoan():
    search_term = int(request.args.get('search', ''))
    print(type(search_term))
    # search_term = str(search_term)
    loans_list = [loan.to_dict() for loan in Loans.query.filter(
        or_(
            func.cast(Loans.custid, Integer).like(f'%{search_term}%')
        )
    )]
    json_data = json.dumps(loans_list)
    print(json_data)
    return json_data


#End of function


#Showing expired loans function
@app.route('/show-expired-loans')
def showExpiredLoans():
    loans_list = [loan.to_dict() for loan in Loans.query.all()]
    current_date= datetime.datetime.now()
    expired_loans = []
    for loan in loans_list:
        returnLoanDate = loan['returndate']

        print(returnLoanDate)
        returnLoanDate = datetime.datetime.strptime(returnLoanDate, '%d/%m/%Y')
        if current_date > returnLoanDate:
            expired_loans.append(loan)
    return expired_loans


#Add loan function
@app.route('/add-loan', methods=['POST'])
def add_loan():
    data = request.get_json()
    # print(data)
    custid = data['custid']
    bookid = data['bookid']
    loandate = data['loandate']
    returndate = data['returndate']

    new_loan = Loans(custid, bookid, loandate, returndate)
    db.session.add(new_loan)
    db.session.commit()
    return "A new record was created."
#End of function

#Function of updating loan
@app.route('/loans-update/<int:id>', methods=['PUT'])
def update_loan(id):
    data = request.get_json()
    loan = Loans.query.get(id)

    if loan:
        loan.custid = data.get('custid', loan.custid)
        loan.bookid = data.get('bookid', loan.bookid)
        loan.loandate = data.get('loandate', loan.loandate)
        loan.returndate = data.get('returndate', loan.returndate)

        db.session.commit()
        return 'sucess'
#End function update loan

#Function of returning loan
@app.route('/deleteLoan/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    loan = Loans.query.get(loan_id)
    if loan:
        db.session.delete(loan)
        db.session.commit()
        return 'delete'
#End of function



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # fetch_and_add_books()
    app.run(debug=True)


