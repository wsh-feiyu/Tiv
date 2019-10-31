package tt.tiv.base

import androidx.appcompat.app.AppCompatActivity
import com.dueeeke.videoplayer.player.AbstractPlayer
import com.dueeeke.videoplayer.player.VideoView
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.ViewCompat.onApplyWindowInsets
import android.view.WindowInsets
import androidx.core.view.ViewCompat.setOnApplyWindowInsetsListener
import android.os.Build
import android.os.Bundle
import android.icu.lang.UCharacter.GraphemeClusterBreak.T
import android.view.MenuItem
import android.view.View
import androidx.core.app.ComponentActivity.ExtraData
import androidx.core.content.ContextCompat.getSystemService
import tt.tiv.R


/**
 * @ClassName: BasePlayerActivity
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-31 下午2:48
 */
abstract class BasePlayerActivity<T:VideoView<AbstractPlayer>>:AppCompatActivity() {
    protected var mVideoView: T? = null

    protected open fun getTitleResId(): Int {
        return R.string.app_name
    }

    protected open fun getLayoutResId(): Int {
        return 0
    }

    protected open fun getContentView(): View? {
        return null
    }

    protected open fun enableBack(): Boolean {
        return true
    }

    override fun onCreate( savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (getLayoutResId() != 0) {
            setContentView(getLayoutResId())
        } else if (getContentView() != null) {
            setContentView(getContentView())
            //把基类的videoview 赋值给mVideoView，不然后面的 ondescroy onpause等都不起作用，因为初始为null
            mVideoView=getContentView() as T
        }

        //标题栏设置
        val actionBar = supportActionBar
        if (actionBar != null) {
            actionBar.setTitle(getTitleResId())
            if (enableBack()) {
                actionBar.setDisplayHomeAsUpEnabled(true)
            }
        }

        initView()

    }

    protected open fun initView() {

    }

    /**
     * 把状态栏设成透明
     */
    protected fun setStatusBarTransparent() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            val decorView = window.decorView
            decorView.setOnApplyWindowInsetsListener { v, insets ->
                val defaultInsets = v.onApplyWindowInsets(insets)
                defaultInsets.replaceSystemWindowInsets(
                    defaultInsets.systemWindowInsetLeft,
                    0,
                    defaultInsets.systemWindowInsetRight,
                    defaultInsets.systemWindowInsetBottom
                )
            }
            ViewCompat.requestApplyInsets(decorView)
            window.statusBarColor = ContextCompat.getColor(this, android.R.color.transparent)
        }
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.getItemId() === android.R.id.home) {
            finish()
        }
        return super.onOptionsItemSelected(item)
    }

    override fun onResume() {
        super.onResume()
        if (mVideoView != null) {
            mVideoView!!.resume()
        }
    }


    override fun onPause() {
        super.onPause()
        if (mVideoView != null) {
            mVideoView!!.pause()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        if (mVideoView != null) {
            mVideoView!!.release()
        }
    }

    override fun onBackPressed() {
        if (mVideoView == null || !mVideoView!!.onBackPressed()) {
            super.onBackPressed()
        }
    }
}