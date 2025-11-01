'use client';
import { useRef, useState, useEffect } from 'react';
import axios from 'axios';
import UploadDropzone from '../../../components/UploadDropzone';
import FinancingWidget from '../../../components/FinancingWidget';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function ProjectPage({ params }: any){
  const { id } = params;
  const [est,setEst] = useState<any>(null);
  const [findings,setFindings] = useState<any[]>([]);
  useEffect(()=>{
    (async()=>{
      const e = await axios.get(`${API}/estimates/${id}`);
      setEst(e.data.payload);
      const f = await axios.get(`${API}/estimates/${id}/findings`);
      setFindings(f.data);
    })();
  },[id]);

  return (
    <div>
      <h1>Project</h1>
      <UploadDropzone projectId={id} />
      <div style={{marginTop:16}}>
        <button onClick={async()=>{
          const r = await axios.post(`${API}/estimates/${id}/quick`,{});
          setEst(r.data.payload);
          const f = await axios.get(`${API}/estimates/${id}/findings`);
          setFindings(f.data);
        }}>Generate Quick Estimate</button>
      </div>

      <h2 style={{marginTop:24}}>Estimate</h2>
      {est ? (
        <pre style={{background:'#f8f8f8',padding:12}}>{JSON.stringify(est,null,2)}</pre>
      ) : <p>No estimate yet.</p>}

      <h2>Findings</h2>
      <ul>
        {findings.map(f=> (
          <li key={f.id}><b>{f.severity.toUpperCase()}</b> · {f.discipline} · {f.location} · <i>{f.code_citation}</i><br/>{f.recommendation}</li>
        ))}
      </ul>

      <h2>Financing</h2>
      <FinancingWidget amount={est?.summary?.total || 0} />
    </div>
  );
}
