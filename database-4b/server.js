import mysql from "mysql2";
import fs from 'fs'

const pool = mysql.createPool({
    host: "sql9.freesqldatabase.com",
    user: "sql9609574",
    password: "U6JqdflMxh",
    database: "sql9609574",
    port:3306,
}).promise()

const insertIntoDB = async (pool, base64String, returnString) => {
    try {
        await pool.query(
            "UPDATE project4 SET base64String='"+base64String+"', returnString='"+returnString+"' WHERE id=0"
        );
        console.log("Updated ("+base64String+","+returnString+") in DB")
        } catch (error) {
           console.log(error)
        }
};
const getImageURL = async(pool) => {
    try {
        const [rows] = await pool.query(
            `SELECT * FROM project4`)
            console.log("Received data from DB");
            return rows[0].base64String
        } catch (error) {
            console.log(error);
        }
}  
const deleteDB = async (pool) => {
    try {
        await pool.query(
            "DELETE FROM project4"
        );
        console.log("Deleted data from DB");
        } catch (error) {
            console.log(error);
        }
}

function sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}

// call functions down here
// insertIntoDB(pool, "test from server!", "did it work?")
// deleteDB(pool)

const imageURL = await getImageURL(pool)

fs.writeFile("data", imageURL, await function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("Image URL exported for Python use!")    
    while (!fs.existsSync('response')) { // wait for python to create 'response file'
        sleep(1000);
    }
    insertIntoDB(pool, "ServerReturn", fs.readFileSync("response").toString('utf-8'));
}); 