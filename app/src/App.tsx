import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { useEffect } from "react"
import { Navigation } from "./components/Navigation"
import { Home } from "./pages/Home"
import { Sectors } from "./pages/Sectors"
import { Login } from "./pages/Login"
import { Company } from "./pages/Company"
import { initCompanyCache, registerCompanyCacheEvent } from "./services/companyStore"

export default function App() {
  useEffect(() => {
    // 仅初始化读取本地维护的股票池文件，不做任何更新或导出
    initCompanyCache()
    registerCompanyCacheEvent()
  }, [])
  return (
    <Router>
      <div className="min-h-screen bg-slate-900">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/*" element={
            <>
              <Navigation />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/sectors" element={<Sectors />} />
                <Route path="/company" element={<Company />} />
              </Routes>
            </>
          } />
        </Routes>
      </div>
    </Router>
  )
}
