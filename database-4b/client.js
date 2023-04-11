import mysql from "mysql2";
import fs from 'fs'

const pool = mysql.createPool({
    host: "sql9.freesqldatabase.com",
    user: "sql9609574",
    password: "U6JqdflMxh",
    database: "sql9609574",
    port:3306,
}).promise()

const getImageURL = async(pool) => {
    try {
        const [rows] = await pool.query(
            `SELECT * FROM distrowebscraper`)
            console.log("Received data from DB");
            return rows
        } catch (error) {
            console.log(error);
        }
}

fs.writeFile("partialURLs", getImageURL(), function(err) {
    if(err) {
        return console.log(err);
    }
    });