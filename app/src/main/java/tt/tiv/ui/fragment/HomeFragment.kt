package tt.tiv.ui.fragment

import android.view.View
import kotlinx.android.synthetic.main.fragment_home.*
import org.jetbrains.anko.startActivity
import tt.tiv.R
import tt.tiv.base.BaseFragment
import tt.tiv.model.LiveUrl
import tt.tiv.presenter.impl.LivePtPresenterImpl
import tt.tiv.ui.activity.LivePtActivity
import tt.tiv.view.LivePtView

class HomeFragment : BaseFragment(), View.OnClickListener {


    override fun initView(): View? {
        return View.inflate(context,R.layout.fragment_home,null)
    }

    override fun initListener() {
        live1.setOnClickListener(this)
    }

    override fun onClick(v: View?) {
        when(v?.id){
            R.id.live1->activity?.startActivity<LivePtActivity>("url" to LiveUrl.LIVE1)
        }
    }
}