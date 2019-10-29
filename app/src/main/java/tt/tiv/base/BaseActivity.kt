package tt.tiv.base

import android.app.Activity
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import org.jetbrains.anko.startActivity
import org.jetbrains.anko.toast

/**
 * @ClassName: BaseActivity
 * @Description: 所有avtivity的基类
 * @Author: wsh
 * @Date: 19-10-27 下午6:49
 */
abstract class BaseActivity:AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(getLayoutId())
        initData()
        initListener()
    }

    /**
     * 监听器初始化
     */
    protected open fun initListener() {

    }

    /**
     * 数据初始化
     */
    protected  open fun initData() {

    }


    abstract fun getLayoutId(): Int
    /**
     * 吐司方法
     */
     fun myToast(msg:String){
        runOnUiThread{toast(msg)}
    }

    /**
     * 跳转另一界面，并销毁当前界面
     */
    inline fun <reified T: Activity>startActivityAndFinsh(){
        startActivity<T>()
        finish()
    }
}