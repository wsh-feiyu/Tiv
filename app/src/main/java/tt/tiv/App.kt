package tt.tiv

import android.app.Application
import com.dueeeke.videoplayer.ijk.IjkPlayerFactory
import com.dueeeke.videoplayer.player.VideoViewConfig
import com.dueeeke.videoplayer.player.VideoViewManager

/**
 * @ClassName: App
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-31 下午3:23
 */
class App:Application() {
    override fun onCreate() {
        super.onCreate()
        VideoViewManager.setConfig(
            VideoViewConfig.newBuilder()
            //使用使用IjkPlayer解码
            .setPlayerFactory(IjkPlayerFactory.create())
//            //使用ExoPlayer解码
//            .setPlayerFactory(ExoMediaPlayerFactory.create())
//            //使用MediaPlayer解码
//            .setPlayerFactory(AndroidMediaPlayerFactory.create())
            .build());
    }
}