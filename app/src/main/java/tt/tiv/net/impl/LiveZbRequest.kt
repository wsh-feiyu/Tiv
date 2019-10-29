package tt.tiv.net.impl

import tt.tiv.model.LivePtBean
import tt.tiv.model.LiveZbBean
import tt.tiv.net.BaseRequest
import tt.tiv.net.ResponseHandler

/**
 * @ClassName: LivePtRequest
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午1:44
 */
class LiveZbRequest(url: String, handler: ResponseHandler<LiveZbBean>) :
    BaseRequest<LiveZbBean>(url, handler) {
}