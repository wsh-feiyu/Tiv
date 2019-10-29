package tt.tiv.ui.activity

import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import kotlinx.android.synthetic.main.activity_livept.*
import org.jetbrains.anko.startActivity
import tt.tiv.R
import tt.tiv.adapter.LivePtAdapter
import tt.tiv.base.BaseActivity
import tt.tiv.model.LivePtBean
import tt.tiv.presenter.impl.LivePtPresenterImpl
import tt.tiv.view.LivePtView

/**
 * @ClassName: LivePtActivity
 * @Description: live pt 列表
 * @Author: wsh
 * @Date: 19-10-28 上午11:06
 */
class LivePtActivity :BaseActivity(), LivePtView {
    val persenter by lazy { LivePtPresenterImpl(this) }
    val adapter by lazy { LivePtAdapter() }
    var url:String?=null

    override fun getLayoutId(): Int {
        return R.layout.activity_livept
    }

    override fun initData() {
        val liveUrl = intent.getStringExtra("url")
        url=liveUrl
        persenter.initdata(liveUrl)
    }

    override fun onLoad(result: LivePtBean) {
        refre_layout.isRefreshing=false
        adapter.updataList(result)
        adapter.listener={
            startActivity<LiveZbActivity>("data" to it)
        }
    }

    override fun onErr(msg: String?) {
        refre_layout.isRefreshing=false

        myToast("获取数据失败")
    }

    override fun initListener() {
        recycler.layoutManager=GridLayoutManager(this,3)
        recycler.adapter=adapter
        refre_layout.setOnRefreshListener { persenter.initdata(url!!) }
    }
}