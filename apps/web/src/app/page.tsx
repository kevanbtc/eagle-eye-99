import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Eagle Eye AI
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Construction Plan Review & Pricing System
          </p>
        </div>

        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-3xl font-semibold text-gray-800 mb-6">
            Welcome to Eagle Eye
          </h2>
          
          <p className="text-lg text-gray-600 mb-6">
            Transform construction plan PDFs into code-cited risk reports, 
            priced estimates, and professional proposals in minutes.
          </p>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="bg-blue-50 p-6 rounded-lg">
              <h3 className="font-semibold text-lg mb-2">📋 Plan Review</h3>
              <p className="text-gray-600">
                Automated code compliance checks for IRC, IECC, NEC + GA amendments
              </p>
            </div>
            
            <div className="bg-green-50 p-6 rounded-lg">
              <h3 className="font-semibold text-lg mb-2">💰 Pricing Engine</h3>
              <p className="text-gray-600">
                TradeBase catalog with regional factors and alternates
              </p>
            </div>
            
            <div className="bg-purple-50 p-6 rounded-lg">
              <h3 className="font-semibold text-lg mb-2">📄 One-Click Reports</h3>
              <p className="text-gray-600">
                Professional PDFs and Xactimate CSV export
              </p>
            </div>
          </div>

          <div className="flex gap-4 justify-center">
            <Link 
              href="/projects/new"
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
            >
              Create New Project
            </Link>
            
            <Link 
              href="/projects"
              className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
            >
              View Projects
            </Link>
          </div>
        </div>

        <div className="max-w-4xl mx-auto mt-12 text-center text-gray-500 text-sm">
          <p>
            API: <a href="http://localhost:8000/docs" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
              http://localhost:8000/docs
            </a>
          </p>
        </div>
      </div>
    </main>
  )
}
