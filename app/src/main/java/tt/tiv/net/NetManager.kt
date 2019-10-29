package tt.tiv.net

import okhttp3.*
import tt.tiv.utils.ThreadUtil
import java.io.IOException

/**
 * @ClassName: NetManager
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午12:46
 */
class NetManager private constructor(){
    val client by lazy { OkHttpClient() }

    companion object{
        val manager by lazy { NetManager() }
    }
    /**
     * 发送网络请求
     */
    fun <RESPONSE>sendReuest(req:BaseRequest<RESPONSE>){

        val request= Request.Builder().
            url(req.url).get()
            .build()
        client.newCall(request)
            .enqueue(object : Callback {
                //子线程中运行
                override fun onFailure(call: Call, e: IOException) {

                    req.handler.onErr(e?.message)
                }

                override fun onResponse(call: Call, response: Response) {

                    val result=response.body?.string()

                    val parseResult=req.paseResult(result)
                    ThreadUtil.runOnMainThread(Runnable { req.handler.onSuccess(parseResult) })
                }
            })
    }
}