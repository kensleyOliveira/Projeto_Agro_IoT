import mysql from 'mysql2/promise';

// Configuração do pool de conexões corrigida para fuso horário local
const pool = mysql.createPool({
  host: '192.168.1.110',      
  user: 'root',            
  password: 'mysql',   
  database: 'agro_telemetria',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  
  // 👇 ADICIONE ESTAS DUAS LINHAS ABAIXO:
  timezone: '-03:00', // Força o fuso horário de Brasília (UTC-3)
  dateStrings: true   // Evita que o Node.js tente converter e distorcer as datas
});

export default pool;