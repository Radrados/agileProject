from app import app
# To run flask: flask run
# To run flask app in development mode: python main.py

if __name__ == '__main__':
    app.run(debug=True)  # Developement mode allows realtime changes in webserver

