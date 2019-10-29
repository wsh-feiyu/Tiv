package tt.tiv.view

import tt.tiv.model.LivePtBean

/**
 * @ClassName: LivePtView
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午12:20
 */
interface LivePtView {
    fun onLoad(result: LivePtBean)
    fun onErr(msg:String?)
}