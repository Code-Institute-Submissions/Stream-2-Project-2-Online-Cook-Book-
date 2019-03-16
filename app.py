from flask import Flask, render_template, request, redirect, flash
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL
import yaml
app = Flask(__name__)
app.secret_key = "secret_key"


Bootstrap(app)
mysql = MySQL(app)

# MySQL configurations
db = yaml.load(open('db.yaml'))
app.config['MYSQL_DATABASE_USER'] = db['mysql_user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DATABASE_DB'] = db['mysql_db']
app.config['MYSQL_DATABASE_HOST'] = db['mysql_host']
mysql.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/course/<string:title>')
def get_recipe(title):
    conn = mysql.connect()
    cur = conn.cursor()
    total = cur.execute("SELECT * FROM recipe WHERE course = %s", (title))
    if total > 0:
        recipe = cur.fetchall()
        conn.close()
        return render_template('home.html', recipe=recipe)
    else:
        return render_template('home.html', recipe=None)

@app.route('/dietry/<int:dietry>')
def get_recipe_by_dietry(dietry):
    conn = mysql.connect()
    cur = conn.cursor()
    total = cur.execute("SELECT * FROM recipe r, recipe_dietry d WHERE d.recipe_id = r.id and d.dietry_id= %s ", (dietry))
    if total > 0:
        recipe = cur.fetchall()
        conn.close()
        return render_template('home.html', recipe=recipe, dietry_id = dietry)
    else:
        flash("No recipes found by this filter",'danger')
        return render_template('home.html', recipe=None)




@app.route('/')
def index():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipe")
    recipes = cur.fetchall()
    conn.close()

    return render_template('home.html',recipe = recipes)





@app.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("UPDATE recipe SET views = views+1 WHERE id = %s", (recipe_id))
    conn.commit()
    cur.execute("SELECT * FROM recipe WHERE id = %s",(recipe_id))
    recipe = cur.fetchone()
    conn.close()

    return render_template('recipe.html',recipe = recipe)

@app.route('/upvote/<int:recipe_id>')
def upvote_recipe(recipe_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("UPDATE recipe SET upvotes = upvotes+1 WHERE id = %s",(recipe_id))
    conn.commit()
    cur.execute("SELECT * FROM recipe WHERE id = %s", (recipe_id))
    recipe = cur.fetchone()
    conn.close()
    flash("Successfully Upvoted",'success')
    return render_template('recipe.html',recipe = recipe)


@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM recipe_dietry WHERE recipe_id = %s", (recipe_id))
    conn.commit()
    cur.execute("DELETE FROM recipe WHERE id = %s",(recipe_id))
    conn.commit()
    conn.close()
    flash("Successfully Deleted Recipe", 'success')
    return redirect('/')




@app.route('/submit',methods = ['GET','POST'])
def submit_recipe():
    if request.method=="POST":
        form = request.form
        title = form['title']
        ingredients = form['ingredients']
        instructions = form['instructions']
        authors = form['author']
        author_country = form['country']
        course = form['course']
        dietry = form.getlist('dietry')
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO recipe(title,ingredients,instructions,authors,author_country,course) VALUES(%s,%s,%s,%s,%s,%s)",(title,ingredients,instructions,authors,author_country,course))
        conn.commit()

        id = cur.lastrowid
        for diet in dietry:
            cur.execute(
                "INSERT INTO recipe_dietry(recipe_id,dietry_id) VALUES(%s,%s)",
                (id, diet))
            conn.commit()

        conn.close()
        flash("Successfully Added", 'success')
        return redirect('/')

    else:
        return render_template('submit.html')

@app.route('/edit/<int:recipe_id>',methods = ['GET','POST'])
def edit_recipe(recipe_id):
    if request.method=="POST":
        form = request.form
        title = form['title']
        ingredients = form['ingredients']
        instructions = form['instructions']
        authors = form['author']
        author_country = form['country']
        course = form['course']
        dietry = form.getlist('dietry')
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("UPDATE recipe SET title = %s ,ingredients = %s ,instructions = %s, authors  = %s,author_country = %s,course = %s WHERE id= %s",(title,ingredients,instructions,authors,author_country,course, recipe_id))
        conn.commit()
        cur.execute("DELETE FROM recipe_dietry WHERE recipe_id = %s",(recipe_id))
        conn.commit()

        for diet in dietry:
            cur.execute("INSERT INTO recipe_dietry(recipe_id,dietry_id) VALUES(%s,%s)",(recipe_id, diet))
            conn.commit()

        total = cur.execute("SELECT * FROM recipe where id = %s", (recipe_id))
        if total > 0:
            recipe = cur.fetchone()
            total = cur.execute("SELECT * FROM recipe_dietry where recipe_id = %s", (recipe_id))
            if total > 0:
                dietry = cur.fetchall()
                di = ""
                for diet in dietry:
                    di += str(diet[2])
                    di += ","
                flash("Successfully Updated", 'success')
                return render_template('edit.html', recipe=recipe, dietry_se=di)
            else:
                flash("Error Updating Recipe", 'danger')
                return render_template('edit.html', recipe=recipe, dietry_sel="None")
        conn.close()
    else:
        conn = mysql.connect()
        cur = conn.cursor()
        total = cur.execute("SELECT * FROM recipe where id = %s",(recipe_id))
        if total > 0:
            recipe = cur.fetchone()
            total = cur.execute("SELECT * FROM recipe_dietry where recipe_id = %s", (recipe_id))
            if total > 0:
                dietry = cur.fetchall()
                di = ""
                for diet in dietry:
                    di+= str(diet[2])
                    di+= ","

                return render_template('edit.html',recipe = recipe, dietry_se = di)
            else:
                return render_template('edit.html', recipe=recipe, dietry_sel="None")
