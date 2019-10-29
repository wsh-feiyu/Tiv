package tt.tiv.ui.activity

import android.webkit.URLUtil
import androidx.recyclerview.widget.GridLayoutManager
import kotlinx.android.synthetic.main.activity_livept.*
import org.jetbrains.anko.startActivity
import tt.tiv.R
import tt.tiv.adapter.LiveZbAdapter
import tt.tiv.base.BaseActivity
import tt.tiv.model.LivePtItem
import tt.tiv.model.LiveUrl
import tt.tiv.model.LiveZbBean
import tt.tiv.presenter.impl.LiveZbPresenterImpl
import tt.tiv.presenter.interf.LiveZbPresenter
import tt.tiv.view.LiveZbView

class LiveZbActivity : BaseActivity(), LiveZbView {
    val adapter by lazy { LiveZbAdapter() }
    var url:String?=null
    override fun onLoad(result: LiveZbBean) {
        refre_layout.isRefreshing=false
        adapter.updataList(result)
        adapter.listener={
            startActivity<LivePlayActivity>("url" to it.address)
        }
    }

    override fun onErr(msg: String?) {
        refre_layout.isRefreshing=false
        myToast("获取数据失败")
    }

    val presenter by lazy { LiveZbPresenterImpl(this) }
    override fun getLayoutId(): Int {
        return R.layout.activity_livept
    }

    override fun initData() {
        val urlEnd=intent?.getParcelableExtra<LivePtItem>("data")?.address
        url=LiveUrl.LIVE1+urlEnd
        presenter.initdata(url!!)

    }

    override fun initListener() {
        recycler.layoutManager=GridLayoutManager(this,3)
        recycler.adapter=adapter

        refre_layout.setOnRefreshListener { presenter.initdata(url!!) }
    }
}
