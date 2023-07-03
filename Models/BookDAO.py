class BookDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "books"

    def delete(self, id):
        q = self.db.query(f"DELETE FROM @table where id={id}")
        self.db.commit()

        return q

    def reserve(self, user_id, book_id):
        if not self.available(book_id):
            return "err_out"

        q = self.db.query(f"INSERT INTO reserve (user_id, book_id) VALUES('{user_id}', '{book_id}');")

        self.db.query(f"UPDATE @table set count=count-1 where id={book_id};")
        self.db.commit()

        return q

    def getBooksByUser(self, user_id):
        q = self.db.query(
            f"select * from @table left join reserve on reserve.book_id = @table.id where reserve.user_id={user_id}")

        books = q.fetchall()

        print(books)
        return books

    def getBooksCountByUser(self, user_id):
        q = self.db.query(
            f"select count(reserve.book_id) as books_count from @table left join reserve on reserve.book_id = @table.id"
            f" where reserve.user_id={user_id}")

        books = q.fetchall()

        print(books)
        return books

    def getBook(self, id):
        q = self.db.query("select * from @table where id={}".format(id))

        book = q.fetchone()

        print(book)
        return book

    def available(self, id):
        book = self.getById(id)
        count = book['count']

        if count < 1:
            return False

        return True

    def getById(self, id):
        q = self.db.query(f"select * from @table where id='{id}'")

        book = q.fetchone()

        return book

    def list(self, availability=1):
        query = "select * from @table"
        # Usually when no-admin user query for book
        if availability == 1:
            query = query + f"  WHERE availability={availability}"

        books = self.db.query(query)

        books = books.fetchall()

        return books

    def getReserverdBooksByUser(self, user_id):
        query = f"select concat(book_id,',') as user_books from reserve WHERE user_id={user_id}"

        books = self.db.query(query)

        books = books.fetchone()

        return books

    def search_book(self, name, availability=1):
        query = f"select * from @table where name LIKE '%{name}%'"

        # Usually when no-admin user query for book
        if availability == 1:
            query = query + "  AND availability={}".format(availability)

        q = self.db.query(query)
        books = q.fetchall()

        return books
