from flyweb.web import Hasfly
from flyweb.render import render_template,redirect
from demo.Model.book import Book
app = Hasfly(__name__)

@app.route('/detail')
def detail(request):
    book_list = Book.find().order('pub_date').all()
    return render_template('detail', book_list=book_list)

@app.route('/addBook')
def addBook(request):
    if request.method == 'POST':
        temp_name = request.form['name']
        temp_author = request.form['author']
        temp_pub_house = request.form['pub_house']

    temp_book = Book(name=temp_name, author=temp_author, pub_house=temp_pub_house)
    temp_book.save()
    #重定向
    return redirect('/detail')

@app.route('/delBook/<book_id:int>')
def deleteBook(request, book_id):
    Book.deleteOne(id=book_id)
    # book = Book.find().where(id=book_id).one()
    # book.delete()
    return redirect('/detail')


# Book.createTable()
if __name__ == '__main__':
    app.run('127.0.0.1', 5000, use_debugger=True, use_reloader=False)