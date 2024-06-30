from ext import app

if __name__ == "__main__":
    from routes import register, login, index, logout, product
    app.run(debug=True)




