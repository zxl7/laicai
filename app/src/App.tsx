import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import 'antd/dist/reset.css'
import { ConfigProvider, theme } from 'antd'
import { darkTokens } from './theme'
import { useEffect } from "react"
import { Navigation } from "./components/Navigation"
import { Home } from "./pages/Home"
import { Sectors } from "./pages/Sectors"
import { Login } from "./pages/Login"
import { Company } from "./pages/Company"
import { BoardLadder } from "./pages/BoardLadder"
import { initCompanyCache, registerCompanyCacheEvent } from "./services/companyStore"

export default function App() {
  useEffect(() => {
    // 仅初始化读取本地维护的股票池文件，不做任何更新或导出
    initCompanyCache()
    registerCompanyCacheEvent()
  }, [])
  return (
    <ConfigProvider theme={{ algorithm: theme.darkAlgorithm, token: darkTokens }}>
      <Router>
        <div className="min-h-screen bg-[var(--bg-base)]">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/*" element={
              <>
                <Navigation />
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/sectors" element={<Sectors />} />
                  <Route path="/company" element={<Company />} />
                  <Route path="/ladder" element={<BoardLadder />} />
                </Routes>
              </>
            } />
          </Routes>
        </div>
      </Router>
    </ConfigProvider>
  )
}
