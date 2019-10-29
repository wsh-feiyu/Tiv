package tt.tiv.net.impl

import tt.tiv.model.LivePtBean
import tt.tiv.net.BaseRequest
import tt.tiv.net.ResponseHandler

/**
 * @ClassName: LivePtRequest
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午1:44
 */
class LivePtRequest(url: String, handler: ResponseHandler<LivePtBean>) :
    BaseRequest<LivePtBean>(url, handler) {
}