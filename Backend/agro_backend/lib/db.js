import mysql from 'mysql2/promise';


const pool = mysql.createPool({
  host: 'localhost',      
  port: 3309,              
  user: 'root',            
  password: 'mysql', 
  database: 'agro_telemetria',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  timezone: 'local', 
  dateStrings: true   
});

export default pool;