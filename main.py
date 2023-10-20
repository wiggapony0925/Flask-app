from website import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)   # Every time we make a change it'll rerun the server 
    
    
     