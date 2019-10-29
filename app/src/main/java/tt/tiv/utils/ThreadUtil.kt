package tt.tiv.utils

import android.os.Handler
import android.os.Looper

/**
 * @ClassName: ThreadUtil
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午12:50
 */
object ThreadUtil {
    val handler= Handler(Looper.getMainLooper())

    fun runOnMainThread(runnable: Runnable){
        handler.post(runnable)
    }
}