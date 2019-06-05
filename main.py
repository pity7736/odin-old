from dotenv import load_dotenv
import uvicorn


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run(app='odin:app', host='0.0.0.0', port=8888, reload=True)
