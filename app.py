from read_automation import create_app

# Call the application factory function to construct a Flask application
# instance using the development configuration
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
