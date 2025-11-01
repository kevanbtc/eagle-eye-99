'use client';
import { useState } from 'react';
import axios from 'axios';
const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function Projects(){
  const [name,setName]=useState('New Project');
  const [account_id,setAccount]=useState('00000000-0000-0000-0000-000000000000');
  const [jurisdiction,setJ]=useState('City of Atlanta, GA');
  const [created,setCreated]=useState<any>(null);
  return (
    <div>
      <h1>Projects</h1>
      <div style={{display:'grid',gap:8,maxWidth:520}}>
        <input placeholder="Account UUID" value={account_id} onChange={e=>setAccount(e.target.value)} />
        <input placeholder="Project name" value={name} onChange={e=>setName(e.target.value)} />
        <input placeholder="Jurisdiction" value={jurisdiction} onChange={e=>setJ(e.target.value)} />
        <button onClick={async()=>{
          const r = await axios.post(`${API}/projects`,{account_id,name,jurisdiction});
          setCreated(r.data);
        }}>Create</button>
        {created && <p>Created <a href={`/projects/${created.id}`}>{created.name}</a></p>}
      </div>
    </div>
  );
}
