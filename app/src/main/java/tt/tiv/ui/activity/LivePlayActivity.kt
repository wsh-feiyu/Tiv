package tt.tiv.ui.activity


import android.view.View
import com.dueeeke.videoplayer.player.VideoView
import tt.tiv.R
import tt.tiv.base.BasePlayerActivity
import tt.tiv.widget.controller.FullScreenVideoController
import tt.tiv.widget.videoview.FullscreenVideoView

class LivePlayActivity: BasePlayerActivity<FullscreenVideoView>() {
    val videoView by lazy { FullscreenVideoView(this) }
    val controller by lazy { FullScreenVideoController(this) }

    override fun getContentView(): View? {
        return videoView
    }

    override fun initView() {
        val url=intent.getStringExtra("url")
        videoView.setUrl(url)
        controller.setPlayState(VideoView.PLAYER_FULL_SCREEN)
        videoView.setVideoController(controller)
        videoView.setScreenScaleType(VideoView.SCREEN_SCALE_DEFAULT)
        videoView.start()
    }

//    override fun onBackPressed() {
//        super.onBackPressed()
//        videoView.release()
//    }
//
//    override fun onDestroy() {
//        super.onDestroy()
//        videoView.release()
//    }

}

//    override fun getLayoutId(): Int {
//        return FullscreenVideoView(this)
//    }
//
//    override fun initData() {
//        val url=intent.getStringExtra("url")
//        dkplayer.setUrl(url)
////        dkplayer.setPlayerFactory(IjkPlayerFactory.create())
//        dkplayer.start()
//
//
//    }
//
//    override fun onDestroy() {
//        super.onDestroy()
//        dkplayer.release()
//    }
//
//    override fun onPause() {
//        super.onPause()
//        dkplayer.pause()
//    }
//
//    override fun onBackPressed() {
//        if (!dkplayer.onBackPressed()){
//            super.onBackPressed()
//        }
//    }
//
//}