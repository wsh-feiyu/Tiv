package tt.tiv.widget.controller

import android.content.Context
import android.util.AttributeSet
import android.view.View
import androidx.core.view.isGone
import com.dueeeke.videocontroller.StandardVideoController
import com.dueeeke.videoplayer.controller.MediaPlayerControl
import com.dueeeke.videoplayer.player.VideoView
import com.dueeeke.videoplayer.util.PlayerUtils
import tt.tiv.R

/**
 * @ClassName: FullScreenVideoController
 * @Description: 全屏播放控制器
 * @Author: wsh
 * @Date: 19-10-31 下午2:30
 */
class FullScreenVideoController:StandardVideoController<MediaPlayerControl> {
    constructor(context: Context) : super(context)
    constructor(context: Context, attrs: AttributeSet?) : super(context, attrs)
    constructor(context: Context, attrs: AttributeSet?, defStyleAttr: Int) : super(
        context,
        attrs,
        defStyleAttr
    )

    override fun onClick(v: View?) {
        val id=v?.id
        if (id== R.id.lock){
            doLockUnlock()
        }else if(id==R.id.iv_play || id==R.id.iv_replay){
            doPauseResume()
        }else if(id==R.id.back){
            PlayerUtils.scanForActivity(context).finish()
        }
    }

    override fun setPlayState(playState: Int) {
        super.setPlayState(playState)
//        mFullScreenButton.visibility= View.GONE
        if (playState==VideoView.PLAYER_FULL_SCREEN){
            mFullScreenButton.isGone=true
        }
    }

    override fun adjustReserveLandscape() {
        super.adjustReserveLandscape()
        mBottomContainer.setPadding(0,0,(mPadding+resources.getDimension(R.dimen.dkplayer_default_spacing).toInt()),0)
    }

    override fun adjustLandscape() {
        super.adjustLandscape()
        mBottomContainer.setPadding(mPadding,0,resources.getDimension(R.dimen.dkplayer_default_spacing).toInt(),0)
    }
}