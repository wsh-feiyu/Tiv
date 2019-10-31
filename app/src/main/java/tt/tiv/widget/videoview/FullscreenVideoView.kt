package tt.tiv.widget.videoview

import android.content.Context
import android.content.pm.ActivityInfo
import android.util.AttributeSet
import com.dueeeke.videocontroller.CutoutUtil
import com.dueeeke.videoplayer.player.AbstractPlayer
import com.dueeeke.videoplayer.player.VideoView
import com.dueeeke.videoplayer.util.PlayerUtils

/**
 * @ClassName: FullscreenVideoView
 * @Description: 锁定全屏播放器
 * @Author: wsh
 * @Date: 19-10-31 下午2:20
 */
class FullscreenVideoView : VideoView<AbstractPlayer>{
    constructor(context: Context) : super(context)
    constructor(context: Context, attrs: AttributeSet?) : super(context, attrs)
    constructor(context: Context, attrs: AttributeSet?, defStyleAttr: Int) : super(
        context,
        attrs,
        defStyleAttr
    )
    init {
        CutoutUtil.adaptCutoutAboveAndroidP(context,true)
    }
    /**
     * 直接全屏开启播放
     */
    fun startFullScreenDirectly(){
        val scanForActivity = PlayerUtils.scanForActivity(context)
        scanForActivity?.let {
            it.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT)
            startFullScreen()
        }
    }

    override fun startPlay() {
        startFullScreenDirectly()
        super.startPlay()
    }

    override fun onBackPressed(): Boolean {
        return false

    }
}