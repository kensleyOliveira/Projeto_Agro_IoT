import mysql from 'mysql2/promise';

const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',      
  port: parseInt(process.env.DB_PORT || '3309', 10),              
  user: process.env.DB_USER || 'root',            
  password: process.env.DB_PASSWORD || 'mysql', 
  database: process.env.DB_NAME || 'agro_telemetria',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  timezone: 'Z', // Configuração ideal para lidar com DATETIME e fuso-horários globais
  dateStrings: true   
});

export default pool;