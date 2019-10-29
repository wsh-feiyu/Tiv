package tt.tiv.widget

import android.content.Context
import android.util.AttributeSet
import android.view.View
import android.widget.RelativeLayout
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.item_livept.view.*
import tt.tiv.R
import tt.tiv.model.LivePtItem
import tt.tiv.model.ZhuboBean

/**
 * @ClassName: LivePtItemView
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午2:44
 */
class LiveZbItemView:RelativeLayout {
    fun setData(data: ZhuboBean) {
        pt_title.text=data.title
//        num.text=data.Number
        Picasso.get().load(data.img).into(pt_img)
    }

    constructor(context: Context?) : super(context)
    constructor(context: Context?, attrs: AttributeSet?) : super(context, attrs)
    constructor(context: Context?, attrs: AttributeSet?, defStyleAttr: Int) : super(
        context,
        attrs,
        defStyleAttr
    )
    init {
        View.inflate(context, R.layout.item_livept,this)
    }
}