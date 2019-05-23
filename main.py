from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    from odin import app
    app.run(host='0.0.0.0', port='8888')
