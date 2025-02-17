from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from typing import List, Optional


app = FastAPI()


def get_db_connection():
    connection = pymysql.connect(
        host='localhost',  
        user='root',       
        password='yourpassword',  
        db='project',     
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


class User(BaseModel):
    name: str
    lastname: str
    age: int
    contact: str
    gender: List[str]  


@app.post("/add/")
async def add_user(user: User):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO emp (name, lastname, age, contact, gender) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user.name, user.lastname, user.age, user.contact, ",".join(user.gender)))
        connection.commit()
        return {"message": "User added successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()


@app.put("/update/{user_id}")
async def update_user(user_id: int, user: User):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """
        UPDATE emp SET name=%s, lastname=%s, age=%s, contact=%s, gender=%s
        WHERE id=%s
        """
        cursor.execute(query, (user.name, user.lastname, user.age, user.contact, ",".join(user.gender), user_id))
        connection.commit()
        return {"message": "User updated successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()


@app.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM emp WHERE id=%s"
        cursor.execute(query, (user_id,))
        connection.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()


@app.get("/show/")
async def show_users():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM emp"
        cursor.execute(query)
        users = cursor.fetchall()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()
