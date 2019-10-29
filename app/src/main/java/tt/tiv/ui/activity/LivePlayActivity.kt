package tt.tiv.ui.activity

import androidx.core.view.isGone
import androidx.core.view.isVisible
import cn.jzvd.Jzvd
import kotlinx.android.synthetic.main.activity_liveplay.*
import tt.tiv.R
import tt.tiv.base.BaseActivity
import tt.tiv.utils.JZMediaIjk

class LivePlayActivity:BaseActivity() {
    override fun getLayoutId(): Int {
        return R.layout.activity_liveplay
    }

    override fun initData() {
        val url=intent.getStringExtra("url")
        Jzvd.releaseAllVideos()
        jzplayer.fullscreenButton.isGone=true
        jzplayer.backButton.isGone=true
        jzplayer.tinyBackImageView.isGone=true
        jzplayer.setUp(url,null,Jzvd.SCREEN_FULLSCREEN,JZMediaIjk::class.java)
        jzplayer.startVideo()
    }

    override fun onDestroy() {
        super.onDestroy()
        Jzvd.releaseAllVideos()
    }

    override fun onPause() {
        super.onPause()
        Jzvd.releaseAllVideos()
    }


}