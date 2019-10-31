package tt.tiv.ui.activity

import androidx.core.view.isGone
import androidx.core.view.isVisible
import com.dueeeke.videoplayer.ijk.IjkPlayerFactory
import kotlinx.android.synthetic.main.activity_liveplay.*
import tt.tiv.R
import tt.tiv.base.BaseActivity

class LivePlayActivity:BaseActivity() {

    override fun getLayoutId(): Int {
        return R.layout.activity_liveplay
    }

    override fun initData() {
        val url=intent.getStringExtra("url")
        dkplayer.setUrl(url)
//        dkplayer.setPlayerFactory(IjkPlayerFactory.create())
        dkplayer.start()


    }

    override fun onDestroy() {
        super.onDestroy()
        dkplayer.release()
    }

    override fun onPause() {
        super.onPause()
        dkplayer.pause()
    }

    override fun onBackPressed() {
        if (!dkplayer.onBackPressed()){
            super.onBackPressed()
        }
    }

}