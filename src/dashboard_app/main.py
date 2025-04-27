from app_factory import create_app

# Crear la aplicación
app, data = create_app()

if __name__ == "__main__":
    app.run(debug=True)

