from flask import Flask, render_template,url_for,request,flash,jsonify,redirect
import sqlite3
import base64

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Init db
def init_db():
      conn = sqlite3.connect('site.db')
      cursor = conn.cursor()
      cursor.execute('''
          CREATE TABLE IF NOT EXISTS posts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              description TEXT NOT NULL,
              location TEXT NOT NULL,
              latitude TEXT NOT NULL,
              longitude TEXT NOT NULL,
              name TEXT NOT NULL,
              image_data BLOB NOT NULL,
              mime_type TEXT NOT NULL,
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              type TEXT NOT NULL
          )
      ''')
      cursor.execute('''
          CREATE TABLE IF NOT EXISTS map (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            latitude TEXT NOT NULL,
            longitude TEXT NOT NULL,
            status TEXT NOT NULL
          )


      ''')
      conn.commit()
      conn.close()
      

init_db()

def get_all_data():
    # Connect to SQLite database
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    
    # Execute query to fetch all data
    cursor.execute("SELECT * FROM posts")
    
    # Fetch all rows
    data = cursor.fetchall()
    
    # Close connection
    conn.close()
    
    return data

def get_map_data():
    # Connect to SQLite database
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    
    # Execute query to fetch all data
    data = cursor.execute("SELECT description,location,status,id FROM map").fetchall()
    
    # Close connection
    conn.close()

    return (data)

def get_map_markers():
    # Connect to SQLite database
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    
    markers = cursor.execute("SELECT latitude,longitude FROM map").fetchall()
    
    # Close connection
    conn.close()

    markers_list = list()
    for row in markers:
      markers_list.append({'lat':row[0],'lon':row[1]})

    return jsonify(markers)

def estimate_co2e_reduction(tons_collected, tons_recycled):
    """
    Estimates the CO2e reduction from waste collection and recycling.

    This is a simplified, fictitious model based on assumed reduction factors.
    It is not a scientifically accurate representation.

    Args:
        tons_collected (float): The total tons of waste collected.
        tons_recycled (float): The total tons of waste recycled.

    Returns:
        float: The estimated CO2e reduction in metric tons.
    """
    
    COLLECTION_FACTOR = 0.5  # tons of CO2e per ton of collected waste
    RECYCLING_FACTOR = 2.0  # tons of CO2e per ton of recycled waste
    
    # Ensure recycled tons do not exceed collected tons
    if tons_recycled > tons_collected:
        tons_collected += 1

    # Calculate reduction from collection
    reduction_from_collection = (tons_collected - tons_recycled) * COLLECTION_FACTOR
    
    # Calculate reduction from recycling, which has a higher impact
    reduction_from_recycling = tons_recycled * RECYCLING_FACTOR
    
    total_co2e_reduction = reduction_from_collection + reduction_from_recycling
    
    return total_co2e_reduction


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report',methods=['GET','POST'])
def report():
    if request.method == 'POST':
        description = request.form['description']
        type = request.form['type']
        
        if request.form['location']:
            location = request.form['location']

        #get geolocation
        if request.form['geoAvail'] == 'No':
          flash('Geolocation is not available','error')
            
        elif request.form['geoEnabled'] == 'No':
          flash('Geolocation is not enabled','error')

        else:
          latitude = request.form['lat']
          longitude = request.form['long']

        if 'image' not in request.files:
          flash('error: No image provided','error')
    
        file = request.files['image']

        if file.filename == '':
          flash('error: No file selected','error')
    
        if file:
            # Read image data
            image_data = file.read()
            img_64 = base64.b64encode(image_data).decode('utf-8')
            mime_type = file.mimetype
            name = file.filename
            
            # Store in database
            conn = sqlite3.connect('site.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO posts (description,location,latitude,longitude,name, image_data, mime_type, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',(description,location,latitude,longitude,name, img_64, mime_type, type))
            cursor.execute('INSERT INTO map (description,location,latitude,longitude,status) VALUES (?, ?, ?, ?, ?)',(description,location,latitude,longitude,'reported'))
            conn.commit()
            conn.close()
              
        
        flash('Created successfully','success')

    return render_template('index.html')

@app.route('/posts')
def posts():
  posts = get_all_data()
  return render_template('posts.html',posts=posts)

@app.route('/map')
def map():
  data = get_map_data()
  return render_template('map.html',data=data)

@app.route('/map/markers')    
def markers():
  data = get_map_markers()
  
  return data

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/collected/<post_id>',methods=['GET','PUT'])
def collected(post_id):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    print(cursor.execute('SELECT status FROM map WHERE id=?',(post_id)).fetchone())
    cursor.execute('UPDATE map SET status= ? WHERE id=?',('Collected',post_id))
    print(cursor.execute('SELECT status FROM map WHERE id=?',(post_id)).fetchone())
    conn.commit()
    conn.close()

    return redirect('/map')


@app.route('/analytics')
def analytics():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    reported = len(cursor.execute('SELECT id FROM posts').fetchall())
    collected=len(cursor.execute("SELECT status FROM map where status = 'Collected' ").fetchall())
    plastic=len(cursor.execute("SELECT type FROM posts where type = 'Plastic' ").fetchall())
    paper=len(cursor.execute("SELECT type FROM posts where type = 'Paper' ").fetchall())
    organic=len(cursor.execute("SELECT type FROM posts where type = 'Organic' ").fetchall())
    glass=len(cursor.execute("SELECT type FROM posts where type = 'Glass' ").fetchall())
    metal=len(cursor.execute("SELECT type FROM posts where type = 'Metal' ").fetchall())
    recycled = plastic + paper + glass + metal
   

    stats = {
      'reported':reported,
      'collected': collected,
      'recycled': recycled,
      'plastic': plastic,
      'paper': paper,
      'glass': glass,
      'organic': organic,
      'metal': metal,
      'co2': estimate_co2e_reduction(collected,recycled),
      'aug': 0,
      'sep': estimate_co2e_reduction(collected,recycled) * 100,
      'oct': 0,
      'nov': 0,
      'dec': 0
    }
    conn.close()
    return render_template('analytics.html',stats=stats)

@app.route('/clear')
def dropT():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE posts')
    conn.commit()
    conn.close()

    return 'deleted hopefully'

@app.route('/map/delete')
def map_delete():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE map')
    conn.commit()
    conn.close()
    return 'Map table deleted'



if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8002, debug=True)
 