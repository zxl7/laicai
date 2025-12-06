import type { CompanyProfile } from '../api/types'

interface Props {
  profile: CompanyProfile
}

export function CompanyProfileCard({ profile }: Props) {
  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-white">{profile.name}</h2>
        <p className="text-slate-400 text-sm">{profile.ename}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <div className="text-slate-400 text-xs">上市市场</div>
          <div className="text-white">{profile.market}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">上市日期</div>
          <div className="text-white">{profile.ldate}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">发行价格</div>
          <div className="text-white">{profile.sprice}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">主承销商</div>
          <div className="text-white">{profile.principal}</div>
        </div>
        <div className="md:col-span-2">
          <div className="text-slate-400 text-xs">概念及板块</div>
          <div className="text-white">{profile.idea}</div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <div className="text-slate-400 text-xs">公司网站</div>
          <div className="text-amber-400 break-all">{profile.site}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">信息披露网址</div>
          <div className="text-amber-400 break-all">{profile.infosite}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">公司邮箱</div>
          <div className="text-white break-all">{profile.email}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">联系电话</div>
          <div className="text-white">{profile.phone}</div>
        </div>
      </div>

      <div className="mt-6">
        <div className="text-slate-400 text-xs mb-2">公司简介</div>
        <div className="text-slate-200 text-sm leading-6 whitespace-pre-line">
          {profile.desc}
        </div>
      </div>
    </div>
  )
}
