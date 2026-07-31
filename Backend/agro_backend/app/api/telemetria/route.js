import { NextResponse } from 'next/server';
import supabase from '@/lib/db';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const dataInicio = searchParams.get('inicio');
  const dataFim = searchParams.get('fim');

  try {
    let query = supabase
      .from('telemetria_microclima')
      .select('id, temperatura, umidade, timestamp')
      .order('timestamp', { ascending: false })
      .limit(10000); 

    if (dataInicio && dataFim) {
      query = query
        .gte('timestamp', `${dataInicio}T00:00:00.000Z`)
        .lte('timestamp', `${dataFim}T23:59:59.999Z`);
    }

    const { data, error } = await query;

    if (error) {
      throw error;
    }

    return NextResponse.json({ success: true, data: data }, { status: 200 });
  } catch (error) {
    console.error("Erro ao buscar dados do Supabase:", error);
    return NextResponse.json({ success: false, message: 'Erro interno na API.' }, { status: 500 });
  }
}