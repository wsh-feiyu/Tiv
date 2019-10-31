package tt.tiv.ui.fragment

import android.content.DialogInterface
import android.view.View
import android.widget.EditText
import androidx.appcompat.app.AlertDialog
import kotlinx.android.synthetic.main.fragment_home.*
import org.jetbrains.anko.startActivity
import tt.tiv.R
import tt.tiv.base.BaseFragment
import tt.tiv.model.LiveUrl
import tt.tiv.ui.activity.LivePtActivity

class HomeFragment : BaseFragment(), View.OnClickListener {


    override fun initView(): View? {
        return View.inflate(context, R.layout.fragment_home, null)
    }

    override fun initListener() {
        live1.setOnClickListener(this)
        live2.setOnClickListener(this)
        live3.setOnClickListener(this)
        live_diy.setOnClickListener(this)
    }

    override fun onClick(v: View?) {
        when (v?.id) {
            R.id.live1 -> activity?.startActivity<LivePtActivity>("url" to LiveUrl.LIVE1)
            R.id.live2 -> activity?.startActivity<LivePtActivity>("url" to LiveUrl.LIVE2)
            R.id.live3 -> activity?.startActivity<LivePtActivity>("url" to LiveUrl.LIVE3)
            R.id.live_diy -> {
                val builder = AlertDialog.Builder(context!!)
                val editText=EditText(context)
                editText.setText(LiveUrl.LIVE2)
                editText.setHint(LiveUrl.LIVE2)
                builder.setTitle("请输入类似http://xx.xx.xx.../json.txt\n 去掉json.txt的地址")
                builder.setView(editText)
                builder.setPositiveButton("确定进入",  DialogInterface.OnClickListener{dialog,which->Unit
                    val text=editText.text.toString()
                    text?.let {
                        activity?.startActivity<LivePtActivity>("url" to it)
                    }
                })
                builder.setNegativeButton("取消",null)
                builder.show()
            }
        }
    }
}