from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

def next_number():
    for i in range(1,101):
        yield i
next_id = next_number()

@app.route("/")
def web_home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    user_id = next(next_id)
    with open('database.txt', mode='a') as db:
        db.write(f"\nUserID - {user_id}\n")
        for item in data:
            db.write(f"{item}: {data.get(item)}\n")
        db.close()

def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as db2:
        user_id = next(next_id)
        email = data['email']
        subject = data['subject']
        message = data['message']

        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, )
        csv_writer.writerow([user_id,email,subject,message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('thankyou.html')
        except:
            return "Data not saved"
    else:
        "Please try again"