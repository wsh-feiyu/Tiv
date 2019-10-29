package tt.tiv.net

/**
 * @ClassName: ResponseHandler
 * @Description: 网络请求返回的回调接口
 * @Author: wsh
 * @Date: 19-10-28 下午12:42
 */
interface ResponseHandler<RESPONSE> {
    fun onSuccess(result:RESPONSE)
    fun onErr(msg:String?)
}