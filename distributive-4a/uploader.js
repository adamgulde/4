import mysql from "mysql2";
import fs from 'fs'

const pool = mysql.createPool({
    host: "sql9.freesqldatabase.com",
    user: "sql9609574",
    password: "U6JqdflMxh",
    database: "sql9609574",
    port:3306,
}).promise()

export const insertIntoDB = async (posID) => {
    try {
        await pool.query(
            "INSERT INTO distrowebscraper (positiveID) VALUES ("+posID+")"
        );
        console.log("Inserted ("+posID+") into DB");
    } catch (error) {
        console.log(error);
    }
};
function main() {
    let positiveIDs = fs.readFileSync("data").toString().split('\n').forEach(
        function(entry) {
            if(entry!=''){
                insertIntoDB(entry)
            }
        }
    );
}
main();