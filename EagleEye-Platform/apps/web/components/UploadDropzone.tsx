'use client';
import { useState } from 'react';
import axios from 'axios';
const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function UploadDropzone({ projectId }: { projectId: string }){
  const [file,setFile]=useState<File|null>(null);
  const [msg,setMsg]=useState<string>('');
  return (
    <div style={{border:'2px dashed #999',padding:16,borderRadius:8}}>
      <input type="file" onChange={e=>setFile(e.target.files?.[0]||null)} />
      <button disabled={!file} onClick={async()=>{
        const fd = new FormData();
        if(file) fd.append('f', file);
        const r = await axios.post(`${API}/files/${projectId}`, fd, { headers: { 'Content-Type': 'multipart/form-data' }});
        setMsg(`Uploaded: ${r.data.path}`);
      }}>Upload</button>
      {msg && <p>{msg}</p>}
    </div>
  );
}
