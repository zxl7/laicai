import type { CompanyProfile } from "../api/types"
import { Tag } from "antd"
import { resolveTagColor } from "../lib/tagColors"

interface Props {
  profile: CompanyProfile
}

export function CompanyProfileCard({ profile }: Props) {
  const tags = (profile.idea || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean)
  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
      <div className="mb-2">
        <h2 className="text-xl font-semibold text-white">{profile.mc}</h2>
        <p className="text-slate-400 text-sm">{profile.ename}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        <div>
          <div className="text-slate-400 text-xs">当前价格</div>
          <div className="text-white">{profile.p}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">所属板块</div>
          <div className="text-white">{profile.hy}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">公司全称</div>
          <div className="text-white">{profile.name}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">公司地址</div>
          <div className="text-white">{profile.addr}</div>
        </div>
        <div className="md:col-span-2">
          <div className="text-slate-400 text-xs">概念及板块</div>
          <div className="flex flex-wrap gap-2 mt-2">
            {tags.length === 0 ? (
              <span className="text-slate-500 text-xs">-</span>
            ) : (
              tags.map((t) => (
                <Tag key={t} className="m-0" color={resolveTagColor(t)}>
                  {t}
                </Tag>
              ))
            )}
          </div>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-2">
        <div>
          <div className="text-slate-400 text-xs">是否异动</div>
          {/* <div className="text-amber-400 break-all">{profile.yd === "1" ? "是" : "否"}</div> */}
        </div>
        <div>
          <div className="text-slate-400 text-xs">利好</div>
          {/* <div className="text-amber-400 break-all">{profile.infosite}</div> */}
        </div>
        <div>
          <div className="text-slate-400 text-xs">利空</div>
          {/* <div className="text-white break-all">{profile.email}</div> */}
        </div>
        <div>
          <div className="text-slate-400 text-xs">信息披露</div>
          {/* <div className="text-white">{profile.phone}</div> */}
        </div>
      </div>

      <div className="mt-4">
        <div className="text-slate-400 text-xs mb-2">公司简介</div>
        <div className="text-slate-200 text-sm leading-6 whitespace-pre-line">{profile.bscope}</div>
      </div>
    </div>
  )
}
