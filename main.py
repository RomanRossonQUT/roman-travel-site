# Import the create_app function from the getaway module
from getaway import create_app

if __name__ == '__main__':
    # Create an instance of the Flask application using the create_app function
    app = create_app()
    
    # Run the Flask application on port 5001 with optional debugging
    app.run(debug=False, port=5001)
