import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os.path
from werkzeug import secure_filename
import random
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['mpeg', 'ogg', 'mp3', 'wav'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
           
@app.route('/')
@app.route('/Library', methods = ['GET', 'POST'])
def library():
    f = open("Public", "r")
    f2 = f.read()
    f.close()
    try:
        f4 = request.url
        f5 = f4.split("?")
        f6 = f5[1].split("&user&password")
        f = open(f6[0], "r")
        f7 = f.read()
        f8 = f7.split("<!>")
        f.close()
        if f6[1] == f8[2]:
            f = open(f6[0] + ".lib", "r")
            f3 = f.read()
            f.close()
        else:
            f3 = "Wrong Password"    
    except:
        f3 = "You aren't signed in"    
    return render_template('hello.html', tunes=f2, mytunes=f3)


@app.route('/buy/<user>/<password>/<id1>')
def buy(user, password, id1):
    url = "?%s&user&password%s" % (user, password)
    f = open(user, "r")
    f2 = f.read()
    f.close()
    f3 = f2.split("<!>")
    if password == f3[2]:
        f = open(id1 + ".cost", "r")
        f4 = f.read()
        f5 = f4.split("<!>")
        f.close()
        f = open(id1, "r")
        f6 = f.read()
        f.close()
        if f3[4] >= f5[1]:
            f = open(user, "w")
            left = int(f3[4]) - int(f5[1])
            g = "<!>"
            f.write(g + user + g + f3[2] + g + f3[3] + g + str(left) + g)
            f.close()
            f = open(user + ".lib", "a+")
            f.write(f6)
            f.close()
            f = open(id1 + ".payment", "a+")
            f.write("\n" + f5[1] + "\n")
            f.close()          
            return """
            <body onload='alert("Purchase Success!"); window.location.href = "/%s"'>
            """ % url
        else:
            return """
                <body onload='alert("Insufficient Balance, it costs $%s but you only have $%s"); window.location.href = "/%s"'>
                """ % (f5[1], f3[4], url)
    else:               
        return """
                <body onload='alert("Incorrect Passcode!"); window.location.href = "/%s"'>
                """ % url                       
                
@app.route('/album/<albumt>')
def album(albumt): 
    f4 = request.url
    f5 = f4.split("?")
    f6 = f5[1].split("&user&password")
    print f6[0], f6[1]
    f = open(f6[0], "r")
    f7 = f.read()
    f8 = f7.split("<!>")
    f.close()
    if f6[1] == f8[2]:
        a = f8[4] 
    else:   
        a = "0 (Not signed in)"
    try:
        f = open(albumt + ".artist", "r")
        f2 = f.read()
        f.close()
    except:    
        f2 = "Album doesn't exist!"   
    return render_template('album.html', page=f2, amount=a)
    
@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('hello.html')
    elif request.method == 'POST':
        name = request.form['name']
        mail = request.form['email']
        ps = request.form['pass']
        a = os.path.isfile(name)
        b = "<!>"
        fg = "hello"
        url = "?%s&user&password%s" % (name, ps)
        if a == False:
            f = open(name, "w")
            f.write(b + name + b + ps + b + mail + b + "0" + b)
            f.close()
            f = open(name + '.lib', "w")
            return """
            <body onload='alert("Account Created Successfully!"); window.location.href = "/%s"'>
            """ % url
            f.close()
            
        if a == True:
            return """
            <body onload='alert("Account Already Exists!"); window.location.href = "/"'>   
            """ 
        
@app.route('/redeem/<t>/<usr>/<pswd>', methods = ['GET', 'POST'])
def redeem(t, usr, pswd):
    if request.method == 'GET':
        return render_template('base.html')
    elif request.method == 'POST':
        code = request.form['code']
        url = '?%s&user&password%s"' % (usr, pswd)
        f = open(usr, "r")
        f2 = f.read()
        f.close()
        f4 = f2.split("<!>")
        if pswd == f4[2]: 
            tw = "<!>%s<!>%s<!>%s<!>" % (usr, pswd, f4[3])
            try:
                f = open(code, "r+")
                f5 = f.read()
                f6 = f5.split("<!>")
                f.truncate()
                f.write("This Code has been used$#%$.")
                f.close()
                if '$#%$' in f5:
                    return "<body onload='" + 'alert("Code has already been redeemed, go back?"); window.location.href = "/' + url + ";'>"                 
                else:
                    fs = open(usr, "w")
                    i1 = int(f4[4])
                    i2 = int(f6[1])
                    fs.write(tw + str(i1 + i2) + "<!>")
                    fs.close()
                    return "<body onload='" + 'alert("Code Redeemed, You now have added $' + f6[1] + ' to your account."); window.location.href = "/' + url + "'>"
                
                        
            except:
                return "<body onload='" + 'alert("Code does not exist, go back?"); window.location.href = "/' + url + "'>"                

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    user = request.form['artist']
    ps = request.form['apass']
    typ = request.form['type']
    aname = request.form['artistname']
    cost = request.form['cost']
    songname = request.form['songname']
    des = request.form['des']
    url = "album?%s&user&password%s" % (user, ps)
    if cost == "":
        cost = "0"
    song = '<audio class="my_audio" controls><source src="http://127.0.0.1:9000/uploads/%s" type="audio/%s"></audio>' % (file.filename, typ)     
    f = open(user, "r")
    f2 = f.read()
    f.close()
    f3 = f2.split("<!>")
    num = random.randint(0, 8000)
    if ps == f3[2]:
        a = os.path.isfile(str(num))
        f = open(str(num) + ".payment", "w")
        f.write("Pay " + user + ":\n\n")
        f.close()
        if a == False:
            f = open(str(num), "w")
            cst = open(str(num) + ".cost", "w")
            cst.write("<!>" + cost + "<!>")
            cst.close()
            content = """
            <div class="song">
            <h1>%s:%s</h1>
            <p>%s</p>     
            </div>       
            """ % (aname, songname, song)
            f.write(content)
            f.close()
            f = open(user + ".lib", "a+")
            f.write(content)
            f.close()
        else:
            num = random.randint(0, 8000)    
            f = open(str(num), "w")
            cst = open(str(num) + ".cost", "w")
            cst.write("<!>" + cost + "<!>")
            cst.close()
            content = """
            <div class="song">
            <h1>%s:%s</h1>
            <p>%s</p>     
            </div>       
            """ % (aname, songname, song)
            f.write(content)
            f.close()
        f = open(aname + ".artist", "w")
        f.close()    
        f = open(aname + ".artist", "r+")
        s = f.read()
        f.seek(0)
        if cost != "0":
            song = "You must first purchase this content before you can listen to it."
        content = """
        <div class="c">
        <h1>Artist: %s</h1>
        <h2>Song: %s</h2>
        <p>%s</p>  
        <p>Cost: $%s</p><button class="button button2" onclick="add_id('%s')">Buy</button>
        <p>Description:<br>%s</p>
        <p>Uploaded by: %s</p> 
        </div>       
        """ % (aname, songname, song, cost, str(num), des, user)
        f.write(content + s)
        f.close()
        f = open("Public", "r+")
        s2 = f.read()
        f.seek(0)
        f.write(content + s2)
        f.close()
        if file and allowed_file(file.filename):
        
            filename = secure_filename(file.filename)
   
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
   
            return redirect(url_for('album2', albumtl=aname, usr=url))

@app.route('/album2/<albumtl>/<usr>')
def album2(albumtl, usr): 
    f4 = request.url
    f5 = f4.split("%3F")
    f6 = f5[1].split("&user&password")
    f = open(f6[0], "r")
    f7 = f.read()
    f8 = f7.split("<!>")
    f.close()
    if f6[1] == f8[2]:
        a = f8[4] 
    else:   
        a = "0 (Not signed in)"
    try:
        f = open(albumtl + ".artist", "r")
        f2 = f.read()
        f.close()
    except:    
        f2 = "Album doesn't exist!"   
    return render_template('album.html', page=f2, amount=a)
    
@app.route('/admin/<adpas>', methods = ['GET', 'POST'])
def admin(adpas):
    if request.method == 'GET':
        f = open("admin", "r")
        f2 = f.read()
        f3 = f2.split("<!>")
        f.close()
        if adpas == f3[1]:
            return render_template("form.html")
        else:
            return "Admin Login failed..."    
    elif request.method == 'POST':
        f = open("admin", "r")
        f2 = f.read()
        f3 = f2.split("<!>")
        f.close()
        if adpas == f3[1]:
            this = request.form['val']
            alphabet2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            alphabet3 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']    
            alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            key_1 = random.randint(0,25)
            key_letter_1 = alphabet[key_1]
            key_2 = random.randint(0,25)
            key_letter_2 = alphabet3[key_2]    
            key_3 = random.randint(0,9)
            key_number_1 = numbers[key_3]
            key_4 = random.randint(0,9)
            key_number_2 = numbers[key_4]
            key_5 = random.randint(0,9)    
            key_number_3 = numbers[key_5]    
            key_6 = random.randint(0,25)    
            key_letter_3 = alphabet3[key_6]
            key_7 = random.randint(0,25)
            key_letter_4 = alphabet[key_7]
            key_8 = random.randint(0,25)
            key_letter_5 = alphabet3[key_8] 
            key_9 = random.randint(0,9)
            key_number_4 = numbers[key_9]
            key_10 = random.randint(0,9)
            key_number_5 = numbers[key_10]    
            key_11 = random.randint(0,61)
            key_letter_6 = alphabet2[key_11]
            key_12 = random.randint(0,61)
            key_letter_7 = alphabet2[key_12]    
            key_13 = random.randint(0,61)
            key_number_6 = alphabet2[key_13]
            key_14 = random.randint(0,61)
            key_number_7 = alphabet2[key_14]
            key_15 = random.randint(0,61)    
            key_number_8 = alphabet2[key_15]    
            key_16 = random.randint(0,61)    
            key_letter_8 = alphabet2[key_16]
            key_17 = random.randint(0,61)
            key_letter_9 = alphabet2[key_17]
            key_18 = random.randint(0,61)
            key_letter_10 = alphabet2[key_18] 
            key_19 = random.randint(0,61)
            key_number_9 = alphabet2[key_19]
            key_20 = random.randint(0,61)
            key_number_10 = alphabet2[key_20] 
            keys = key_letter_1 + key_letter_2 + key_number_1 + key_number_2 + key_number_3 + key_letter_3 + key_letter_4 + key_letter_5 + key_number_4 + key_number_5 + key_letter_6 + key_letter_7 + key_number_6 + key_number_7 + key_number_8 + key_letter_8 + key_letter_9 + key_letter_10 + key_number_9 + key_number_10
            f = open(keys, 'w') 
            f.write("<!>" + this + "<!>")
            f.close()
            return "The Key: %s<br>The Value: $%s" % (keys, this)
        else:
            return "Admin Login failed..."            
            

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=9000)
