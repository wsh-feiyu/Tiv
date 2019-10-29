package tt.tiv.base

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import org.jetbrains.anko.runOnUiThread
import org.jetbrains.anko.toast

/**
 * @ClassName: BaseFragment
 * @Description: 所有fragment的基类
 * @Author: wsh
 * @Date: 19-10-27 下午6:57
 */
abstract class BaseFragment:Fragment() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        init()
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return initView()
    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        initData()
        initListener()
    }

    abstract fun initView():View?

    protected fun init(){}
    protected open fun initData(){}
    protected open fun initListener(){}

    fun myToast(msg:String){
//        activity?.runOnUiThread {toast(msg)}
        context?.runOnUiThread { toast(msg) }
    }
}