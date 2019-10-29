package tt.tiv.view

import tt.tiv.model.LivePtBean
import tt.tiv.model.LiveZbBean

interface LiveZbView {
    fun onLoad(result: LiveZbBean)
    fun onErr(msg:String?)
}