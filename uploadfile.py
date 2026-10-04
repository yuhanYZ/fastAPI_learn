from fastapi import FastAPI, File, UploadFile
import uvicorn
app=FastAPI()
# 方式一：bytes —— 整个文件读进内存，只适合小文件
@app.post("/small")
async def upload_small(file: bytes = File()):
    return {
        "size":len(file)
    }

@app.post("/count")
async def count_words(file: bytes = File()):
    text = file.decode("utf-8")      # 字节 → 字符串
    return {
        "字节数": len(file),
        "字符数": len(text),
        "内容预览": text[:20],
    }
if __name__=='__main__':
    uvicorn.run("uploadfile:app", host='127.0.0.1', port=8000,reload=True)