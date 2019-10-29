package tt.tiv.net

import com.google.gson.Gson
import java.lang.reflect.ParameterizedType

/**
 * @ClassName: BaseRequest
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午12:41
 */
open class BaseRequest<RESPONSE>(val url:String,val handler: ResponseHandler<RESPONSE>) {

    /**
     * 解析获取的数据并返回bean
     */
    open fun paseResult(result: String?): RESPONSE {
//        println(result)
        val gson= Gson()
        //获取泛型type的方法
        val type=(this.javaClass.genericSuperclass as ParameterizedType)
            .actualTypeArguments[0]

        val list=gson.fromJson<RESPONSE>(result,type)
        return list
    }

    /**
     * 发送请求
     */
    fun excute(){
        NetManager.manager.sendReuest(this)
    }

}