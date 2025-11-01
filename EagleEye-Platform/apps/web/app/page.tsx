'use client';
import useSWR from 'swr';
import axios from 'axios';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
const fetcher = (url:string)=>axios.get(url).then(r=>r.data);

export default function Dashboard(){
  const { data } = useSWR(`${API}/projects`, fetcher);
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Quick glance at recent projects.</p>
      <ul>{(data||[]).slice(0,5).map((p:any)=> (<li key={p.id}><a href={`/projects/${p.id}`}>{p.name}</a></li>))}</ul>
    </div>
  );
}
