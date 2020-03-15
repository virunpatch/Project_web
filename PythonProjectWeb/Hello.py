from flask import Flask , render_template,request,redirect,url_for
import pymysql
#from flask import render_template
app = Flask(__name__)
conn=pymysql.connect('localhost','root','','customerdb')

@app.route("/admin") #ส่วนของAdmin
def showData():
    with conn:
        cur=conn.cursor()
        cur.execute("select * from customer")
        rows=cur.fetchall()
        return render_template('index.html',datas=rows)

@app.route("/customer") #หน้าบันทึกข้อมูล
def showForm():

    return render_template('addcustomer.html')

@app.route("/delete/<string:id_data>",methods=['GET']) #ลบข้อมูล
def delete(id_data):
    with conn:
        cur=conn.cursor()
        cur.execute("delete from customer where id=%s",(id_data))
        conn.commit()
    return redirect(url_for('showData'))

@app.route("/insert",methods=['POST']) #รับค่า
def insert():
    if request.method=="POST":
        fname=request.form['fname']
        message=request.form['message']
        Phone=request.form['phone']
        Mail=request.form['mail']
        with conn.cursor() as cursor:
            sql=" insert into `customer` (`fname`,`message`,`phone`,`mail`) values(%s,%s,%s,%s)"
            cursor.execute(sql,(fname,message,Phone,Mail))
            conn.commit()
        return redirect(url_for('home'))

@app.route("/update",methods=['POST']) #หน้าอัปเดทผู้ใช้ของAdmin
def update():
    if request.method=="POST":
        id_update=request.form['id']
        fname=request.form['fname']
        message=request.form['message']
        Phone=request.form['phone']
        Mail=request.form['mail']
        with conn.cursor() as cursor:
            sql=" update customer set fname=%s, message=%s ,phone=%s, mail=%s where id=%s "
            cursor.execute(sql,(fname,message,Phone,Mail,id_update))
            conn.commit()
        return redirect(url_for('showData'))

@app.route("/") #หน้าHome
def home():
        return render_template('home.html')


@app.route("/addboard") #หน้าเพิ่มBoard
def addboard():

    return render_template('addboard.html')


@app.route("/boardlist")  # หน้าชื่อBoard
def boardlist():
    with conn:
        cur = conn.cursor()
        cur.execute("select * from board")
        rows = cur.fetchall()

        return render_template('boardlist.html', datas=rows)


@app.route("/insert_b", methods=['POST'])  # รับค่ากระทู้
def insert_b():
    if request.method == "POST":
        name = request.form['name']
        texts = request.form['texts']
        with conn.cursor() as cursor:
            sql = " insert into `board` (`name`,`texts`) values(%s,%s)"
            cursor.execute(sql, (name, texts))
            conn.commit()
        return redirect(url_for('boardlist'))


@app.route("/insert_c", methods=['POST'])  # รับค่าคอมเมนต์
def insert_c():
    if request.method == "POST":
        board_id = request.form['board_id']
        comment = request.form['comment']
        with conn.cursor() as cursor:
            sql = " insert into `comment` (`board_id`,`comment`) values(%s,%s)"
            cursor.execute(sql, (board_id, comment))
            conn.commit()
        return redirect(url_for('board'))


"""@app.route("/board", methods=['POST'])  # หน้าBoard
def board():
    if request.method == "POST":
        name = request.form['id']
        with conn.cursor() as cursor:
            select_stmt = "SELECT * FROM employees WHERE board_id = %(id)s"
            cur = conn.cursor()
            cur.execute(select_stmt, {'id': id})
            rows = cur.fetchall()
        return render_template('board.html', datas=rows)"""


@app.route("/board")  # หน้าBoard
def board():
    with conn:
        cur = conn.cursor()
        cur.execute(
            "select board.id,board.name,board.texts,board.date,comment.comment,comment.date from comment right join board on board.id=comment.board_id order by board.id")
        rows = cur.fetchall()
        return render_template('board.html', datas=rows)

if __name__ == "__main__":
    app.run(debug=True)
