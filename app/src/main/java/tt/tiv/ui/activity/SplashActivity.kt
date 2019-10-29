package tt.tiv.ui.activity

import kotlinx.android.synthetic.main.activity_splash.*
import org.jetbrains.anko.alert
import org.jetbrains.anko.yesButton
import tt.tiv.R
import tt.tiv.base.BaseActivity

/**
 * @ClassName: SplashActivity
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-27 下午6:48
 */
class SplashActivity:BaseActivity() {
    override fun getLayoutId(): Int {
        return R.layout.activity_splash
    }

    override fun initData() {
        splash_bt.setOnClickListener {
            val pass=splash_ed.text.toString()
            pass?.let {
                if (pass=="1973")
                    startActivityAndFinsh<MainActivity>()
                else
                    alert("钥匙不对呀！","出错啦"){
                        yesButton {  }
                    }.show()
            }
        }
    }

}