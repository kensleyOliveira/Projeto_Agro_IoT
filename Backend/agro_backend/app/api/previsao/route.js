
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    
    const gerarDadosSimulados = () => {
      const dias = 15;
      const time = [];
      const tempMax = [];
      const tempMin = [];
      const chuva = [];

      for (let i = 0; i < dias; i++) {
        const data = new Date();
        data.setDate(data.getDate() + i);
        time.push(data.toISOString().split('T')[0]); // Formato "YYYY-MM-DD"
        
        // Temperaturas simuladas entre 26 e 32 para máxima, 15 e 19 para mínima
        tempMax.push((Math.random() * (32 - 26) + 26).toFixed(1));
        tempMin.push((Math.random() * (19 - 15) + 15).toFixed(1));
        
        // Probabilidade de chuva (0 a 100%)
        chuva.push(Math.floor(Math.random() * 100));
      }

      return {
        daily: {
          time: time,
          temperature_2m_max: tempMax,
          temperature_2m_min: tempMin,
          precipitation_probability_max: chuva
        }
      };
    };

    const mockData = gerarDadosSimulados();
    
   
    return NextResponse.json({ success: true, data: mockData }, { status: 200 });
    
  } catch (error) {
    console.error("Erro na API de previsão:", error.message);
    return NextResponse.json({ success: false, message: 'Erro interno.' }, { status: 500 });
  }
}