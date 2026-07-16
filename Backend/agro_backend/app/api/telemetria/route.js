
import { NextResponse } from 'next/server';
import pool from '@/lib/db';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const dataInicio = searchParams.get('inicio');
  const dataFim = searchParams.get('fim');

  try {
    let query = `SELECT id, temperatura, umidade, timestamp FROM telemetria_microclima`;
    let queryParams = [];

    if (dataInicio && dataFim) {
      query += ` WHERE timestamp BETWEEN ? AND ?`;
      queryParams.push(`${dataInicio} 00:00:00`, `${dataFim} 23:59:59`);
    }

    query += ` ORDER BY timestamp DESC LIMIT 5000`;

    const [rows] = await pool.query(query, queryParams);

    return NextResponse.json({ success: true, data: rows }, { status: 200 });
  } catch (error) {
    console.error("Erro ao buscar dados do MySQL:", error);
    return NextResponse.json({ success: false, message: 'Erro interno.' }, { status: 500 });
  }
}