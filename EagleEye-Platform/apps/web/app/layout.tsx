import React from "react";
export const metadata = { title: "Eagle Eye", description: "Estimate + CRM + AI" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{fontFamily:"Inter,system-ui,Arial",margin:0}}>
        <header style={{padding:"12px 20px",borderBottom:"1px solid #eee"}}>
          <b>Eagle Eye</b> · <a href="/">Dashboard</a> · <a href="/projects">Projects</a>
        </header>
        <main style={{padding:20, maxWidth:1080, margin:"0 auto"}}>{children}</main>
      </body>
    </html>
  );
}
