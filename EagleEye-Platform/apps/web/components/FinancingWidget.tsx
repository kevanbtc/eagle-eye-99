'use client';
import { useState, useMemo } from 'react';

export default function FinancingWidget({ amount }: { amount: number }){
  const [apr,setApr]=useState(0.08);
  const [term,setTerm]=useState(24);
  const payment = useMemo(()=>{
    const r = apr/12; if(!amount||!term) return 0; if(r===0) return amount/term;
    return amount*(r*Math.pow(1+r,term))/(Math.pow(1+r,term)-1);
  },[amount,apr,term]);
  return (
    <div style={{border:'1px solid #eee',padding:12,borderRadius:8}}>
      <div style={{display:'flex',gap:12,alignItems:'center'}}>
        <label>Amount</label><input value={amount.toFixed(2)} readOnly />
        <label>APR</label><input type="number" step="0.01" value={apr} onChange={e=>setApr(parseFloat(e.target.value))} />
        <label>Term (mo)</label><input type="number" value={term} onChange={e=>setTerm(parseInt(e.target.value))} />
      </div>
      <p style={{marginTop:8}}><b>Est. Payment:</b> ${payment.toFixed(2)}/mo</p>
    </div>
  );
}
