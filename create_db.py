# Import the necessary modules from the getaway package
from getaway import db, create_app
app = create_app()
# Create an application context to work with the app's context
ctx = app.app_context()
# Push the application context so that we can work with it
ctx.push()
# Create the database tables by calling the create_all method on the db object
db.create_all()
quit()
